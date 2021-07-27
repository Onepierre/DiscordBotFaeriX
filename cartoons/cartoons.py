import pickle
import time
from datetime import datetime
from typing import DefaultDict
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

class cartoonsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.new_astrid.start()
        self.update_mtg.start()
        self.update_xkcd.start()


    @commands.command(name="follow", pass_context=True)
    async def _follow(self, ctx, name = None):
        id = ctx.message.guild.id
        track_mtg = pickle.load(open("cartoons/data/mtg_follow.txt", "rb"))   
        if name == None or name == "mtg":   
            for a in track_mtg:
                if a[0] == id and a[1] == ctx.channel.id:
                    role = discord.utils.get(self.bot.get_guild(id).roles,name=a[2])
                    if not role == None:
                        await ctx.message.author.add_roles(role)
                        await ctx.channel.send("{}, you'll be tagged for new Carboard Crack cartoons in this channel.".format(ctx.message.author.mention))
                    

        track_xkcd = pickle.load(open("cartoons/data/xkcd_follow.txt", "rb")) 
        if name == None or name == "xkcd":   
            for a in track_xkcd:
                if a[0] == id and a[1] == ctx.channel.id:
                    role = discord.utils.get(self.bot.get_guild(id).roles,name=a[2])
                    if not role == None:
                        await ctx.message.author.add_roles(role)
                        await ctx.channel.send("{}, you'll be tagged for new Xkcd cartoons in this channel.".format(ctx.message.author.mention))

    @commands.command(name="unfollow", pass_context=True)
    async def _unfollow(self, ctx, name = None):
        id = ctx.message.guild.id
        track_mtg = pickle.load(open("cartoons/data/mtg_follow.txt", "rb"))   
        if name == None or name == "mtg":   
            for a in track_mtg:
                if a[0] == id and a[1] == ctx.channel.id:
                    role = discord.utils.get(self.bot.get_guild(id).roles,name=a[2])
                    if not role == None:
                        await ctx.message.author.remove_roles(role)
                        await ctx.channel.send("{}, you won't be tagged anymore for new Carboard Crack cartoons in this channel.".format(ctx.message.author.mention))
                    

        track_xkcd = pickle.load(open("cartoons/data/xkcd_follow.txt", "rb")) 
        if name == None or name == "xkcd":   
            for a in track_xkcd:
                if a[0] == id and a[1] == ctx.channel.id:
                    role = discord.utils.get(self.bot.get_guild(id).roles,name=a[2])
                    if not role == None:
                        await ctx.message.author.remove_roles(role)
                        await ctx.channel.send("{}, you won't be tagged anymore for new Xkcd cartoons in this channel.".format(ctx.message.author.mention))
                    
    @commands.command(name="followmtg", pass_context=True)
    async def _follow_mtg(self, ctx, name = None):
        id = ctx.message.guild.id
        track = pickle.load(open("cartoons/data/mtg_follow.txt", "rb"))
        temp = []
        role = discord.utils.get(self.bot.get_guild(id).roles,name=name)
        tag = [id,ctx.channel.id,name]
        remove = False
        for a in track:
            if a[0] == tag[0] and a[1] == tag[1]:
                remove = True
        if remove:
            for a in track:
                if not (a[0] == tag[0] and a[1] == tag[1]):
                    temp.append(a)
            pickle.dump(temp, open("cartoons/data/mtg_follow.txt", "wb"))
            await ctx.channel.send("Successfully removed canal")
        else:
            track.append(tag)
            pickle.dump(track, open("cartoons/data/mtg_follow.txt", "wb"))
            await ctx.channel.send("Successfully added canal")
            if not role==None:
                await ctx.channel.send("{} will be tagged for new cartoons".format(role.mention))

    @commands.command(name="followxkcd", pass_context=True)
    async def _follow_xkcd(self, ctx, name = None):
        id = ctx.message.guild.id
        track = pickle.load(open("cartoons/data/xkcd_follow.txt", "rb"))
        temp = []
        role = discord.utils.get(self.bot.get_guild(id).roles,name=name)
        tag = [id,ctx.channel.id,name]
        remove = False
        for a in track:
            if a[0] == tag[0] and a[1] == tag[1]:
                remove = True
        if remove:
            for a in track:
                if not (a[0] == tag[0] and a[1] == tag[1]):
                    temp.append(a)
            pickle.dump(temp, open("cartoons/data/xkcd_follow.txt", "wb"))
            await ctx.channel.send("Successfully removed canal")
        else:
            track.append(tag)
            pickle.dump(track, open("cartoons/data/xkcd_follow.txt", "wb"))
            await ctx.channel.send("Successfully added canal")
            if not role == None:
                await ctx.channel.send("{} will be tagged for new cartoons".format(role.mention))

    @commands.command(name="followastrid", pass_context=True)
    async def _follow_astrid(self, ctx, name = None):
        id = ctx.message.guild.id
        track = pickle.load(open("cartoons/data/astrid_follow.txt", "rb"))
        temp = []
        role = discord.utils.get(self.bot.get_guild(id).roles,name=name)
        tag = [id,ctx.channel.id,name]
        remove = False
        for a in track:
            if a[0] == tag[0] and a[1] == tag[1]:
                remove = True
        if remove:
            for a in track:
                if not (a[0] == tag[0] and a[1] == tag[1]):
                    temp.append(a)
            pickle.dump(temp, open("cartoons/data/astrid_follow.txt", "wb"))
            await ctx.channel.send("Successfully removed canal")
        else:
            track.append(tag)
            pickle.dump(track, open("cartoons/data/astrid_follow.txt", "wb"))
            await ctx.channel.send("Successfully added canal")
            if not role==None:
                await ctx.channel.send("{} will be tagged for new cartoons".format(role.mention))

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
                path = random.choice(os.listdir('cartoons/cardboard_crack/'))

            name = path.split("_")[2].replace("-", " ")[:-4]
            if not err:
                with open('cartoons/cardboard_crack/' + path, 'rb') as f:
                    picture = discord.File(f)
                    if not name.isdigit() or name == "2021":
                        await ctx.channel.send(name[0].capitalize() + name[1:])
                    await ctx.channel.send(file=picture)
            await ctx.channel.send("Cartoon réalisé par Cardboard Crack (https://cardboard-crack.com/)")

    @commands.command(name="astrid", pass_context=True)
    async def _astrid(self,ctx):
        if "cartoons" in ctx.channel.name or "sages_paroles" in ctx.channel.name or "random" in ctx.channel.name:
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

    @tasks.loop(minutes = 60)
    async def update_mtg(self):
        urls_new = get_links()
        urls = pickle.load(open("cartoons/data/urls.txt", "rb"))
        new = False
        n = len(urls)

        for i, url in enumerate(urls_new):
            if not url in urls:
                new = True
                print("New cartoon :")
                name, file = download_post(url)
                urls = np.append(urls, [url])

                #Display it in some channels
                print(name)
                name = name.split("_")[1].replace("-", " ")
                track = pickle.load(open("cartoons/data/mtg_follow.txt", "rb"))
                for chanid in track:
                    with open(file, 'rb') as f:
                        chan = discord.utils.get(self.bot.get_guild(chanid[0]).channels,id = chanid[1])
                        if not chanid[2] == None:
                            role = discord.utils.get(self.bot.get_guild(chanid[0]).roles,name=chanid[2])
                            await chan.send('{}'.format(role.mention) )
                        
                        await chan.send(name[0].capitalize() + name[1:])
                        await chan.send(file=discord.File(f))
                        await chan.send("Cartoon réalisé par Cardboard Crack (https://cardboard-crack.com/)")
                
        path = 'cartoons/cardboard_crack/'
        files = os.listdir(path)
        for _, file in enumerate(files):
            MTG_CARTOONS.append(file)
        MTG_CARTOONS.sort()
                
        if new:
            pickle.dump(urls, open("cartoons/data/urls.txt", "wb"))

        else:
            print("No new Cardboard Crack cartoon")

    @tasks.loop(minutes = 60)
    async def update_xkcd(self):
        last_saved = pickle.load(open("cartoons/data/last_xkcd.txt", "rb"))
        last = xkcd.getLatestComic()
        if not last.getTitle() == last_saved:
            pickle.dump(last.getTitle(), open("cartoons/data/last_xkcd.txt", "wb"))
            track = pickle.load(open("cartoons/data/xkcd_follow.txt", "rb"))
            for chanid in track:
                chan = discord.utils.get(self.bot.get_guild(chanid[0]).channels,id = chanid[1])
                if not chanid[2] == None:
                    role = discord.utils.get(self.bot.get_guild(chanid[0]).roles,name=chanid[2])
                    await chan.send('{}'.format(role.mention) )
                await chan.send(last.getTitle())
                await chan.send(last.getImageLink())
                await chan.send(last.getAltText())
        else:
            print("No new Xkcd cartoon")

    @tasks.loop(minutes = 60*12)
    async def new_astrid(self):  
        now = datetime.now()
        now.strftime("%d/%m/%Y %H:%M:%S")
        print("Date: " + str(now)[0:19])
        track = pickle.load(open("cartoons/data/astrid_follow.txt", "rb"))
        create_image()
        for chanid in track:
            chan = discord.utils.get(self.bot.get_guild(chanid[0]).channels,id = chanid[1])
            if not chanid[2] == None:
                role = discord.utils.get(self.bot.get_guild(chanid[0]).roles,name=chanid[2])
                await chan.send('{}'.format(role.mention))
            with open("astrid/conseil.png", 'rb') as f:
                picture = discord.File(f)
                await chan.send(file=picture)

def setup(bot):
    # Every extension should have this function
    bot.add_cog(cartoonsCog(bot))
    
    path = 'cartoons/cardboard_crack/'
    files = os.listdir(path)
    for _, file in enumerate(files):
        MTG_CARTOONS.append(file)
    MTG_CARTOONS.sort()



