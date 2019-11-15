import json
import Cell


class Game:

	def __init__(self,path):
		with open(path) as file:
			self.gameJson = json.load(file)

		self.name = self.gameJson["name"]
		self.dice = self.gameJson["dice"]
		self.cycles = self.gameJson["cycles"]
		self.termination = self.gameJson["termination"]
		# self.cards = self.gameJson["cards"]
		self.cells = []

		for cell in self.gameJson["cells"]:
			action = ""
			if "action" in cell: action = cell["action"]

			artifact = ""
			if "artifact" in cell: artifact = cell["artifact"]
			
			self.cells.append(Cell.Cell(cell["cellno"], cell["description"], action, artifact))



game = Game('game.json')

print(len(game.cells))

""" cell = Cells.Cells(4,"onur")
print(cell.description) """