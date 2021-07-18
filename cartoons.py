from discord.ext import commands
import discord
from image_print import create_image
import numpy as np
from random import *
import xkcd as xkcd
import os
import random

MTG_CARTOONS = []

class cartoonsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mtg", pass_context=True)
    async def _mtg(self,ctx, var="False"):
        if "cartoons" in ctx.channel.name or "sages_paroles" in ctx.channel.name:
            err = False
            digit = (var.startswith("-") and var[1:].isdigit()) or var.isdigit()
            if digit:
                nb = int(var)
                n = len(MTG_CARTOONS)
                if -n > nb or nb >= n:
                    err = True
                    await ctx.channel.send("Ce numéro n'est pas valable, réessayez.")
                else:
                    path = MTG_CARTOONS[nb]
            else:
                path = random.choice(os.listdir('cardboard_crack/'))

            name = path.split("_")[2].replace("-", " ")[:-4]
            if not err:
                with open('cardboard_crack/' + path, 'rb') as f:
                    picture = discord.File(f)
                    if not name.isdigit() or name == "2021":
                        await ctx.channel.send(name[0].capitalize() + name[1:])
                    await ctx.channel.send(file=picture)

    @commands.command(name="astrid", pass_context=True)
    async def _astrid(self,ctx):
        if "cartoons" in ctx.channel.name or "sages_paroles" in ctx.channel.name:
            create_image()
            with open("astrid/conseil.png", 'rb') as f:
                picture = discord.File(f)
                await ctx.channel.send(file=picture)

    @commands.command(name="xkcd", pass_context=True)
    async def _xkcd(self,ctx, var="False"):
        if "cartoons" in ctx.channel.name or "sages_paroles" in ctx.channel.name:
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


def setup(bot):
    # Every extension should have this function
    bot.add_cog(cartoonsCog(bot))

    path = 'cardboard_crack/'
    files = os.listdir(path)
    for _, file in enumerate(files):
        MTG_CARTOONS.append(file)
    MTG_CARTOONS.sort()
