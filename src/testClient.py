import time
import random
from socket import *
from threading import Thread
import os,stat

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
            reply = c.recv(1024)
            reply = reply.decode()
            print(reply)
            if reply == "" :
                break



    def client(self,c):
        # send n random request
        # the connection is kept alive until client closes it.
        #c = socket(AF_INET, SOCK_STREAM)
        #c.connect(('127.0.0.1', port))
        
        while True:
            print("please write your command")
            inp =  input()
            c.send(inp.encode())
            if inp == "" :
                break


        c.close()

variable = test("127.0.0.1",2337)
#clients = [Thread(target = client, args=(5, 20448)) for i in range(5)]
# start clients
#clients[0].start()