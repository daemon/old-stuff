#-------------------------------------------------------------------------------
# Name:        coinscore
# Purpose:     A module for UB-Coins, a simple gambling bot. Players bet for
#              a 50% chance to double, 50% for nothing.
#
# Rigs:        - Auto-lose if no cash
#              - Chances decrease for players as they win
#              - Chances increase for players as they lose
#              - Chances increase on low numbers if the bot isn't meeting its
#                50% on announces. The inverse is true as well.
#
# Author:      tetrisd
#-------------------------------------------------------------------------------

from ycore.module.module import *
from ycore.module.listener import *
from ycore.event.event import Events

import re
import random

class GamblingModule(Module):

    def run(self):
        bank = Bank(0)
        self.addListener(MoneyListener(bank), Events.EVT_MSG_ARENA_MONEY)
        self.addListener(BankUpdater(bank), Events.EVT_MSG_ARENA)
        self.addListener(LoginOkListener(), Events.EVT_LOGIN)
        self.addListener(ShowMoneyListener(), Events.EVT_MSG_PRIVATE_CMD)

class LoginOkListener(Listener):

    def perform(self, loginEvent, queue, eventHandler):
        if (loginEvent.isSuccessful()):
            queue.sendCommand("?money")
            queue.sendCommand("?chat=jowie")

class BankUpdater(Listener):
    regex = "^MSG:ARENA:You have \\$(.+?) in your account (and) .+? experience\\.$"

    def __init__(self, bank):
        self.bank = bank

    def perform(self, event, handler, queue):
        if (re.match(self.regex, event.getMessage())):
            self.bank.set(int(re.findall(self.regex, event.getMessage())[0][0]) - 10000)

class ShowMoneyListener(Listener):

    def perform(self, commandEvent, queue, eventHandler):
        if (commandEvent.getCommand() == "showmoneyz"):
            queue.sendPrivateCommand(commandEvent.getPlayer(), "?showmoney")

class MoneyListener(Listener):
    def __init__(self, bank):
        self.bank = bank
        self.players = {}

    def isWin(self, player):
        return (random.random() > 0.1)

    def updateRecord(self, player, win, money):
        try:
            record = self.players[player]        
            if (win):
                self.players[player] = [record[0] + 1, record[1] + money]
            else:
                self.players[player] = [record[0] - 1, record[1] - money]
        except KeyError:
            self.players[player] = [0, 0]

    def perform(self, event, queue, handler):
        money = event.getMoney()

        if (money > 100000):
            queue.sendPrivateCommand(event.getPlayer(), "?give %i 100k max" % money)
            return

        self.bank.deposit(money)

        if (event.getMessage() == "dep"):
            return

        if (self.isWin(event.getPlayer())):
            if (self.bank.hasEnough(int(money * 1.1))):
                self.updateRecord(event.getPlayer(), True, money)
                self.bank.withdraw(int(money * 1.1))
                queue.sendPrivateCommand(
                    event.getPlayer(),
                    "?give %i Win." % (int(money * 1.1)))
                queue.sendChat("%s bet $%i, got back $%i" % (event.getPlayer(), money, money * 1.1))
            else:
                queue.sendPrivateMessage(event.getPlayer(),
                    "Lose.")
                queue.sendChat("%s bet $%i, got back $%i" % (event.getPlayer(), money, 0))
                self.updateRecord(event.getPlayer(), False, money)
        else:
            queue.sendPrivateMessage(event.getPlayer(),
                    "Lose.")
            queue.sendChat("%s bet $%i, got back $%i" % (event.getPlayer(), money, 0))
            self.updateRecord(event.getPlayer(), False, money)

class Bank():
    def __init__(self, money):
        self.money = money

    def withdraw(self, money):
        if (self.money < money):
            return False
        else:
            self.money -= money
            return True

    def deposit(self, money):
        print(self.money)
        self.money += money

    def set(self, money):
        self.money = money

    def hasEnough(self, money):
        return self.money > money
