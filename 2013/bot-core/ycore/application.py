#!/opt/python3/python3.2
#-------------------------------------------------------------------------------
# Name:        Bot application
# Purpose:     An application for connecting to a server.
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

from . import client
from . import builder
from .module import core

class BotApplication:

    # Initialize a BotApplication object using a client builder.
    # clientBuilder:    the builder to use
    def __init__(self, client):
        self.modules = []
        self.client = client

    # Enable an event module for the bot.
    # module:           the module to enable and register listeners from
    def enableModule(self, module):
        module.run()
        self.modules.append(module)
        module.setApplication(self)

        for l in module.getListeners():
            self.client.getEventHandler().register(l)

    # Disable an event module for the bot.
    # module:           the module to disable and remove listeners from
    def disableModule(self, module):
        self.modules.remove(module)
        for l in module.getListeners():
            self.client.getEventHandler().unregister(l)

    # Starts the application
    def start(self):
        self.client.start()
