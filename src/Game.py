import json
from Cell import Cell
from Player import Player
import threading as th
import random
import string

class Game:

	games = []
	
	def __init__(self,path):
		with open(path) as file:
			self.gameJson = json.load(file)

		self.name = self.gameJson["name"]
		self.dice = self.gameJson["dice"]
		self.cycles = self.gameJson["cycles"]
		self.credit = self.gameJson["credit"]
		# self.cards = self.gameJson["cards"]
		self.currRound = 0
		self.cells = []
		self.players = []
		self.lock = th.Lock()
		self.conditionStr = None
		self.conditionVal = 0
		self.currPlayer = Player(0,"None")
		if(isinstance(self.gameJson["termination"],dict)):
			for key,value in self.termination.items():
				self.conditionStr = key
				self.conditionVal = value	
		else:
			self.conditionStr = gameJson["termination"]
		for cell in self.gameJson["cells"]:
			action = ""
			if "action" in cell: action = cell["action"]

			artifact = ""
			if "artifact" in cell: artifact = cell["artifact"]
			
			self.cells.append(Cell(cell["cellno"], cell["description"], action, artifact))
	
	def state(self):
		playerPositions = []
		for player in self.players:
			playerPositions.append(player.cellNo)
		return {
			
		}
	def join(self,player):
		if isinstance(player, Player) == False:
			raise Exception("Player is not valid.")
		with self.lock:
			if player in self.players:
				raise Exception("This player has already joined.")
			self.players.append(player)
		
	def ready(self, player):
		print("selam")

	def next(self, player):
		while(player != self.currPlayer):	continue

		if(player.skipLeftRound != 0):
			player.skipLeftRound -= 1
			

		elif(player.currType == "roll"):
			currentMove = random.randrange(self.dice + 1)
			player.cellNo += currentMove
			action = self.cells[player.cellNo].action 
			# artifact= self.cells[cellNo].artifact 

			actionKey = list(action.keys())[0]
			actionValue = list(action.values())[0]

			if(actionKey == "skip"):
				player.skipLeftRound += 1
			
			elif(actionKey == "drop"):
				player.credit += actionValue
			
			elif(actionKey == "drawcard"):
				pass

			elif(actionKey == "jump"):
				if(actionValue[0] == "="):
					#TODO: absolute location
					print("dummy output")
				else:
					player.cellNo += actionValue

			elif(player.currType == "drawcard"):
				pass
			elif(player.currType == "artifact"): 
				pass
		
		return{
		#TODO: player state change
			"move": currentMove
		}


	def notifyPlayer(self):
		if(self.conditionStr == "firstcollect"):
			pass
		elif (self.conditionStr == "round"):
			if self.conditionVal == self.currRound:
				pass # termination here
		elif self.conditionStr == "finish":
			pass
		elif self.conditionStr == "firstbroke":
			pass

		#if isinstance(player, Player) == False:
		#	raise ValueError("Player is not valid.")

		if(self.cycles == True):
			for player in self.players:
				player.turn("roll")


		for player in self.players:
			player.turn("roll")

		playerCount = len(self.players)

		for i in range(0,playerCount):
			self.currPlayer = self.players[i]
			(self.players[i]).turn("roll")