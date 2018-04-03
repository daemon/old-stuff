#-------------------------------------------------------------------------------
# Name:        Builder
# Purpose:     Contains client builders for the creation of a desired client
#              connection.
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

from . import client
from .event import eventhandler
from .event import eventparser
from .network import network
from .event import eventfactory as fact

class ChatnetClientBuilder:
    def __init__(self):
        self.client = client.Client()
        self.parser = eventparser.EventParser()
        self.client.setEventParser(self.parser)
        self.parser.register(fact.LoginEventFactory.getInstance())
        self.parser.register(fact.MessageEventFactory.getInstance())

    def networkManager(self, manager):
        self.client.setNetworkManager(manager)
        self.client.setEventHandler(eventhandler.EventHandler(self.client.getQueue()))
        return self

    def eventParser(self, evtParser):
        self.parser = evtParser
        self.client.setEventParser(evtParser)
        return self

    def eventParserFlag(self, flag):
        self.parser = eventparser.EventParser()
        self.client.setEventParser(self.parser)
        if (flag & Flags.PSR_LOGIN):
            self.parser.register(fact.LoginEventFactory.getInstance())
        if (flag & Flags.PSR_MESSAGE):
            self.parser.register(fact.MessageEventFactory.getInstance())
        return self    

    def build(self):
        return self.client

class Flags:
    PSR_LOGIN = 0x1
    PSR_MESSAGE = 0x10
