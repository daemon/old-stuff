#-------------------------------------------------------------------------------
# Name:        Event parser
# Purpose:     Creates events from the input.
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

import abc

class EventParser():
    def __init__(self):
        self.factories = []

    def register(self, factory):
        self.factories.append(factory)

    def parse(self, message):
        factory = self.getFactory(message)
        if (factory is None):
            return None
        else:
            return factory.makeEvent()

    def getFactory(self, message):
        factory = None
        for f in self.factories:
            if (f.handles(message)):
                factory = f.setMessage(message)
                break        

        return factory

##        elif (message.startswith("PL")):
##            factory = PlayerEventFactory(message)
##        elif (message.startswith("EN")):
##            factory = PlayerEventFactory(message)
##        elif (message.startswith("LE")):
##            factory = PlayerEventFactory(message)
##        elif (message.startswith("SH")):
##            factory = PlayerEventFactory(message)
##        elif (message.startswith("KI")):
##            factory = KillEventFactory(message)
