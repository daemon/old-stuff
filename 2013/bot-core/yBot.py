#!/opt/python3/bin/python3
from ycore.application import *
from ycore.module.core2quad import *
from ycore.network.network import *
from ycore.builder import *
from ycore.client import *

from coinscore import *

def main():
    clientBuilder = ChatnetClientBuilder().networkManager(
        ThrottledNetwork(ChatNetworkManager("142.4.200.80", 5005)))
    client = clientBuilder.build()

    bot = BotApplication(client)
    bot.enableModule(CoreModule("UB-Bot-Casino", "ralphtango"))
    bot.enableModule(GamblingModule())
    bot.start()

main()
