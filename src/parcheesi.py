#import Game
from Cell import Cell
from Game import Game
from Player import Player
def parcheesi():
    #test = Game("game.json")
    #print(test.gameJson["cells"][2]["description"])
    player1 = Player(1,"ilker")
    player2 = Player(2,"onur")
    player3 = Player(3,"emine")
    
    newgame = Game("/home/arvethir/BoardGame/src/game.json")
"""
    player1.join(newgame)
    player2.join(newgame)
    player3.join(newgame)
    player1.ready()
    player2.ready()
    player3.ready()
"""
    
    #print(player2.currentGame)
if __name__ == '__main__':
    parcheesi()