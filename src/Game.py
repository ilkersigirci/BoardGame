import json
import Cells


class Game:

	def __init__(self,path):
		with open(path) as file:
			self.gameJson = json.load(file)


game = Game('game.json')

print(game.gameJson["cells"][2]["description"])

cell = Cells.Cells(4,"onur")
print(cell.description)