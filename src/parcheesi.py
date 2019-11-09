import Game

def parcheesi():
    test = Game.Game("game.json")
    print(test.gameJson["cells"][2]["description"])


if __name__ == '__main__':
    parcheesi()