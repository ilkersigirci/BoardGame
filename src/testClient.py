import time
import random
from socket import *
from threading import Thread
import os,stat

def client(n, port):
    # send n random request
    # the connection is kept alive until client closes it.
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('127.0.0.1', port))
    print("Connected...")
    while True:
        print("please write your command")
        inp =  input()
        c.send(inp.encode())
        if inp == "" :
            break
        reply = c.recv(1024)
        reply = reply.decode()
        print(reply)
        
    c.close()


clients = [Thread(target = client, args=(5, 20446)) for i in range(5)]
# start clients
clients[0].start()