import time
import random
from socket import *
import pickle
from threading import Thread
import os,stat
#import contextlib
#with contextlib.redirect_stdout(None):
#    import pygame
class test:
    def __init__(self, addr, port):
        super().__init__()
        c = socket(AF_INET, SOCK_STREAM)
        c.connect((addr, port))
        print("Connected...")
        cli = Thread(target=self.client, args=(c,))
        subs = Thread(target=self.subscriber, args=(c,))
        cli.start()
        subs.start()

    def subscriber(self,c):
        while True:
            reply = pickle.loads(c.recv(2048))
            if(reply["type"] == "join"):
                print(reply["message"])
            elif(reply["type"] == "exception"):
                print(reply["message"])
            elif(reply["type"] == "create"):
                print(reply["message"])
            elif(reply["type"] == "ready"):
                print(reply["message"])
            elif(reply["type"] == "stateChange"):
                print(reply["message"])
            elif( reply["type"] == "gameState"):
                print(reply["message"])
            elif(reply["type"] == "listGames"):
                print("-------------------------Printing Game MetaData-------------------------")
                print(reply["message"])
            elif (reply["type"] == "turn"):
                if reply["turnType"] == "turnEnd":
                    print("Your turn is over!")
                elif reply["turnType"] == "roll":
                    print("It's you turn! Type \"roll \" for rolling... ")
                elif  reply["turnType"] == "actionOrArtifactPhase":
                    if reply["artifact"] == "empty":
                        print("There is no artifact in your cell...")
                        if reply['action'] == "empty":
                            print("There is nothing to do:( Type \"yield\" for yielding your turn...")
                        else:
                            print(reply["action"])
                            print("type \"action\" for action")
                    else:
                        print(reply["artifact"])
                        if reply['action'] == "empty":
                            print("Do you want to pick this artifact? Type \"yes\" or \"no\"")
                        else:
                            print(reply["action"])
                            print("type \"action\" for action, or your pick choice...")
            
            else:
                print("ELSE PART")
                print(reply)

            if reply == "" :
                break



    def client(self,c):
        # send n random request
        # the connection is kept alive until client closes it.
        #c = socket(AF_INET, SOCK_STREAM)
        #c.connect(('127.0.0.1', port))
        print("Welcome! Please enter your name:)")
        nickname = input()
        c.send(pickle.dumps({"type":"createPlayer",
                        "nickname": nickname}))
        while True:
            #print("please write your command")
            inp =  input()
            if inp == "list":
                c.send(pickle.dumps({"type":"listGames"}))
            elif inp == "join":
                print("please write the id of the game")
                id = input()
                c.send(pickle.dumps({"type":"join",
                                    "id":id}))
            elif inp == "ready":
                c.send(pickle.dumps({"type":"ready"}))
            elif inp == "yield":
                c.send(pickle.dumps({"type":"yield"}))
            elif inp == "action":
                c.send(pickle.dumps({"type":"action"}))
            elif inp == "roll":
                c.send(pickle.dumps({"type":"roll"}))
            elif inp == "yes":
                c.send(pickle.dumps({"type":"pick","val":"true"}))
            elif inp == "no":
                c.send(pickle.dumps({"type":"pick","val":"false"}))
            
            else:
                print("I couldn't understand your command")




        c.close()

variable = test("127.0.0.1",3164)
#clients = [Thread(target = client, args=(5, 20448)) for i in range(5)]
# start clients
#clients[0].start()