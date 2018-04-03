#-------------------------------------------------------------------------------
# Name:        Event handler
# Purpose:     Dispatches events using two threads. Modules also register their
#              events on this interface.
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

import threading
import time

class EventHandler():
    def __init__(self, queue):
        self.eventsToHandlers = {}
        self.callQueue = []
        self.queue = queue
        threading.Thread(target=self.run).start()
        threading.Thread(target=self.run).start()
        #could optimize busy waiting

    def run(self):
        while(True):
            if (self.callQueue):
                event = self.callQueue.pop(0)
                if (self.eventsToHandlers.get(event.getId())):
                    for listener in self.eventsToHandlers.get(event.getId()):
                        listener.perform(event, self.queue, self)
            time.sleep(0.1)

    def handle(self, event):
        if (event):
            self.callQueue.append(event)

    def register(self, listener):
        eventId = listener.getEventId()
        if (eventId in self.eventsToHandlers.keys()):
            self.eventsToHandlers.get(eventId).append(listener)
        else:
            self.eventsToHandlers[listener.getEventId()] = [listener,]

# TODO: unregister(self, listener)
