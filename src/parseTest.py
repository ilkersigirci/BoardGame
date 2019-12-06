import json
from Cell import Cell

with open("configs/game.json") as file:
	gameJson = json.load(file)

print(gameJson["cells"][1]["action"] == None)
