#-------------------------------------------------------------------------------
# Name:        Listener
# Purpose:     Listens to events: every module needs one of these.
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

from abc import *

class Listener:
    def __init__(self):
        pass

    def setEventId(self, eventId):
        self.eventId = eventId

    def getEventId(self):
        return self.eventId

    @abstractclassmethod
    def perform(self, event, handler, queue):
        pass
