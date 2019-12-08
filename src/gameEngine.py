from Game import Game
import time
import random
from socket import *
from threading import Thread
import os,stat
from utils import *


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





class gameEngine:
    
    def __init__(self):
        self.networkObservers = OSubject()
        self.configList = ["configs/gameFinish.json"]
        gameList = []
        for config in self.configList:
            newgame = Game(config)
            gameList.append(newgame)
        self.obs = OSubject()


    def agent(self,clientCon, id):
        ''' echo uppercase string back in a loop'''
        socket = Network()
        socket.initCon(clientCon)
        requestOfClient = socket.receiveData()

        # burada playeri init et
        # while icine if else lerle komutlari al
        while requestOfClient and requestOfClient != '':
            # remove trailing newline and blanks
            self.networkObservers.notifyOne(id)
            requestOfClient = socket.receiveData()
        print(socket.clientAddr, ' closing')
        
    def server(self,port = 2331):
        socket = Network(port,"127.0.0.1") # defin sonrasina tasimak denenebilir
        socket.initConnectionForClients()
        try:
            while True:
            #for i in range(5):    # just limit # of accepts for Thread to exit
                clientCon = socket.acceptConnectionFromClient()
                i = self.networkObservers.register(socket) # burada hep ayni objeyi mi ekler primitive nesne olmadigi icin
                #TODO: eger ustteki satir calismazsa direk connectionu versek de olur agenta
                # simdilik daha temiz kod olsun diye network nesneleri ile devam ediyorum ama zorunluluk yok
                # create a thread with new socket
                t = Thread(target = gameEngine.agent, args=(self,clientCon,i,))
                t.start()
                # now main thread ready to accept next connection
        finally:

            socket.closeConnection()
            #socket.close()
game = gameEngine()
server = Thread(target=gameEngine.server, args=(game,2337,))
server.start()
# create 5 clients
