from . import network as net
import datetime
import re

class LogWriter(net.ChatNetworkDecorator):
    def __init__(self, networkManager, method):
        self.networkManager = networkManager
        self.method = method    

    def receive(self, messages):
        self.networkManager.receive(messages)        
        self.method.write(messages)

class LogMethod():
    parser = None
    def __init__(self):
        self.pattern = []
    
    def addPattern(self, filterPattern):
        self.pattern.append(filterPattern)
        return self

    def setParser(self, logParser):
        self.parser = logParser

    def parse(self, message):
        if (self.parser):
            return self.parser.parse(message)
        else:
            return message

    def matches(self, message):
        for x in self.pattern:
            if (re.match(x, message)):
                return True
        return False
    
class DateLogMethod(LogMethod):            
    def write(self, message):
        the_date = datetime.date.today()
        with open("logs/%s.log" % (the_date.isoformat()), 'a') as f:
            for m in message.split('\n'):
                if (not super().matches(m)):
                    f.write(super().parse(m))

class ChatnetLogMethodBuilder():
    def __init__(self, logType):
        # Fix magic number...
        if (logType == 1):
            self.logMethod = DateLogMethod()
        self.parser = ArenaMessageParser(PublicMessageParser(None))
        self.parser = FreqMessageParser(self.parser)
        self.parser = ChatMessageParser(EnterMessageParser(self.parser))
        self.parser = LeaveMessageParser(self.parser)
        self.logMethod.setParser(self.parser)

    def parser(self, parser):
        self.parser = parser
        self.logMethod.setParser(self.parser)
        return self

    def setMethod(self, method):
        self.logMethod = method
        self.logMethod.setParser(self.parser)
        return self

    def addFilter(self, theFilter):
        self.logMethod.addPattern(theFilter)
        return self

    def build(self):
        return self.logMethod
            

class LogParser():
    def __init__(self, parser):
        self.parser = parser

    def getNext(self):
        return self.parser

class ArenaMessageParser(LogParser):
    MSG = "^MSG:ARENA:(.+)$"
    
    def __init__(self, parser):
        super().__init__(parser)

    def parse(self, message):
        if (re.match(self.MSG, message)):
            return re.findall(self.MSG, message)[0] + '\n'
        if (self.getNext()):
            return self.getNext().parse(message)
        return ""

class PublicMessageParser(LogParser):
    MSG = "^MSG:PUB(M)?:(.+?):(.+)$"
    
    def __init__(self, parser):
        super().__init__(parser)

    def parse(self, message):
        if (re.match(self.MSG, message)):
            data = re.findall(self.MSG, message)[0]
            player = data[1][0:15]
            message = data[2]
            return ("%15s> %s\n" % (player, message))
        if (self.getNext()):
            return self.getNext().parse(message)
        return ""

class PrivateMessageParser(LogParser):
    MSG = "^MSG:PRIV:(.+?):(.+)$"
    
    def __init__(self, parser):
        super().__init__(parser)

    def parse(self, message):
        if (re.match(self.MSG, message)):
            data = re.findall(self.MSG, message)[0]
            player = data[0][0:14]
            message = data[1]
            return ("P%14s> %s\n" % (player, message))
        if (self.getNext()):
            return self.getNext().parse(message)
        return ""

class FreqMessageParser(LogParser):
    MSG = "^MSG:FREQ:(.+?):(.+)$"

    def __init__(self, parser):
        super().__init__(parser)

    def parse(self, message):
        if (re.match(self.MSG, message)):
            data = re.findall(self.MSG, message)[0]
            player = data[0][0:14]
            message = data[1]
            return ("T%14s> %s\n" % (player, message))
        if (self.getNext()):
            return self.getNext().parse(message)
        return ""

class ChatMessageParser(LogParser):
    MSG = "^MSG:CHAT:(.+)$"

    def __init__(self, parser):
        super().__init__(parser)

    def parse(self, message):
        if (re.match(self.MSG, message)):
            data = re.findall(self.MSG, message)[0]            
            return ("%s\n" % (data))
        if (self.getNext()):
            return self.getNext().parse(message)
        return ""

class EnterMessageParser(LogParser):
    MSG = "^ENTERING:(.+?):.+$"

    def __init__(self, parser):
        super().__init__(parser)

    def parse(self, message):
        if (re.match(self.MSG, message)):
            data = re.findall(self.MSG, message)[0]
            return ("%s has entered the arena.\n" % (data))
        if (self.getNext()):
            return self.getNext().parse(message)
        return ""

class LeaveMessageParser(LogParser):
    MSG = "^LEAVING:(.+)$"

    def __init__(self, parser):
        super().__init__(parser)

    def parse(self, message):
        if (re.match(self.MSG, message)):
            data = re.findall(self.MSG, message)[0]
            return ("%s has left the arena.\n" % (data))
        if (self.getNext()):
            return self.getNext().parse(message)
        return ""
    
