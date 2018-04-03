#-------------------------------------------------------------------------------
# Name:        Client
#
# Author:      tetrisd
#
#-------------------------------------------------------------------------------

from . import event as evt
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
        self.networkManager.start()
        clientEvent = evt.ClientConnectEvent()
        mean = 0
        times = 0

        self.eventHandler.handle(clientEvent)
        while(True):
            # while it has messages
            while (self.networkManager.ready()):

                # get first message and handle
                rawMessage = self.networkManager.poll()
                print(rawMessage)
                
                t1 = time.clock()  
                event = self.eventParser.parse(rawMessage)
                if not (event is None):
                    self.eventHandler.handle(event)
                t2 = time.clock()
                times += 1
                print((mean + (t2-t1) * 1000000) / times)
            time.sleep(0.1)
