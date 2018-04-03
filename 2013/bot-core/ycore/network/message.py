#-------------------------------------------------------------------------------
# Name:        Message
# Purpose:     Contains ChatNet messages to send to the server.
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

class Message:
    def toString(self):
        return self.final

    def setFinalMessage(self, final):
        self.final = final

class LoginMessage(Message):
    STR_PREPEND = "LOGIN:0:"
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.setFinalMessage("%s%s:%s\n"
            % (self.STR_PREPEND, name, password))

class GoMessage(Message):
    STR_PREPEND = "GO:"
    def __init__(self, arena):
        self.arena = arena
        self.setFinalMessage("%s%s\n" % (self.STR_PREPEND, arena))

class PrivateMessage(Message):
    STR_PREPEND = "SEND:PRIV:"
    def __init__(self, player, message):
        self.player = player
        self.message = message
        self.setFinalMessage("%s%s:%s\n" %
            (self.STR_PREPEND, player, message))

class CommandMessage(Message):
    STR_PREPEND = "SEND:CMD:"
    def __init__(self, command):
        self.command = command
        self.setFinalMessage("%s%s\n" % (self.STR_PREPEND, command))

class ChatMessage(Message):
    STR_PREPEND = "SEND:CHAT:1;"
    def __init__(self, message):
        self.message = message
        self.setFinalMessage("%s%s\n" % (self.STR_PREPEND, message))

class PrivateCommandMessage(Message):
    STR_PREPEND = "SEND:PRIVCMD"
    def __init__(self, player, command):
        self.player = player
        self.command = command
        self.setFinalMessage("%s:%s:%s\n" % (self.STR_PREPEND, player, command))
