from ..Game import Game
import time
import random
from socket import *
from threading import Thread
import os,stat
def player(sock):
    ''' echo uppercase string back in a loop'''
    req = sock.recv(1000)
    while req and req != '':
        # remove trailing newline and blanks
        req = req.rstrip()
        sock.send(req.decode().upper().encode())
        req = sock.recv(1000)
    print(sock.getpeername(), ' closing')


        
def gameEngine(port):
    newgame = Game.Game("../configs/gameFinish.json")
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('',port))
    s.listen(1)    # 1 is queue size for "not yet accept()'ed connections"
    try:
        #while True:
        for i in range(5):    # just limit # of accepts for Thread to exit
            ns, peer = s.accept()
            print(peer, "connected")
            # create a thread with new socket
            t = Thread(target = player, args=(ns,))
            t.start()
            # now main thread ready to accept next connection
    finally:
        s.close()

server = Thread(target=gameEngine, args=(20446,))
server.start()
# create 5 clients
