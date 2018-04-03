#-------------------------------------------------------------------------------
# Name:        Module
# Purpose:     Extend this class and add to BotApplication to handle events.
#              See example Core module.
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

import abc

class Module:
    def __init__(self):
        self.listeners = []

    def setApplication(self, application):
        self.application = application

    def getApplication(self):
        return self.application

    def getListeners(self):
        return self.listeners

    def addListener(self, listener, eventId):
        self.listeners.append(listener)
        listener.setEventId(eventId)

    @abc.abstractclassmethod
    def run(self):
        pass
