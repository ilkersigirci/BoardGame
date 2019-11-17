import json
from Cell import Cell
from Player import Player
import threading as th
import random
import string

class Game:

	games = []
	notifyLock = th.Lock()
	
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
		self.terminationStr = None
		self.terminationVal = 0
		self.currPlayer = None
		self.readyPlayerCount = 0 #to check whether there is a ready player in the game or not
		if(isinstance(self.gameJson["termination"],dict)):
			self.terminationStr = list(self.gameJson["termination"].keys())[0]
			self.terminationVal = list(self.gameJson["termination"].values())[0]

		else:
			self.terminationStr = self.gameJson["termination"]

		for cell in self.gameJson["cells"]:
			action = None
			if "action" in cell:
				action = cell["action"]

			artifact = None
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
			elif self.readyPlayerCount >0:
				raise Exception("The game is about to start, you are late!")
			self.players.append(player)
		
	def ready(self, player):
		self.readyPlayerCount += 1
		if self.readyPlayerCount == len(self.players):
			print("game is starting")
			self.notifyPlayer()

	def listgames(self):
		print("list games")
		for game in games:
			print(game.state())
	
	def next(self, player):
		#while(player != self.currPlayer):	continue

		stateChange = []
		if(player.skipLeftRound != 0):
			player.skipLeftRound -= 1
			

		elif(player.currType == "roll"):
			currentMove = random.randrange(self.dice + 1)
			tempCell = player.cellNo + currentMove
			
			if tempCell > len(self.cells):
				if(self.cycles):
					if(self.terminationStr == "round"):
						tempCell = tempCell % len(self.cells)
						player.playerCycle += 1
				else:
					if(self.terminationStr == "finish"):
						tempCell = len(self.cells) - 1
						print("Game should be ended")
				player.cellNo = tempCell

			action = self.cells[player.cellNo].action
			print("Player {} at cellno: {} action is {}".format(player.nickname, tempCell,action))
			if action is None:
				print("No action specified")
				return stateChange
			# artifact= self.cells[cellNo].artifact 
			stateChange.append({"move": currentMove})

			actionKey = list(action.keys())[0]
			actionValue = list(action.values())[0]
			print(actionValue)

			if(actionKey == "skip"):
				player.skipLeftRound += actionValue
				stateChange.append({"skip": actionValue})
			
			elif(actionKey == "drop"):
				player.credit -= actionValue # check
				stateChange.append({"drop": actionValue})
			
			elif(actionKey == "drawcard"):
				pass

			elif(actionKey == "jump"):
				if(isinstance(actionValue[0],str)):
					#TODO: absolute location
					print("Absolute jump, but not implemented")
				else:
					player.cellNo += actionValue
					
				stateChange.append({"jump": actionValue})

			elif(player.currType == "artifact"): 
				pass
		print(stateChange)
		return stateChange

	def notifyPlayer(self):
		
		#if(self.terminationStr == "firstcollect"):
		#	pass
		#elif (self.terminationStr == "round"):
		#	if self.terminationVal == self.currRound:
		#		pass # termination here
		#elif self.terminationStr == "finish":
		#	pass
		#elif self.terminationStr == "firstbroke":
		#	pass

		#if isinstance(player, Player) == False:
		#	raise ValueError("Player is not valid.")

		#if(self.cycles == True):
		#	for player in self.players:
		#		player.turn("roll")


		#for player in self.players:
		#	player.turn("roll")

		if(self.terminationStr != "round"):
			print("Termination must be round for phase 1")

		playerCount = len(self.players)
		playerIndex = 0
		while(self.currRound != self.terminationVal):
			self.currPlayer = self.players[playerIndex]
			if self.currPlayer.currType == None:
				(self.players[playerIndex]).turn("roll")
			if self.currPlayer.currType == "roll":
				self.currPlayer.currType = None
				if playerIndex == playerCount-1:
					playerIndex = 0
					self.currRound += 1
					print("Round: {} ended".format(self.currRound))
				#
				#cellIndex = self.currPlayer.cellNo
				#if self.cells[cellIndex].action == "drawcard":
				#	self.currPlayer.turn("drawcard")
				#elif self.cells[cellIndex].action == "choice":
				#	self.currPlayer.turn("choice")
				#self.currPlayer.currType = None
			playerIndex += 1



