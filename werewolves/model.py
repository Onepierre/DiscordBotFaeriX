import time
import numpy as np

class LG_Game():
    def __init__(self):
        self.players = []
        self.time = 0
        self.ctx = 0
        self.lg_role = ""
        self.other_role = ""

        self.phase = "enter"

        self.first_night = True
        self.night_phase = 0
        self.day_phase = 0
        ## PHASES
        # enter : initialization of game
        # waiting : wait to begin the game
        # init : choosing roles/events etc
        # night : night of the game
        # day : day of the game

        self.public_lg_channel = ""
        self.private_lg_channel = ""
        self.message_entrance = ""
        self.message_entered = ""

        self.message_wolves_chat = False
        self.message_public_chat = False

        self.message_wolves_vote = ""
        self.message_public_vote = ""
        self.message_witch_kill = ""
        self.message_witch_rez = ""

        # Game variables
        self.n_players = 0
        self.n_wolves = 0
        self.alive_players = []
        self.night_kills = []
        self.wolves = []

    def start_game(self, ctx, entering_duration):
        self.time = time.time()
        self.entering_duration = entering_duration
        self.wolves_chattime = 6
        self.wolves_votetime = 10
        self.public_chattime = 6
        self.public_votetime = 10
        self.phase = "enter"
        self.ctx = ctx

        self.first_night = True

        # Special roles
        self.witch_wake = True
        self.witch = ""
        self.witch_kill = True
        self.message_witch_kill = ""

        self.witch_rez = True
        self.message_witch_rez = ""

        self.players = []
        self.kill_potential = []
        self.alive_players = []
        self.night_kills = []
        self.night_phase = 0
        self.day_phase = 0
        # Get special channels for lg game
        # lg-chat : special chat for werewolves
        # acces : role "lG"
        #
        # lg_game : public chat for the game
        # access : everyone
        for channel in ctx.guild.channels:
            if channel.name == "lg-chat":
                self.private_lg_channel = channel
            if channel.name == "lg-game":
                self.public_lg_channel = channel

        ## Server setup
        # Two roles named lG and IG.
        # lG for wolves, IG for others to make no difference with wolves
        roles = ctx.guild.roles
        for role in roles:
            if role.name == "lG":
                self.lg_role = role
            if role.name == 'IG':
                self.other_role = role
