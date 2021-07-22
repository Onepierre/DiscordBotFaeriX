import pickle
import time
import shutil
from typing import DefaultDict
import requests
from discord.ext import commands,tasks
import discord
import numpy as np
from random import *
import xkcd as xkcd
import os
import random
from cartoons.cardboard_crack import get_links, download_post
from image_print import create_image


MTG_CARTOONS = []

class helpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def _help(self,ctx,function = None):
        channel = await ctx.message.author.create_dm()
        if function == None:
            await channel.send("__**Commandes**__\n\n**Cartoons**\n```?mtg [number]\n?xkcd [number]```\n**Werewolves**\n```?startlg [time]\n?stoplg```\n**Autres fonctions**\n```?astrid```\nEntrez `?help [fonction]` pour avoir plus de détails sur une fonction.")
        if function == "mtg":
            await channel.send("__**Commande**__\n`?mtg [number]`\n`number` est le numéro du Cartoon que vous souhaitez afficher. Il peut être négatif si vous souhaitez compter en partant du dernier cartoon paru.")
        if function == "xkcd":
            await channel.send("__**Commande**__\n`?xkcd [number]`\n`number` est le numéro du Cartoon que vous souhaitez afficher. Il peut être négatif si vous souhaitez compter en partant du dernier cartoon paru.")
        if function == "astrid":
            await channel.send("__**Commande**__\n`?astrid`\nAffiche une prédiction aléatoire d'Astrid.")
        if function == "startlg":
            await channel.send("__**Commande**__\n`?startlg [time]`\nDémarre une partie de Loup-Garou. `Time` est le temps d'inscription précédant la partie.")
        if function == "stoplg":
            await channel.send("__**Commande**__\n`?stoplg`\nStoppe la partie de Loup-Garou.")
        if function == "help":
            await channel.send("__**Commande**__\n`?help`\nPleh!")
        if function == "here":
            await ctx.message.channel.send("__**Commandes**__\n\n**Cartoons**\n```?mtg [number]\n?xkcd [number]```\n**Werewolves**\n```?startlg [time]\n?stoplg```\n**Autres fonctions**\n```?astrid```\nEntrez `?help [fonction]` pour avoir plus de détails sur une fonction.")






def setup(bot):
    # Every extension should have this function
    bot.add_cog(helpCog(bot))



