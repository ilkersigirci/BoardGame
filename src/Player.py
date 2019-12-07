import json
from Cell import Cell
from Cell import Artifact
import random


class Player:
    def __init__(self, id, nickname):
        self.nickname = nickname
        self.id = id
        self.currentGame = None
        self.cellNo = 0
        self.playerCycle = 0
        self.skipLeftRound = 0
        self.currType = None
        self.credit = 0
        self.artifacts = []
        print("user "+ self.nickname + " created!")
    def join(self,game):
        
        if self.currentGame == None:
            try:
                game.join(self)
                self.credit = game.credit
                self.currentGame = game
                
                
            except ValueError:                
                print("Player {} couldn't join the game".format(self.nickname))
        else:
            
            self.currentGame = game

    def ready(self):
        if self.currentGame == None:
            raise  ValueError("You are not in a game!")
        else:
            self.currentGame.ready(self)

    def turn(self,type):

        
        if(self.currentGame == None):
            raise Exception("Player needs to join the game before turn command")

        

        if type == "roll":
            self.currType = type
            stateChange = self.currentGame.next(self)
            print(stateChange)
            #print(json.dumps(stateChange, indent = 2))

        elif type == "drawcard":
            self.currType = type
            stateChange = self.currentGame.next(self)


        if(isinstance(type, Artifact)): #FIXME: type nasil gelecek?  Artifact olarak mi string olarak mi?
            self.currType = "artifact" #TODO: degisecek bu ad
            respond = [True, False]
            self.currentGame.pick(self, random.choice(respond))

"""
When a user enters a cell with artifact, s/he is given the turn(choice('Artifact Descr')).
User responds:
pick(True):
if price > 0 and user.credit >= price, price is dropped from users credit, and
if action is specified, action is taken on behalf of user.
if artifact is owned user becomes the owner of the artifact. Otherwise artifact simply disappears from the board.

pick(False):
Artifact is left in the board as it is.
"""