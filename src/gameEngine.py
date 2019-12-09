from Game import Game
from Player import Player
import time
import random
from socket import *
from threading import *
import os,stat
from utils import *
import pickle

'''
    gameList = []
    host = "127.0.0.1"
    port = "2331"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self, configFile):
        configList = []
        with open(configFile,"r") as file:
            line = file.readline()
            while line:
                configList.append(line)
                line = file.readline()
        
        for config in self.configList:
            newgame = Game(config)
            gameList.append(newgame)
'''


class GameThread(Thread):
    def __init__(self, game):
        self.currentGame = game
        self.readyCond = game.readyCond
        self.turnCond = game.turnCond
        self.mutex = game.mutex
        self.mutex2 = game.mutex2
        self.isGameEnd = False
        self.networkObservers = OSubject()
        super(GameThread, self).__init__()
        
    
    def notifyUser(self, message):
        data = pickle.dumps(message)
        playerId = self.currentGame.currPlayer.id
        self.networkObservers.notifyOne(playerId, data)
    
    def notifyAllUsers(self, message):
        data = pickle.dumps(message)
        for player in self.currentGame.players:
            try:
                self.networkObservers.notifyOne(player.id, data)
            except:
                pass

    
    
    def run(self):
        with self.readyCond:
            while len(self.currentGame.players) < 2 or len(self.currentGame.players) == 0 or len(self.currentGame.players) != self.currentGame.readyPlayerCount:
                print("in while")
                print("allPlayer",len(self.currentGame.players))
                print("readyplayers",self.currentGame.readyPlayerCount)
                self.readyCond.wait()
        message = {"type": "gameState","message": "-----------Game is Starting-----------"}
        self.notifyAllUsers(message)
        # game is starting
        #print(len(self.currentGame.players))
        #print(self.currentGame.readyPlayerCount)
        playerIndex = 0
        while(self.currentGame.isGameEnd == False):
            self.currentGame.currPlayer = self.currentGame.players[playerIndex]
            #print("player starting: ",self.currentGame.currPlayer.id)
            if self.currentGame.currPlayer.turnPhase == 0:
                self.notifyUser({"type": "turn","turnType":"roll"})
            with self.mutex2:
                while self.currentGame.currPlayer.turnPhase == 0:
                    self.turnCond.wait()
            
            result = {"type":"turn","turnType":"actionOrArtifactPhase", "artifact":"empty","action":"empty"}
            
            currCell = self.currentGame.cells[self.currentGame.currPlayer.cellNo]
            
            if currCell.artifact != "":
                result["artifact"] = currCell.artifact
            if currCell.action != "":
                result["action"] = currCell.action
            #if currCell.artifact != "" and currCell.action != "":
            #    self.currentGame.currPlayer.turnPhase += 1
            self.notifyUser(result)
            with self.mutex2:
                while self.currentGame.currPlayer.turnPhase == 1:
                    self.turnCond.wait()
                self.currentGame.currPlayer.currType = None
            self.currentGame.currPlayer.turnPhase = 0
            self.notifyUser({"type": "turn","turnType":"turnEnd"})
            playerIndex += 1

            if playerIndex == len(self.currentGame.players):
                #print(.format(reply["val"]))
                message = {"type": "gameState", "message": "-------------------Round:" + str(self.currentGame.currRound) + "ended------------------"}
                self.notifyAllUsers(message)

                if isinstance(self.currentGame.cycles , int):
                    for player in self.currentGame.players:
                        player.credit += self.currentGame.cycles

                playerIndex = 0
                self.currentGame.currRound += 1
        
        message = {"type": "gameState", "message": "Game is ended"}
        self.notifyAllUsers(message)
				


class Agent(Thread):
    def __init__(self,clientCon, playerId, gameList,lock):
        ''' echo uppercase string back in a loop'''
        self.clientCon = clientCon
        self.playerId = playerId
        self.readyCond = None
        self.turnCond = None
        self.currentPlayer = None
        self.currentGame = None
        self.networkObservers = OSubject()
        self.gameList =  gameList
        self.lock = lock
        super(Agent, self).__init__()

    def notifyUser(self, message):
        data = pickle.dumps(message)
        self.networkObservers.notifyOne(self.playerId, data)
    
    def notifyAllUsers(self, message):
        data = pickle.dumps(message)
        self.networkObservers.notifyAll(data)

    def createPlayer(self,request):
        #print("createPlayer PlayerID", self.playerId)
        self.currentPlayer = Player(self.playerId,request["nickname"])
        #print("currentPlayer PlayerID", self.currentPlayer.id)
        message = {"type":"create","message": "The player "+ request["nickname"] +" has been created!"}
        self.notifyUser(message)

    def join(self, request):
        with self.lock:
            try:
                message = self.currentPlayer.join(self.gameList[int(request["id"])])
                if message["type"] == "exception":
                    self.notifyUser(message)
                    return
            except Exception as e:
                print(e)
                print("User can't enter the game")

            self.currentGame = self.gameList[int(request["id"])]
            message = {"type":"join", "message": "The player "+ self.currentPlayer.nickname + 
                        " joined the game " + self.currentGame.name}
            self.readyCond = self.currentGame.readyCond
            self.turnCond = self.currentGame.turnCond
            self.notifyUser(message)
        
    def ready(self):
        with self.lock:
            self.currentPlayer.ready()
            message = {"type":"ready", "message": "The player "+ self.currentPlayer.nickname + 
                        " is ready for the game " + self.currentGame.name}   
            self.notifyUser(message)

    def yielding(self):
        self.currentPlayer.turnPhase += 1

    def listGames(self):
        result = Game.listgames()
        message = {"type": "listGames", "message":result}
        self.notifyUser(message)

    def turn(self, request):
        if request["type"] != "pick":
            result = self.currentPlayer.turn(request["type"])          
        else:
            result = self.currentPlayer.turn(request["val"]) 
        self.notifyUser({"type":"stateChange", "message":result})
        
    def run(self):
        try:
            while True:
                request = pickle.loads(self.clientCon.recv(2048))
                print(request)
                if request["type"] == "createPlayer":
                    self.createPlayer(request)
                elif request["type"] == "listGames":
                    self.listGames()
                elif request["type"] == "join":
                    self.join(request)
                elif request["type"] == "yield":
                    self.yielding()
                    with self.turnCond:
                            self.turnCond.notify()
                elif request["type"] == "ready":
                    self.ready()
                    with self.readyCond:
                        self.readyCond.notify()
                elif request["type"] == "action" or request["type"] == "roll"  or request["type"] == "pick":
                    if self.currentPlayer.id == self.currentGame.currPlayer.id:
                        self.turn(request)
                        with self.turnCond:
                            self.turnCond.notify()
                    else:
                        self.notifyUser({"type":"exception","message":"It's not your turn!"})
                        


        except KeyboardInterrupt:
            print("Connection is force closing")

        finally:
            print("Connection is closing")




class gameEngine:
    
    def __init__(self):
        self.networkObservers = OSubject()
        self.configList = ["configs/gameArt.json","configs/gameFinish.json"]
        self.gameList = []
        self.lock = Lock()
        for config in self.configList:
            newgame = Game(config)
            newGameThread = GameThread(newgame)
            newGameThread.start()
            self.gameList.append(newgame)

    
        
    def server(self,port = 2331):
        s = socket.socket(AF_INET, SOCK_STREAM)
        s.bind(('',port))
        s.listen(4)    # 4 is queue size for "not yet accept()'ed connections"
        try:
            while True:
                ns, peer = s.accept()
                playerId = self.networkObservers.register(ns)
                # create a thread with new socket
                newAgent = Agent(ns,playerId,self.gameList,self.lock)
                newAgent.start()
                # now main thread ready to accept next connection
        except:
            s.close()
        finally:
            s.close()

game = gameEngine()
server = Thread(target=gameEngine.server, args=(game,3164,))
server.start()
# create 5 clients
