#-------------------------------------------------------------------------------
# Name:        Event parser
# Purpose:     Creates events from the input.
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

import abc
from . import eventfactory as fact

class EventParser():
    def __init__(self):
        self.factories = []

    def register(self, factory):
        self.factories.append(factory)

    def parse(self, message):
        factories = self.getFactories(message)
        if (factories):
            return [f.makeEvent() for f in factories]
        else:
            return None

    def getFactories(self, message):
        factories = []
        for f in self.factories:
            if (f.handles(message)):
                factories.append(f.setMessage(message))

        return factories
