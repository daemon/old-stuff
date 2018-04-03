#-------------------------------------------------------------------------------
# Name:        Network
# Purpose:     Network connection object that intuitively extends a queue. Poll 
#              polls the receiving queue; push pushes to the send queue.
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

import socket
import threading
import time
from . import message as msg
import re

# remove globals

DECODE = "utf-8"
FLAG = "ignore"
SOCK_RECV = 4096
SOCK_SLEEP = 0.1

class Queue():
    def __init__(self):
        self.messages = []

    def push(self, message):
        item = QueueItem(message)
        self.messages.append(item)
        return item

    def poll(self):
        message = self.messages.pop(0)
        message.notify()
        return message.getItem()

    def ready(self):
        return self.messages

class QueueItem():
    def __init__(self, item):
        self.item = item
        self.notifed = False

    def notify(self):
        self.notifed = True

    def isNotified(self):
        return self.notifed

    def getItem(self):
        return self.item
# TODO: Make blocking
# PERHAPS make interface?
class NetworkManager(Queue):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sendQueue = Queue()
        self.receiveQueue = Queue()
        self.connected = True

    def connect(self):
        self.socket.connect((self.host, self.port))
        self.connected = True

    def reconnect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sendQueue = Queue()
        self.receiveQueue = Queue()
        self.connect()

    def getSocket(self):
        return self.socket

    def getSendQueue(self):
        return self.sendQueue

    def poll(self):
        return self.receiveQueue.poll()

    def push(self, string, isBlocking=False, timeout=60):
        notification = self.sendQueue.push(string.encode())
        if (isBlocking):
            time_t = time.time()
            while(not notification.isNotified()):
                time.sleep(0.1)
                if (time.time() - time_t > timeout):
                    return #perhaps raise a timeout exception?      

    def send(self, bytes_):
        self.socket.send(bytes_)

    def isConnected(self):
        return self.connected

    def ready(self):
        return self.receiveQueue.ready()

    def receive(self, messages):                                   
        splitMsg = messages.split('\n')
        if (messages == ""):
            self.connected = False
            return
        for m in range(0, len(splitMsg) - 1):
            self.receiveQueue.push(splitMsg[m])

        time.sleep(SOCK_SLEEP)

    def close(self):
        self.socket.close()        

    @staticmethod
    def beginThreads(manager):
        threading.Thread(target=NetworkReceiveThread(manager).run).start()
        threading.Thread(target=NetworkSendThread(manager).run).start()
        

class NetworkSendThread:
    def __init__(self, manager):
        self.manager = manager

    def run(self):
        while(self.manager.isConnected()):
            if (self.manager.getSendQueue().ready()):                
                self.manager.send(self.manager.getSendQueue().poll())

class NetworkReceiveThread:
    def __init__(self, manager):
        self.manager = manager

    def run(self):
        while(self.manager.isConnected()):
            messages = self.manager.getSocket().recv(SOCK_RECV).decode(DECODE, FLAG)
            self.manager.receive(messages)

class ChatNetworkManager(NetworkManager):
    def __init__(self, host, port):
        super().__init__(host, port)

    def sendLogin(self, name, password, isBlocking=False):
        self.push(msg.LoginMessage(name, password).toString(), isBlocking)

    def sendGoArena(self, arena, isBlocking=False):
        self.push(msg.GoMessage(arena).toString(), isBlocking)

    def sendPrivateMessage(self, player, message, isBlocking=False):
        self.push(msg.PrivateMessage(player, message).toString(), isBlocking)

    def sendPrivateCommand(self, player, command, isBlocking=False):
        self.push(msg.PrivateCommandMessage(player, command).toString(),
            isBlocking)

    def sendChat(self, message, isBlocking=False):
        self.push(msg.ChatMessage(message).toString(), isBlocking)

    def sendCommand(self, command, isBlocking=False):
        self.push(msg.CommandMessage(command).toString(), isBlocking)
        
class ChatNetworkDecorator(ChatNetworkManager):
    def __init__(self, chatNetwork):        
        self.networkManager = chatNetwork

    def getSendQueue(self):
        return self.networkManager.getSendQueue()

    def isConnected(self):
        return self.networkManager.isConnected()

    def send(self, bytes_):
        self.networkManager.send(bytes_)

    def getSocket(self):
        return self.networkManager.getSocket()

    def receive(self, messages):
        self.networkManager.receive(messages)

    def reconnect(self):
        self.networkManager.reconnect()

    def connect(self):
        self.networkManager.connect()

    def poll(self):
        return self.networkManager.poll()

    def push(self, string, isBlocking=False, timeout=60):
        self.networkManager.push(string, isBlocking, timeout)

    def ready(self):
        return self.networkManager.ready()

    def close(self):
        self.networkManager.close()

        
class ThrottledNetwork(ChatNetworkDecorator):
    burst = 0
    sock_sleep = 0.1

    def __init__(self, networkManager):
        self.networkManager = networkManager

    def send(self, bytes_):
        self.networkManager.send(bytes_)
        self.time_t = time.time()
        if (self.burst < 3):
            self.burst += 1
            self.sock_sleep += 0.5
            self.time_t = time.time()
        if (time.time() - self.time_t > 8):
            self.sock_sleep = 0.1
            self.burst = 0
            self.time_t = time.time()
        time.sleep(self.sock_sleep)        
