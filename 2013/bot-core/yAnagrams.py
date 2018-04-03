#!/opt/python3/bin/python3
from ycore.application import *
from ycore.module.core import *
from ycore.network.network import *
from ycore.network.util import *
from ycore.builder import *
from ycore.client import *

PASSWORD = "comb123"
USERNAME = "ycombinator-3"

def main():
   
    clientBuilder = ChatnetClientBuilder().networkManager(
        ThrottledNetwork(ChatNetworkManager("208.122.59.226", 5005)))
    client = clientBuilder.build()

    bot = BotApplication(client)
    bot.enableModule(CoreModule(USERNAME, PASSWORD))
    bot.start()
    
main()
