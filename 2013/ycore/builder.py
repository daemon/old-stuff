#-------------------------------------------------------------------------------
# Name:        Builder
# Purpose:     Contains client builders for the creation of a desired client
#              connection.
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

from . import client
from . import eventhandler
from . import eventparser
from . import network
from . import eventfactory as fact

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

    def build(self):
        return self.client
