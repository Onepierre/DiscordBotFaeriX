
import pickle
import time
from datetime import datetime
from typing import DefaultDict
from discord.ext import commands,tasks
import discord
import numpy as np
import pandas as pd
from random import *
import xkcd as xkcd
import os
import random
from cartoons.cardboard_crack import get_links, download_post
from image_print import create_image
from hate_speech.model import CustomCamemBERTModel
from transformers import RobertaTokenizerFast
import torch
import torch.nn as nn
import torch.nn.functional as F
BOT_NAME = "Twopierre"
LETTERS_CODE = ['\U0001F1E6', '\U0001F1E7','\U0001F1E8']

def argm(res):
    if res[0] > res[1] and res[0] > res[2]:
        return 0
    if res[1] > res[0] and res[1] > res[2]:
        return 1
    if res[2] > res[1] and res[2] > res[1]:
        return 2
    return -1

def predict(sentences,tokenizer,model):
    logits = []
    with torch.no_grad():  
        encoding = tokenizer.batch_encode_plus(sentences, return_tensors='pt', padding=True, truncation=True,max_length=512)
        outputs = model(**encoding)[0]
        outputs = F.softmax(outputs, dim=1)
        for i in outputs:
            logits.append(i.numpy())
    return logits

class hateSpeechCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = None
        self.tokenizer = None
        self.dataset = pd.read_csv("hate_speech/dataset.csv")
        self.msg = None

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.name == BOT_NAME:
            1
        else:
            if "Aidez-moi à m'améliorer! Quelle est la vraie réponse?\n" in reaction.message.content and self.msg in reaction.message.content:
                res = [0,0,0]
                for react in reaction.message.reactions:
                    if react.emoji == '\U0001F1E6':
                        # Normal
                        async for user in react.users():
                            res[0] += 1
                    elif react.emoji == '\U0001F1E7':
                        # Offensive
                        async for user in react.users():
                            res[1] += 1
                    elif react.emoji == '\U0001F1E8':
                        # Hateful
                        async for user in react.users():
                            res[2] += 1
                rep = argm(res)
                ind = self.dataset[self.dataset["text"]==self.msg].index.values
                if len(ind) == 0:
                    self.dataset = self.dataset.append({'text': self.msg, 'label':rep}, ignore_index=True)
                else:
                    self.dataset.at[ind[0],"label"] = rep
                #if reaction.message.content in self.dataset[]
                self.dataset.to_csv("hate_speech/dataset.csv", index = False)
                
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.name == BOT_NAME:
            if "Aidez-moi à m'améliorer! Quelle est la vraie réponse?\n" in message.content:
                await message.add_reaction('\U0001F1E6') 
                await message.add_reaction('\U0001F1E7')
                await message.add_reaction('\U0001F1E8')

    @commands.command(name="loadBert", pass_context=True)
    async def _loadBert(self, ctx):
        model_name = "camembert-base"
        self.tokenizer = RobertaTokenizerFast.from_pretrained(model_name, do_lower_case=True)
        self.model = CustomCamemBERTModel() 
        self.model.load_state_dict(torch.load("hate_speech/camembert.ckpt"))
        self.model.eval()
        await ctx.channel.send("CamemBERT successfully loaded")

    @commands.command(name="unloadBert", pass_context=True)
    async def _unloadBert(self, ctx):
        self.tokenizer = None
        self.model = None
        await ctx.channel.send("CamemBERT successfully unloaded")
        
    @commands.command(name="Bert", pass_context=True)
    async def _Bert(self, ctx, name = None):
        if self.tokenizer == None or self.model == None:
            await ctx.channel.send("""CamemBERT model not loaded. Please load it with `?loadBert`""")
        else:
            self.msg = name.lower()
            sentences = [name.lower()]
            logits = predict(sentences,self.tokenizer,self.model)
            for i in range(len(logits)):
                id = np.argmax(np.array(logits[i]))
                msg = name + "\nNormal-----Proba: " + str(round(logits[i][0],2))+"\nOffensive---Proba: " + str(round(logits[i][1],2))+"\nHateful------Proba: " + str(round(logits[i][2],2))
                await ctx.channel.send(msg)
                await ctx.channel.send(name.lower() + "\nAidez-moi à m'améliorer! Quelle est la vraie réponse?\n" + '\U0001F1E6' + " Normal\n"+ '\U0001F1E7' + " Offensive\n" + '\U0001F1E8' + " Hateful\n")

                
def setup(bot):
    # Every extension should have this function
    bot.add_cog(hateSpeechCog(bot))


