import json
from Cell import Cell


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

        if(type != "roll"):
            raise Exception("Only roll type is acceptable for this phase")
        
        if(self.currentGame == None):
            raise Exception("Player needs to join the game before turn command")
        if type == "roll":
            self.currType = type
            stateChange = self.currentGame.next(self)
            print(stateChange)
            #print(json.dumps(stateChange, indent = 2))
