import json
from Cell import Cell
from Player import Player
import threading as th

class Game:

	games = []
	
	def __init__(self,path):
		with open(path) as file:
			self.gameJson = json.load(file)

		self.name = self.gameJson["name"]
		self.dice = self.gameJson["dice"]
		self.cycles = self.gameJson["cycles"]
		self.termination = self.gameJson["termination"]
		# self.cards = self.gameJson["cards"]
		self.currRound = 0
		self.cells = []
		self.players = {}
		self.lock = th.Lock()		

		for cell in self.gameJson["cells"]:
			action = ""
			if "action" in cell: action = cell["action"]

			artifact = ""
			if "artifact" in cell: artifact = cell["artifact"]
			
			self.cells.append(Cell.Cell(cell["cellno"], cell["description"], action, artifact))
	
	def state(self):
		playerPositions = []
		for player in self.players:
			playerPositions.append(player.cellNo)
		return {
			
		}

	def notifyPlayer(self, player, method):
		
		if isinstance(player, Player) == False:
			raise ValueError("Player is not valid.")

		if method != Player.turn():
			raise ValueError("Invalid notify method")

		with self.lock:
			



""" cell = Cells.Cells(4,"onur")
print(cell.description) """