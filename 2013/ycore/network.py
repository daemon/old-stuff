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

    def connect(self):
        self.socket.connect((self.host, self.port))

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

    def start(self):
        threading.Thread(target=self.runReceive).start()
        threading.Thread(target=self.runSend).start()

    def send(self, bytes_):
        self.socket.send(bytes_)

    def ready(self):
        return self.receiveQueue.ready()

    def runReceive(self):
        while(True):
            messages = self.socket.recv(SOCK_RECV).decode(DECODE, FLAG)
            #insert check here for no socket
            splitMsg = messages.split('\n')
            for m in range(0, len(splitMsg) - 1):
                self.receiveQueue.push(splitMsg[m])

            time.sleep(SOCK_SLEEP)

    def close(self):
        self.socket.close()

    def sockSend(self):
        self.lastMessage = self.sendQueue.poll()
        self.send(self.lastMessage)

    def runSend(self):
        # TODO: Implement appropriate hyperspace message delay
        while(True):
            if (self.sendQueue.ready()):
                self.sockSend()

class ChatNetworkManager(NetworkManager):
    def __init__(self, host, port):
        super().__init__(host, port)

    def sendLogin(self, name, password, isBlocking=False):
        self.push(msg.LoginMessage(name, password).toString(), isBlocking)

    def sendGoArena(self, arena, isBlocking=False):
        self.push(msg.GoMessage(arena).toString(), isBlocking)

    def sendPrivateMessage(self, player, message, isBlocking=False):
        self.push(msg.PrivateMessage(player, message).toString(), isBlocking)

'''
# fix decorator
class ChatNetworkDecorator(ChatNetworkManager):
    def __init__(self, chatNetwork):
        ChatNetworkManager.__init__(self, chatNetwork.host, chatNetwork.port)
        self.networkManager = chatNetwork

    def '''
        
class ThrottledNetwork(ChatNetworkManager):
    burst = 0
    sock_sleep = 0.1

    def __init__(self, networkManager):
        super().__init__(networkManager.host,
            networkManager.port)

    def send(self, bytes_):
        super().send(bytes_)
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
