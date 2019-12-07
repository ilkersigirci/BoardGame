import multiGame
import time
import random
from socket import *
from threading import Thread
import os,stat

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
        configList = ["configs/gameFinish.json"]
        gameList = []
        for config in self.configList:
            newgame = multiGame.Game(config)
            gameList.append(newgame)


    def player(self,sock):
        ''' echo uppercase string back in a loop'''
        req = sock.recv(1000)
        req = req.rstrip()
        inp = req.decode().upper().encode() 
        # burada playeri init et
        # while icine if else lerle komutlari al
        while req and req != '':
            # remove trailing newline and blanks
            req = req.rstrip()
            sock.send(req.decode().upper().encode())
            req = sock.recv(1000)
        print(sock.getpeername(), ' closing')
        
    def gameEngine(self,port):
        
        

        s = socket(AF_INET, SOCK_STREAM)
        s.bind(('',port))
        s.listen(1)    # 1 is queue size for "not yet accept()'ed connections"
        try:
            i = 0
            while True:
            #for i in range(5):    # just limit # of accepts for Thread to exit
                ns, peer = s.accept()
                print(peer, "connected")
                # create a thread with new socket
                t = Thread(target = player, args=(ns,))
                t.start()
                # now main thread ready to accept next connection
        finally:
            s.close()

server = Thread(target=gameEngine.gameEngine, args=(20446,))
server.start()
# create 5 clients
