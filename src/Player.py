import json
from Cell import Cell


class Player:
    def __init__(self, id, nickname):
        self.nickname = nickname
        self.id = id
        self.CurrentCredit = 0 # init deger verilcek mi
        self.currentGame = None
        self.cellNo = 0
        self.skipLeftRound = 0
        self.currType = None
        self.credit = 0
    
    def join(self,game):
        if self.currentGame != None:
            try:
                game.join(self)
                self.credit = game.credit
                
            except ValueError(err):                
                print(err)
        else:
            self.currentGame = game

    def ready(self):
        if self.currentGame == None:
            raise  ValueError("You are not in a game!")
        else:
            self.currentGame.ready()

    def turn(self,type):

        if(type != "roll"):
            raise Exception("Only roll type is acceptable")
        
        if(self.currentGame == None):
            raise Exception("Player needs to join the game before turn command")
        
        self.currType = type
        self.currentGame.next(self)
