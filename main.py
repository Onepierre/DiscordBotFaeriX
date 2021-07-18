#https://discord.com/api/oauth2/authorize?client_id=441275954078285825&permissions=2416045120&scope=bot
from discord.ext import commands
import discord
from image_print import create_image
import numpy as np
from random import *
import xkcd as xkcd
import os
import random

CARTOON_MAX = 2488
BOT_NAME = "Twopierre"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="?", intents=intents)

@bot.event
async def on_ready():
    print("Le bot est prêt.")


@bot.event
async def on_reaction_add(reaction, user):
    1

@bot.event
async def on_message(message):
    # OTHER
    if not (message.author.name == BOT_NAME):
        text = message.content.replace(' ', '')
        if np.random.randint(1, 100) == 1:
            if "quoi" in text[-5:].lower():
                await message.channel.send("Feur!\nhttps://tenor.com/FgGg.gif")
            if "non" in text[-4:].lower():
                await message.channel.send("Bril!\nhttps://tenor.com/FgGg.gif")
            if "oui" in text[-4:].lower():
                await message.channel.send("Stiti!\nhttps://tenor.com/FgGg.gif")
    await bot.process_commands(message)


@bot.command(name="astrid", pass_context=True)
async def _astrid(ctx):
    create_image()
    with open("astrid/conseil.png", 'rb') as f:
        picture = discord.File(f)
        await ctx.channel.send(file=picture)


@bot.command(name="mtg", pass_context=True)
async def _mtg(ctx):
    if "cartoons" in ctx.channel.name:
        path = random.choice(os.listdir('cardboard_crack/'))
        name = path.split("_")[0].replace("-"," ")
        with open('cardboard_crack/' + path, 'rb') as f:
            picture = discord.File(f)
            if not name.isdigit() or name == "2021":
                await ctx.channel.send(name[0].capitalize() + name[1:])
            await ctx.channel.send(file=picture)
    

@bot.command(name="xkcd", pass_context=True)
async def _xkcd(ctx, var="False"):
    if "cartoons" in ctx.channel.name:
        err = False
        last_num = xkcd.getLatestComicNum()
        digit = (var.startswith("-") and var[1:].isdigit()) or var.isdigit()
        if digit:
            nb = int(var)
            if nb > last_num or nb <= -1 * last_num:
                err = True
                await ctx.channel.send("Ce numéro n'est pas valable, réessayez.")
            elif nb > 0:
                comic = xkcd.getComic(nb)
            else:
                comic = xkcd.getComic(last_num + 1 + nb)
        elif var == "last":
            comic = xkcd.getLatestComic()
        else:
            comic = xkcd.getRandomComic()
        if not err:
            await ctx.channel.send(comic.getTitle())
            await ctx.channel.send(comic.getImageLink())
            await ctx.channel.send(comic.getAltText())

@bot.command(name="exit")
async def _exit(ctx):
    if ctx.author.name == "Onepierre":
        exit()




# Bot launch


with open("token.txt", "r") as f:
    TOKEN = f.read()
bot.run(TOKEN)
