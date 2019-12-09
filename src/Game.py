import json
from Cell import Cell
from Player import Player
import threading as th
import random

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
		self.cards = self.gameJson["cards"]
		self.currRound = 0
		self.cells = []
		self.players = []
		self.mutex = th.Lock()
		self.mutex2 = th.Lock()
		self.readyCond = th.Condition(self.mutex)
		self.turnCond = th.Condition(self.mutex2)
		self.currPlayer = None
		self.readyPlayerCount = 0 #to check whether there is a ready player in the game or not
		self.isGameEnd = False # False oyun devam ediyor / True oyun bitince


		self.terminationStr, self.terminationVal = self._parseTermination(self.gameJson["termination"])
		
		for cell in self.gameJson["cells"]:
			parsedCell = self._parseCell(cell)
			self.cells.append(parsedCell)

		self.cellCount = len(self.cells)
		Game.games.append(self)

########################################################################################################
	def _parseTermination(self, termination):

		if(isinstance(self.gameJson["termination"],dict)):
			return list(termination.keys())[0], list(termination.values())[0]

		else:
			return self.gameJson["termination"] , None

	def _parseCell(self, cell):

		action = ""
		artifact = ""

		if "action" in cell: action = cell["action"]
		if "artifact" in cell: artifact = cell["artifact"]

		artifact[]
		
		return Cell(cell["cellno"], cell["description"], action, artifact)

	def _isGameEnded(self, player):

		if(self.terminationStr == "round"): # Cycle is true
			if player.playerCycle >= self.terminationVal:
				self.isGameEnd = 1

		elif(self.terminationStr == "finish"): # Cycle is false
			if player.cellNo == self.cellCount - 1:
				self.isGameEnd = 1

		elif(self.terminationStr == "firstbroke"):
			if player.credit <= 0:
				self.isGameEnd = 1

		elif(self.terminationStr == "firstcollect"):
			if len(player.artifacts) >= self.terminationVal:
				self.isGameEnd = 1


	def _takeAction(self, action, player):

		actionChange = None
		actionKey = list(action.keys())[0]
		actionValue = list(action.values())[0]	

		if(actionKey == "skip"):
			player.skipLeftRound += actionValue
			actionChange = {"skip": actionValue}
		elif(actionKey == "drop"):
			player.credit -= actionValue # check
			actionChange = {"drop": actionValue}
		elif(actionKey == "add"):
			player.credit += actionValue # check
			actionChange = {"add": actionValue}
		elif(actionKey == "pay"):
			self.players[actionValue[0]].credit += actionValue[1]
			player.credit -= actionValue[1] # check
			actionChange = {"pay": actionValue} 

		elif(actionKey == "jump"):
			if(isinstance(actionValue,str)): # Absolute Jump
				#print("absolute jump")
				actionValue = int(actionValue[1:])
				player.cellNo = actionValue
				actionChange = {"jump absolute =": actionValue,"current cell":player.cellNo}
			else:
				player.cellNo += actionValue
				if self.cycles == True:
					if player.cellNo >= self.cellCount:
						player.cellNo %= self.cellCount
						player.playerCycle += 1
					elif player.cellNo <0:
						player.cellNo %= self.cellCount
						player.playerCycle -= 1
				elif player.cellNo >= self.cellCount:
					player.cellNo = self.cellCount-1
				actionChange = {"jump relative": actionValue,"current cell":player.cellNo}
		
		elif(actionKey == "drawcard"):
			pickedCard = random.choice(self.cards)
			pickedCardKey = list(pickedCard.keys())[0]
			pickedCardValue = list(pickedCard.values())[0]
			actionChange = {"draw card with action of": (pickedCardKey,pickedCardValue)}
			drawCardStateChange = self._takeAction(pickedCard, player)
			actionChange.update(drawCardStateChange)
			
		# Check if the game is ended
		self._isGameEnded(player)
		
		return actionChange

########################################################################################################
	def state(self):
		result = {"type":"state","name":self.name, "cell":[],"player":[]}
		for cell in self.cells:
			result["cell"].append({"no":cell.cellno,"description":cell.description})
		for player in self.players:
			result["player"].append({"player":player.nickname,"credit":player.credit,"cycle":player.playerCycle, "cell":player.cellNo, "skip":player.skipLeftRound})
		return result
		
	def join(self,player):
		if isinstance(player, Player) == False:
			return {"type":"exception", "message":"Player is not valid."}
		
		if player in self.players:
			return {"type":"exception", "message":"This player has already joined."}
		elif self.readyPlayerCount >0:
			return {"type":"exception", "message":"The game is about to start, you are late!"}
		
		self.players.append(player)
		return {"type": "success", "message":"Login is successfull"}
		
	def ready(self, player):
		self.readyPlayerCount += 1
		""" if self.readyPlayerCount == len(self.players):
			print("-----------Game is Starting-----------") """
			#self.notifyPlayer()

	@staticmethod
	def listgames():
		stateOfGames = []
		for game in Game.games:
			#print("-------------------------Printing Game MetaData-------------------------")
			#print("Game name: {}, dice: {}, termination: {}, cycles: {}, initialCredit: {}, playerCount: {}"
					#.format(game.name, game.dice, game.terminationStr, game.cycles, game.credit, len(game.players)))
			#print(json.dumps(game.state(), indent = 2))
			stateOfGames.append(game.state())
			
		return stateOfGames

	
	def next(self, player):
		cellActions = ["jump","skip","drop","drawcard", "add","pay"]
		stateChange = {"type":"stateChange","player":player.nickname,"actions":[]}
		
		if(player.skipLeftRound != 0):
			stateChange["actions"].append({"skip": player.skipLeftRound})
			player.skipLeftRound -= 1

		elif(player.currType == "roll"):
			diceRoll = random.randrange(self.dice) + 1
			stateChange["actions"].append({"dice roll ": diceRoll})
			takeActionStateChange = self._takeAction({"jump": diceRoll}, player)
			stateChange["actions"].append(takeActionStateChange)	#TODO: json formatina yakinlastir
			""" if self.isGameEnd  == True:
				return stateChange
				
			#action = self.cells[player.cellNo].action
			#print("Player {} at cellno: {} action is {}".format(player.nickname, tempCell,action))
			#if action == "": #  or action == None or action == ""
				#print("There is no action in the cell -- NEXT")
				#stateChange["actions"].append({"There is no action in the cell:":player.cellNo})
				#return stateChange

			takeActionStateChange = self._takeAction(action, player)
			stateChange["actions"].append(takeActionStateChange)
			if self.isGameEnd  == True:
				return stateChange """

		elif player.currType in cellActions: # User Cell action yapmak istiyor
			stateChange["actions"].append({"user will do cell action ": "test"})
			action = self.cells[player.cellNo].action
			takeActionStateChange = self._takeAction(action, player)
			stateChange["actions"].append(takeActionStateChange)

		""" elif(player.currType == "drawcard"):
			pickedCard = random.choice(self.cards)
			pickedCardKey = list(pickedCard.keys())[0]
			pickedCardValue = list(pickedCard.values())[0]
			stateChange["actions"].append({"draw card with action of": (pickedCardKey,pickedCardValue)})
			takeActionStateChange = self._takeAction(pickedCard, player)
			stateChange["actions"].append(takeActionStateChange)
			if self.isGameEnd  == True:
				return stateChange """

		return stateChange

	""" def notifyPlayer(self):

		if(self.terminationStr == "firstcollect"):
			pass

		playerIndex = 0
		while(self.isGameEnd == False):
			self.currPlayer = self.players[playerIndex]
			if self.currPlayer.currType == None:
				(self.players[playerIndex]).turn("roll")
			if self.currPlayer.currType == "roll":
				
				self.currPlayer.currType = None
			playerIndex += 1

			if playerIndex == len(self.players):
				playerIndex = 0
				self.currRound += 1
				
				#print(json.dumps(self.state(), indent = 4))
				print("-------------------Round: {} ended------------------".format(self.currRound))
				
		print("-------------------Game: ended------------------")
		print(json.dumps(self.state(), indent = 2)) """


	def pick(self, player, pickbool):
		playerCell = self.cells[player.cellNo]
		stateChange = {"player":player.nickname,"cellNo":player.cellNo,"pick":pickbool, "actions":[]}

		if pickbool == True:
			if(playerCell.artifact.owned == True):
				stateChange["actions"].append({"message": "Artifact can't be selected, it is already owned"})
				return

			if(playerCell.artifact.price >= 0 and player.credit >= playerCell.artifact.price): # Owned artifact
				stateChange["actions"].append({"message":"Artifact is owned"})
				playerCell.artifact.owned = True
				player.artifacts.append(playerCell.artifact)
				action = playerCell.artifact.action
				if action == "": # action is None or action == None or 
					print("There is no action in the cell -- PICK")
					stateChange["actions"].append({"message":"There is no action in the artifact"})
				else:
					takeActionStateChange = self._takeAction(player, action)
					stateChange["actions"].append(takeActionStateChange)
					if self.isGameEnd  == True:
						return stateChange
			else:
				stateChange["actions"].append({"message":"Artifact can't be owned"})
				self.cells[player.cellNo].artifact = None #TODO: olmazsa del yapariz			

		else:   # don't change anything in this case
			pass

		print(stateChange)
		#print(json.dumps(stateChange, indent = 2))
