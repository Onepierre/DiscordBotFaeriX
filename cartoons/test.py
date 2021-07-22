import pickle
import time
import shutil
import requests
from discord.ext import commands, tasks
import discord
import numpy as np
from random import *
import xkcd as xkcd
import os
import random
from cardboard_crack import get_links, get_image, download_post

pickle.dump(xkcd.getRandomComic().getTitle(),
            open("data/last_xkcd.txt", "wb"))

# Reset follow_mtg file
# pickle.dump([],open("data/mtg_follow.txt", "wb"))

