#-------------------------------------------------------------------------------
# Name:        Event Factory
# Purpose:     Contains factories for creating appropriate events.
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

from . import event as evt
import re
import abc

LOGINOK = "LOGINOK"
LOGINBAD = "LOGINBAD"

class EventFactory():

    factory = None
    prefix = None
    
    @staticmethod
    def getInstance():
        pass

    def setMessage(self, message):
        self.message = message
        return self

    def getMessage(self):
        return self.message

    @abc.abstractclassmethod
    def makeEvent(self):
        pass

    @abc.abstractclassmethod
    def handles(self, message):
        pass
    

class LoginEventFactory(EventFactory):

    prefix = "LOG"

    @staticmethod
    def getInstance():
        if (LoginEventFactory.factory is None):
            LoginEventFactory.factory = LoginEventFactory()
        return LoginEventFactory.factory

    def makeEvent(self):
        messages = self.message.split(':')
        success = messages[0]

        if (success == LOGINOK):
            event = evt.LoginEvent(messages[1], True)
        else:
            event = evt.LoginEvent(None, False)
        return event

    def handles(self, message):
        return message.startswith(self.prefix)

class MessageEventFactory(EventFactory):

    prefix = "MS"

    @staticmethod
    def getInstance():
        if (MessageEventFactory.factory is None):
            MessageEventFactory.factory = MessageEventFactory()
        return MessageEventFactory.factory

    def makeEvent(self):
        typeM = Messages.getMessageType(self.message)
        event = None
        parsedMessage = self.message.split(":")

        if (typeM == Messages.MSG_TYPE_PRIV):
            event = evt.MessagePrivateEvent(parsedMessage[2], parsedMessage[3])
        elif (typeM == Messages.MSG_TYPE_CMD):
            f = re.findall(Messages.MSG_PRIV_CMD, self.message)
            event = evt.MessagePrivateCommandEvent(f[0][0], f[0][3].lower(), f[0][4].split(" "))
        elif (typeM == Messages.MSG_TYPE_ARENA):
            event = evt.MessageArenaEvent(self.message)
        return event

    def handles(self, message):
        return message.startswith(self.prefix)

class Messages:
    MSG_PRIV = "MSG:PRIV"
    MSG_ARENA = "MSG:ARENA"
    MSG_PRIV_CMD = "^MSG:PRIV:(.+?):( *?|)!( *?)([A-z]+)( +.*)?$"
    MSG_TYPE_UNKNOWN, MSG_TYPE_PRIV, MSG_TYPE_CMD, MSG_TYPE_ARENA = range(4)

    @staticmethod
    def getMessageType(message):
        typeM = Messages.MSG_TYPE_UNKNOWN
        if (message.startswith(Messages.MSG_PRIV)):
            if (re.findall(Messages.MSG_PRIV_CMD, message)):
                typeM = Messages.MSG_TYPE_CMD
            else:
                typeM = Messages.MSG_TYPE_PRIV
        elif (message.startswith(Messages.MSG_ARENA)):
              typeM = Messages.MSG_TYPE_ARENA
        return typeM
