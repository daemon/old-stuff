#-------------------------------------------------------------------------------
# Name:        Event
# Purpose:     An interface for an event handling model.
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

import time

class Event:
    def __init__(self):
        self.time = time.time()

    def getTime(self):
        return self.time

    def getDeltaFromCurrent(self):
        return time.time() - self.time

    @staticmethod
    def getId():
        return -1

class ChatEvent(Event):
    def __init__(self):
        Event.__init__(self)

class LoginEvent(ChatEvent):
    def __init__(self, player, isSuccess):
        ChatEvent.__init__(self)
        self.player = player
        self.isSuccess = isSuccess

    def getPlayer(self):
        return self.player

    def isSuccessful(self):
        return self.isSuccess

    @staticmethod
    def getId():
        return Events.EVT_LOGIN

class PlayerEvent(ChatEvent):
    def __init__(self, player):
        ChatEvent.__init__(self)
        self.player = player

    def getPlayer(self):
        return self.player

class ClientConnectEvent(ChatEvent):
    def __init__(self):
        ChatEvent.__init__(self)

    @staticmethod
    def getId():
        return Events.EVT_CLIENT_CONNECT

class MessagePrivateEvent(PlayerEvent):
    def __init__(self, player, message):
        PlayerEvent.__init__(self, player)
        self.message = message

    def getMessage():
        return self.message

    @staticmethod
    def getId():
        return Events.EVT_MSG_PRIVATE

class MessagePublicEvent(PlayerEvent):
    def __init__(self, player, message):
        PlayerEvent.__init__(self, player)
        self.message = message

    def getMessage():
        return self.message

    @staticmethod
    def getId():
        return Events.EVT_MSG_PUBLIC

class MessagePrivateCommandEvent(PlayerEvent):
    def __init__(self, player, command, args):
        PlayerEvent.__init__(self, player)
        self.command = command
        self.args = args

    def getCommand(self):
        return self.command

    def getArgs(self):
        return self.args

    @staticmethod
    def getId():
        return Events.EVT_MSG_PRIVATE_CMD

class MessageArenaEvent(Event):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def getMessage(self):
        return self.message

    @staticmethod
    def getId():
        return Events.EVT_MSG_ARENA

class Events:
    EVT_MSG_PRIVATE_CMD, EVT_MSG_PUBLIC, EVT_MSG_PRIVATE, EVT_CLIENT_CONNECT, EVT_LOGIN, EVT_MSG_ARENA = range(6)
