from datetime import date
from discord.ext import tasks,commands
import discord
import numpy as np
from random import *
import time
import math 
import xkcd as xkcd
from werewolves.model import LG_Game
BOT_NAME = "Twopierre"
BRAVO_LIST = ['\U0001F1E7', '\U0001F1F7', '\U0001F1E6', '\U0001F1FB', '\U0001F1F4', '\U0001F44F']

NAME_COLOR_LIST = ["rouge" , "orange", "jaune", "vert", "bleu",  "violet", "marron"]
COLOR_LIST = {"rouge": '\U0001F7E5', "orange": '\U0001F7E7', "jaune": '\U0001F7E8', "vert": '\U0001F7E9', "bleu": '\U0001F7E6',  "violet": '\U0001F7EA', "marron": '\U0001F7EB'}

ROLE_DESCRIPTIONS = {"loup" : "Tu es loup-garou.", "villageois" : "Tu es villageois.", "sorciere" : "Tu es sorciere."}

LETTERS_CODE = ['\U0001F1E6', '\U0001F1E7',
                '\U0001F1E8', '\U0001F1E9', '\U0001F1EA', '\U0001F1EB', '\U0001F1EC']

LG = LG_Game()


class werewolvesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.name != BOT_NAME:
            if "c'est quelle couleur le" in reaction.message.content:
                couleur = reaction.message.content[:-1].split(' ')[-1]
                if reaction.emoji == COLOR_LIST[couleur]:
                    await reaction.message.channel.send(f"Bien joué {user.mention}. Tu n'es pas daltonien")
                    await reaction.message.delete()
                else:
                    await reaction.message.channel.send(f"Non {user.mention}! Tu t'es fait avoir COMME UN BLEU!")

    @commands.Cog.listener()
    async def on_message(self, message):

        # For LG games
        if message.author.name == BOT_NAME:
            if "d'une partie de Loup-Garou." in message.content:
                await message.add_reaction('\U0001F44D')
                LG.message_entrance = message
            elif "Joueurs inscrits" in message.content:
                LG.message_entered = message
            elif "Qui les loups vont-ils devorer ce soir" in message.content:
                LG.message_wolves_vote = message
                for react in LETTERS_CODE[:len(LG.kill_potential)]:
                    await LG.message_wolves_vote.add_reaction(react)
            elif "Qui allez-vous envoyer au bucher" in message.content:
                LG.message_public_vote = message
                for react in LETTERS_CODE[:len(LG.alive_players)]:
                    await LG.message_public_vote.add_reaction(react)
            elif "Vous pouvez tuer quelqu'un parmi" in message.content:
                LG.message_witch_kill = message
                for react in LETTERS_CODE[:len(LG.kill_potential)]:
                    await LG.message_witch_kill.add_reaction(react)
            elif "Vous pouvez ressusciter quelqu'un parmi" in message.content:
                LG.message_witch_rez = message
                for react in LETTERS_CODE[:len(LG.night_kills)]:
                    await LG.message_witch_rez.add_reaction(react)

    @commands.command(name="lg")
    async def _lg(self, ctx, entering_duration=10):
        LG.start_game(ctx, entering_duration)
        self.lg.start()

    @commands.command(name="stoplg")
    async def _stoplg(self, ctx):
        roles = ctx.guild.roles
        for role in roles:
            if role.name == "lG":
                LG.lg_role = role
            if role.name == 'IG':
                LG.other_role = role

        for player in ctx.guild.members:
            await player.remove_roles(LG.lg_role)
            await player.remove_roles(LG.other_role)
        self.lg.cancel()
        print("LG game cancelled")

    # Command which manage werewolves game
    @tasks.loop(seconds=2)
    async def lg(self):
        # Create the inscription message of a game
        if LG.phase == "enter":
            LG.phase = "waiting"
            await LG.public_lg_channel.send("Début d'une partie de Loup-Garou.\nInscrivez-vous en réagissant \U0001F44D")
            await LG.public_lg_channel.send("Durée d'inscription : " + str(LG.entering_duration) + " secondes.")
            await LG.public_lg_channel.send("Joueurs inscrits: ")

        # Get entered people and wait
        elif LG.phase == "waiting":
            entered = []
            for reaction in LG.message_entrance.reactions:
                if reaction.emoji == '\U0001F44D':
                    async for user in reaction.users():
                        entered.append(user)

            text = f"Joueurs inscrits :"
            for user in entered:
                text += "\n" + f"{user.mention}"
            await LG.message_entered.edit(content=text)

            # END OF ENTERINGS
            if (time.time() - LG.time) > LG.entering_duration:
                LG.players = entered
                LG.phase = "init"

                await LG.message_entrance.delete()
                await LG.public_lg_channel.send("Début de la partie ! ")

        # Attributes randomly roles
        elif LG.phase == "init":

            LG.n_players = len(LG.players)
            LG.n_wolves = max(math.floor(LG.n_players/4), 1)
            LG.alive_players = role_attribution(LG.players)
            # DMing players to give them their role
            for player, role in LG.alive_players:
                await player.remove_roles(LG.lg_role)
                await player.remove_roles(LG.other_role)
                if not(player.name == BOT_NAME):
                    if role == "loup":
                        LG.wolves.append(player)
                        await player.add_roles(LG.lg_role)
                    else:
                        await player.add_roles(LG.other_role)

                    msg = ROLE_DESCRIPTIONS[role]
                    channel = await player.create_dm()
                    await channel.send(msg)

            LG.phase = "night"

        # Night phase
        elif LG.phase == "night":
            if LG.first_night:
                LG.first_night = False
                
            #Entering night phase
            if LG.night_phase == 0:
                await LG.public_lg_channel.send("La nuit tombe sur le village et tous s'endorment.")
                LG.night_phase += 1
                LG.time = time.time()
                LG.message_wolves_chat = False

            # Wolves chat
            elif LG.night_phase == 1:
                if LG.message_wolves_chat == False:
                    await LG.public_lg_channel.send("Les loups se reveillent.")
                    await LG.private_lg_channel.send("Les loups se reveillent.\nVous avez " + str(LG.wolves_chattime) + " secondes pour discuter.")
                    LG.message_wolves_chat = True
                # If waited enough after the votetime
                if time.time() - LG.time > LG.wolves_chattime:
                    LG.night_phase += 1
                    LG.time = time.time()
                    LG.message_wolves_vote = ""

            # Wolves vote
            elif LG.night_phase == 2:
                if LG.message_wolves_vote == "":
                    LG.kill_potential = []
                    for player, role in LG.alive_players:
                        if not (role == "loup"):
                            LG.kill_potential.append(player)
                    text = "Qui les loups vont-ils devorer ce soir?"

                    for i, user in enumerate(LG.kill_potential):
                        text += "\n" + LETTERS_CODE[i] + " : " + user.name

                    text += "\nVous avez " + \
                        str(LG.wolves_votetime) + " secondes pour voter."
                    await LG.private_lg_channel.send(text)

                # If waited enough after the votetime
                if time.time() - LG.time > LG.wolves_votetime:
                    LG.night_phase += 1

            # Wolves ending vote
            elif LG.night_phase == 3:
                LG.night_kills = []
                votes = [0]*len(LG.kill_potential)
                for reaction in LG.message_wolves_vote.reactions:
                    if reaction.emoji in LETTERS_CODE:
                        index = LETTERS_CODE.index(reaction.emoji)
                        async for user in reaction.users():
                            if (user, "loup") in LG.alive_players:
                                votes[index] += 1
                maximum = max(votes)
                count = 0
                for a in votes:
                    if a == maximum:
                        count += 1
                if count > 1:
                    await LG.private_lg_channel.send("Vous n'avez pas reussi à decider qui manger. Vous finissez donc la nuit à jeun.")
                    await LG.public_lg_channel.send("Les loups n'ont pas reussi à decider qui manger.")
                else:
                    mort = LG.kill_potential[votes.index(maximum)]
                    LG.night_kills.append(mort)
                    await LG.private_lg_channel.send("Vous avez devore " + mort.name + ".")
                    await LG.public_lg_channel.send("Les loups ont mangé un villageois et sont partis se recoucher.")
                LG.time = time.time()
                LG.night_phase += 1

            # Witch time
            elif LG.night_phase == 4:
                # First we check if witch is alive
                if not(LG.witch, "sorciere") in LG.alive_players:
                    LG.night_phase += 2

                else:
                    if LG.witch_wake:
                        await LG.public_lg_channel.send("La sorcière se reveille.")
                        LG.witch_wake = False

                    channel = await LG.witch.create_dm()

                    if LG.message_witch_kill == "":
                        if LG.witch_kill:
                            # Removing players who have been killed during the night
                            LG.kill_potential = []
                            for user, _ in LG.alive_players:
                                if not user in LG.night_kills:
                                    LG.kill_potential.append(user)

                            text = "Vous pouvez tuer quelqu'un parmi"
                            for i, user in enumerate(LG.kill_potential):
                                text += "\n" + LETTERS_CODE[i] + " : " + user.name
                            text += "\nVous avez " + \
                                str(LG.wolves_votetime) + " secondes pour voter."
                            await channel.send(text)
                        else:
                            await channel.send("Vous avez déjà utilise votre potion de mort.")
                            LG.message_witch_kill = "a"

                    if LG.message_witch_rez == "":
                        if LG.witch_rez:
                            text = "Vous pouvez ressusciter quelqu'un parmi"
                            for i, user in enumerate(LG.night_kills):
                                text += "\n" + LETTERS_CODE[i] + " : " + user.name
                            text += "\nVous avez " + \
                                str(LG.wolves_votetime) + " secondes pour voter."
                            await channel.send(text)
                        else:
                            await channel.send("Vous avez déjà utilise votre potion de vie.")
                            LG.message_witch_rez = "a"

                    # If waited enough after the votetime
                    if time.time() - LG.time > LG.wolves_votetime:
                        LG.night_phase += 1

            # End witch vote
            elif LG.night_phase == 5:
                channel = await LG.witch.create_dm()
                if LG.witch_kill:
                    votes = [0]*len(LG.kill_potential)
                    for reaction in LG.message_witch_kill.reactions:
                        if reaction.emoji in LETTERS_CODE:
                            index = LETTERS_CODE.index(reaction.emoji)
                            async for user in reaction.users():
                                votes[index] += 1
                    maximum = max(votes)
                    count = 0
                    for a in votes:
                        if a == maximum:
                            count += 1
                    if count > 1 or maximum == 1:
                        await channel.send("Vous n'avez pas tué ce soir")
                    else:
                        mort = LG.kill_potential[votes.index(maximum)]
                        LG.night_kills.append(mort)
                        await channel.send("Vous avez empoisonné " + mort.name + ".")
                        LG.witch_kill = False

                if LG.witch_rez:
                    votes = [0]*len(LG.night_kills)
                    for reaction in LG.message_witch_rez.reactions:
                        if reaction.emoji in LETTERS_CODE:
                            index = LETTERS_CODE.index(reaction.emoji)
                            async for user in reaction.users():
                                votes[index] += 1
                    maximum = max(votes)
                    count = 0
                    for a in votes:
                        if a == maximum:
                            count += 1
                    if count > 1 or maximum == 1:
                        await channel.send("Vous n'avez pas ressuscite ce soir")
                    else:
                        saved = LG.night_kills[votes.index(maximum)]
                        LG.night_kills.remove(saved)
                        await channel.send("Vous avez sauve " + saved.name + ".")
                        LG.witch_rez = False
                await LG.public_lg_channel.send("La sorcière se rendort")

                LG.time = time.time()
                LG.night_phase += 1

            # End night
            elif LG.night_phase == 6:
                LG.phase = "day"
                LG.night_phase = 0
                LG.day_phase = 0
                LG.witch_wake = True

        # Day phase
        elif LG.phase == "day":

            # News of the day
            if LG.day_phase == 0:
                await LG.public_lg_channel.send("Le village se reveille. Sauf...")
                if len(LG.night_kills) == 0:
                    await LG.public_lg_channel.send("Personne")
                for mort in LG.night_kills:
                    for user, role in LG.alive_players:
                        if user == mort:
                            LG.alive_players.remove((mort, role))
                            await LG.public_lg_channel.send(f"{mort.mention}, un " + role + ".")
                LG.day_phase += 1
                victory, sent = is_end_lg()

            # Public discussion
            elif LG.day_phase == 1:
                if LG.message_public_chat == False:
                    LG.time = time.time()
                    await LG.public_lg_channel.send("Le village décide de se concerter.")
                    await LG.public_lg_channel.send("Vous avez " + str(LG.public_chattime) + " secondes pour discuter.")
                    LG.message_public_chat = True

                # If waited enough after the votetime
                if time.time() - LG.time > LG.public_chattime:
                    LG.day_phase += 1
                    LG.time = time.time()
                    LG.message_public_vote = ""

            # Public vote
            elif LG.day_phase == 2:
                if LG.message_public_vote == "":
                    text = "Qui allez-vous envoyer au bucher?"

                    for i, (user, _) in enumerate(LG.alive_players):
                        text += "\n" + LETTERS_CODE[i] + " : " + f"{user.mention}"

                    text += "\nVous avez " + \
                        str(LG.public_votetime) + " secondes pour voter."
                    await LG.public_lg_channel.send(text)
                    LG.kill_potential = []
                    for player, role in LG.alive_players:
                        LG.kill_potential.append(player)

                # If waited enough after the votetime
                if time.time() - LG.time > LG.public_votetime:
                    LG.day_phase += 1

            # Public end vote
            elif LG.day_phase == 3:
                votes = [0]*len(LG.alive_players)
                for reaction in LG.message_public_vote.reactions:
                    if reaction.emoji in LETTERS_CODE:
                        index = LETTERS_CODE.index(reaction.emoji)
                        async for user in reaction.users():
                            for user_test in LG.alive_players:
                                if user == user_test:
                                    votes[index] += 1
                maximum = max(votes)
                count = 0
                for a in votes:
                    if a == maximum:
                        count += 1
                if count > 1:
                    await LG.public_lg_channel.send("Vous n'avez pas reussi à vous décider. Personne n'est tué")
                else:
                    mort = LG.kill_potential[votes.index(maximum)]
                    for user, role in LG.alive_players:
                        if user == mort:
                            LG.alive_players.remove((mort, role))
                            await LG.public_lg_channel.send("Vous avez brûlé  " + f"{mort.mention}. Il était " + role + ".")
                LG.phase = "night"
                LG.night_phase = 0
                LG.day_phase = 0

            # Victory check
            victory, sent = is_end_lg()
            if victory:
                await LG.public_lg_channel.send("Fin de partie")
                await LG.public_lg_channel.send(sent)
                LG.phase = "end"

        # End phase
        elif LG.phase == "end":
            roles = LG.ctx.guild.roles
            for role in roles:
                if role.name == "lG":
                    LG.lg_role = role
                if role.name == 'IG':
                    LG.other_role = role

            for player in LG.ctx.guild.members:
                await player.remove_roles(LG.lg_role)
                await player.remove_roles(LG.other_role)
            self.lg.cancel()


def setup(bot):
    # Every extension should have this function
    bot.add_cog(werewolvesCog(bot))

def role_attribution(players):
    res = []
    compo = np.loadtxt("werewolves/composition.txt",  dtype='str')
    if len(compo) == len(players):
        # Choose wolves
        np.random.shuffle(compo)
        for i in range(len(compo)):
            res.append((players[i], compo[i]))
            if compo[i] == "sorciere":
                LG.witch = players[i]

        return res

    return "Mauvaise composition"


def is_end_lg():
    nb_loups = 0
    nb_village = 0
    nb_solo = 0
    for _, role in LG.alive_players:
        if role == "loup":
            nb_loups += 1
        if role == "villageois" or role == "sorciere":
            nb_village += 1
    if nb_solo > 0:
        return False, ""
    if nb_loups == 0:
        return True, "Le village gagne."
    if nb_loups >= nb_village:
        return True, "Les loups gagnent."
    return False, ""
