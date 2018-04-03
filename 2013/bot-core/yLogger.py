#!/opt/python3/bin/python3
from ycore.application import *
from ycore.module.core import *
from ycore.network.network import *
from ycore.network.util import *
from ycore.builder import *
from ycore.client import *

from pastebin.message import *
import os

def main():
    logBuilder = ChatnetLogMethodBuilder(1).setMethod(PastebinDateLogMethod())
    logger = logBuilder.addFilter("^MSG:ARENA:Player.+$").build()
    
    clientBuilder = ChatnetClientBuilder().networkManager(
        LogWriter(ThrottledNetwork(ChatNetworkManager("208.122.59.226", 5005)),
                  logger))
    client = clientBuilder.build()

    bot = BotApplication(client)
    bot.enableModule(CoreModule("UB-Isabelle", "ralphtango"))
    bot.start()

class PastebinDateLogMethod(LogMethod):
    uid = 0
    lastDate = datetime.date.today()

    '''def sendPaste(self, filename, content):
        req = PastebinRequestFactory('55cca42d9f3dfdfd824335d3961ee42c', content)
        req.paste_name(filename).paste_expire_date("N")
        req.user_name('hyperspace').password('ralphtango')
        print(req.makeRequest().doRequest().read())'''
    
    def write(self, message):        
        the_date = datetime.date.today()
        path = 'logs/%i/%i/' % (the_date.month, the_date.day)
        try:
            os.makedirs(path, 755)
        except:
            pass
        filename = "%s%i.log" % (path, self.uid)

        with open(filename, 'a') as f:
            for m in message.split('\n'):
                if (not super().matches(m)):
                    f.write(super().parse(m))

        if (os.path.getsize(filename) > 2000000):
            with open(filename, 'r') as f:
                content = ''.join(f.readlines())
            #self.sendPaste(filename, content)
            self.uid += 1
        elif (the_date != self.lastDate):
            with open(filename, 'r') as f:
                content = ''.join(f.readlines())
            #self.sendPaste(filename, content)
            self.uid = 0
            
        self.lastDate = the_date

main()
