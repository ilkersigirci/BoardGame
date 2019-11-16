#import Game
from Cell import Cell
from Game import Game
def parcheesi():
    #test = Game("game.json")
    #print(test.gameJson["cells"][2]["description"])
    cell1 = Cell(2,"cell1")
    cell2 = Cell(4,"cell2")
    for i in range(2):
        print(Cell.cells[i].cellno)

if __name__ == '__main__':
    parcheesi()