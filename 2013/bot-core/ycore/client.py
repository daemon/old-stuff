#-------------------------------------------------------------------------------
# Name:        Client
#
# Author:      tetrisd
#
#-------------------------------------------------------------------------------

from .event import event as evt
from .network import network as net
import time

class Client:
    # Makes a new client. DO NOT use constructor; find a suitable builder
    # networkManager    : the network manager to use
    # eventParser       : the event parser to use
    # eventHandler      : the event dispatcher to use
    def __init__(self, networkManager, eventParser, eventHandler):
        self.networkManager = networkManager
        self.eventParser = eventParser
        self.eventHandler = eventHandler

    def __init__(self):
        pass

    def setNetworkManager(self, manager):
        self.networkManager = manager

    def setEventParser(self, manager):
        self.eventParser = manager

    def setEventHandler(self, manager):
        self.eventHandler = manager

    def getQueue(self):
        return self.networkManager

    def getEventHandler(self):
        return self.eventHandler

    # Run main thread of the bot. This thread reads from the network, parses
    # events, and dispatches events.
    def start(self):
        self.networkManager.connect()
        net.NetworkManager.beginThreads(self.networkManager)
        clientEvent = evt.ClientConnectEvent()
        self.eventHandler.handle(clientEvent)
        
        while(True):
            # while it has messages
            while (self.networkManager.ready()):
                # get first message and handle
                rawMessage = self.networkManager.poll()
                print(rawMessage)
                events = self.eventParser.parse(rawMessage)
                if (events):
                    list(map(self.eventHandler.handle, events))

            if (not self.networkManager.isConnected()):                
                try:
                    self.networkmanager.close()
                except:
                    pass
                time.sleep(5)
                
                flag = False
                while not flag:
                    try:
                        self.networkManager.reconnect()
                        net.NetworkManager.beginThreads(self.networkManager)
                        flag = True
                    except:
                        time.sleep(5)
                        
                clientEvent = evt.ClientConnectEvent()
                self.eventHandler.handle(clientEvent)
                
