#-------------------------------------------------------------------------------
# Name:        Core
# Purpose:     Basic, required listeners for SSCE Hyperspace
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

from . import module
from ..event import event
from . import listener

class CoreModule(module.Module):

    NAME = ""
    PASSWORD = ""
    ARENA = "0"

    def __init__(self, name, password):
        super().__init__()
        self.NAME = name
        self.PASSWORD = password

    #TODO: Make ID constants
    def run(self):
        self.addListener(BotLoginListener(self.NAME, self.PASSWORD),
            event.Events.EVT_CLIENT_CONNECT)
        self.addListener(LoginOkListener(self.ARENA),
            event.Events.EVT_LOGIN)
        self.addListener(BasicCommandListener("nn"),
            event.Events.EVT_MSG_PRIVATE_CMD)

class BotLoginListener(listener.Listener):
    def __init__(self, name, password):
        super().__init__()
        self.name = name
        self.password = password

    def perform(self, connectEvent, queue, eventHandler):
        queue.sendLogin(self.name, self.password)

class LoginOkListener(listener.Listener):
    def __init__(self, arena):
        super().__init__()
        self.arena = arena

    def perform(self, loginEvent, queue, eventHandler):
        if (loginEvent.isSuccessful()):            
            queue.sendGoArena(self.arena, True)
            queue.sendCommand("?chat=jowie")

class BasicCommandListener(listener.Listener):
    HELP_CMD = "help"
    HELP_MSG = "!about, !help, !owner, !start, !stop"    
    
    OWNER_CMD = "owner"
    OWNER_MSG = "Owner: %s"
    SHUTDOWN_CMD = "shutdown"
    MODS = ['dr brain', 'd1st0rt', 'swift warrior', 'masaru', 'spidernl',
        'rivel', 'noldec', 'psythe', 'ceiu', 'sri']

    def __init__(self, owner):
        super().__init__()
        self.OWNER_MSG = self.OWNER_MSG % owner
        self.MODS.append(owner.lower())

    def perform(self, commandEvent, queue, eventHandler):
        if (commandEvent.getCommand() == self.HELP_CMD):
            queue.sendPrivateMessage(commandEvent.getPlayer(), self.HELP_MSG)
        elif (commandEvent.getCommand() == self.SHUTDOWN_CMD):
            if (commandEvent.getPlayer().lower() in self.MODS):
                queue.sendPrivateMessage(commandEvent.getPlayer(),
                    "Shutting down gracefully...", True)
                queue.close()
        elif (commandEvent.getCommand() == self.OWNER_CMD):
            queue.sendPrivateMessage(commandEvent.getPlayer(), self.OWNER_MSG)
