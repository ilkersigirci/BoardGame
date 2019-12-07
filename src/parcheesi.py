#import Game
from Cell import Cell
from Game import Game
from Player import Player
def parcheesi():

    player1 = Player(0,"ilker")
    player2 = Player(1,"onur")
    player3 = Player(2,"emine")

    player4 = Player(0,"ilker1")
    player5 = Player(1,"onur1")
    player6 = Player(2,"emine1")


    newgame = Game("configs/game.json")

    # Working Game Example
    player1.join(newgame)
    player2.join(newgame)
    player3.join(newgame)
    player1.ready()
    player2.ready()
    player3.ready()

"""     # User Case 1   -> Try to join after a player declares ready
    player1.join(newgame)
    player2.join(newgame)
    player1.ready()
    player3.join(newgame)
    player2.ready()
    player3.ready()

    # User Case 2  -> Not all players declare ready
    player1.join(newgame)
    player2.join(newgame)
    player3.join(newgame)
    player1.ready()
    player2.ready()
    
    # Use Case 3 -> Multiple Games

    newgame2 = Game("configs/game.json")
    player4.join(newgame2)
    player5.join(newgame2)
    player6.join(newgame2)
    player4.ready()
    player5.ready()
    player6.ready()

    Game.listgames() """
    







if __name__ == '__main__':
    parcheesi()