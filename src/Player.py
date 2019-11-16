import json
from Cell import Cell

class Player:
    def __init__(self, id, nickname):
        self.nickname = nickname
        self.id = id
        self.CurrentCredit = 0 # init deger verilcek mi
        self.currentGame = None
    
    def join(self,game):
        if self.currentGame != None:
            try:
                game.join(self)
                
            except:
                #do something
            else:
                self.currentGame = game

    def ready(self):
        if self.currentGame == None:
            raise  ValueError("You are not in a game!")
        else:
            self.currentGame.ready()



            