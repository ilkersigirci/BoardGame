import json
from Cell import Cell
from Player import Player
import threading as th
import random
import string

class Game:

	games = []
	#notifyLock = th.Lock()
	
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
		self.gameState = 0 #0 oyun bitmeden 1 oyun bitince simdilik
		self.maxCurCycle = 0
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
		self.cellCount = len(self.cells)
		Game.games.append(self)

	def state(self):
		result = {"name":self.name, "cell":[],"player":[]}
		for cell in self.cells:
			result["cell"].append({"no":cell.cellno,"description":cell.description})
		for player in self.players:
			result["player"].append({"player":player.nickname,"credit":player.credit,"cycle":player.playerCycle, "cell":player.cellNo, "skip":player.skipLeftRound})
		return result
		
		

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
			print("-----------Game is Starting-----------")
			self.notifyPlayer()

	@staticmethod
	def listgames():
		for game in Game.games:
			print("-------------------------Printing Game MetaData-------------------------")
			print("Game name: {}, dice: {}, termination: {}, cycles: {}, initialCredit: {}, playerCount: {}"
					.format(game.name, game.dice, game.terminationStr, game.cycles, game.credit, len(game.players)))
			print(json.dumps(game.state(), indent = 2))
	
	def next(self, player):

		stateChange = {"player":player.nickname,"actions":[]}
		
		if(player.skipLeftRound != 0):
			stateChange["actions"].append({"skip": player.skipLeftRound})
			player.skipLeftRound -= 1
			return stateChange
			
			

		elif(player.currType == "roll"):
			diceRoll = random.randrange(self.dice) + 1
			tempCell = player.cellNo + diceRoll
			
			if tempCell >= self.cellCount:
				if(self.cycles):
					tempCell = tempCell % self.cellCount
					player.playerCycle += 1
					if player.playerCycle > self.maxCurCycle:
						self.maxCurCycle = player.playerCycle
						if self.terminationStr == "round" and self.maxCurCycle == self.terminationVal:
							self.gameState = 1	
				else:
					if(self.terminationStr == "finish"):
						tempCell = self.cellCount - 1
						self.gameState = 1
						
						print("Game should be ended")

			player.cellNo = tempCell

			stateChange["actions"].append({"dice roll ": diceRoll,"current cell":player.cellNo})
			#print("Player {} rolled the dice as {} and moved to cellNo: {}".format(player.nickname, diceRoll, tempCell))
			#stateChange.append({"dice roll": diceRoll})

			action = self.cells[player.cellNo].action
			#print("Player {} at cellno: {} action is {}".format(player.nickname, tempCell,action))
			if action is None:
				stateChange["actions"].append({"No action in cell:":player.cellNo})
				return stateChange
			# artifact= self.cells[cellNo].artifact 
			

			actionKey = list(action.keys())[0]
			actionValue = list(action.values())[0]

			

			if(actionKey == "skip"):
				player.skipLeftRound += actionValue
				stateChange["actions"].append({"skip": actionValue})
			
			elif(actionKey == "drop"):
				player.credit -= actionValue # check
				stateChange["actions"].append({"drop": actionValue})
				if player.credit <= 0 and self.terminationStr == "firstbroke":
					self.gameState = 1
			elif(actionKey == "add"):
				player.credit += actionValue # check
				stateChange["actions"].append({"drop": actionValue})
			elif(actionKey == "pay"):
				self.players[actionValue[0]].credit += actionValue[1]
				player.credit -= actionValue[1] # check
				stateChange["actions"].append({"drop": actionValue})
				if player.credit <= 0 and self.terminationStr == "firstbroke":
					self.gameState = 1
			
			elif(actionKey == "drawcard"):
				pass

			elif(actionKey == "jump"):
				if(isinstance(actionValue,str)): # Absolute Jump
					#print("absolute jump")
					actionValue = int(actionValue[1:])
					player.cellNo = actionValue
					stateChange["actions"].append({"jump absolute =": actionValue,"current cell":player.cellNo})
				else:
					player.cellNo += actionValue
					if player.cellNo >= self.cellCount:
						if self.cycles == True:
							player.cellNo %= self.cellCount 
						else:
							player.cellNo = self.cellCount-1
							self.gameState = 1
					stateChange["actions"].append({"jump relative": actionValue,"current cell":player.cellNo})
					
				

			elif(player.currType == "artifact"):
				pass

		return stateChange

	def notifyPlayer(self):
		
		if(self.terminationStr == "firstcollect"):
			pass

		playerCount = len(self.players)
		playerIndex = 0
		while(self.gameState == 0):
			self.currPlayer = self.players[playerIndex]
			if self.currPlayer.currType == None:
				(self.players[playerIndex]).turn("roll")
			if self.currPlayer.currType == "roll":
				self.currPlayer.currType = None
			playerIndex += 1

			if playerIndex == playerCount:
				playerIndex = 0
				self.currRound += 1
				
				#print(json.dumps(self.state(), indent = 4))
				print("-------------------Round: {} ended------------------".format(self.currRound))
				
		print("-------------------Game: ended------------------")
		print(json.dumps(self.state(), indent = 2))
