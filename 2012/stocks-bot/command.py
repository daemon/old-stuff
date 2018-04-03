##    Command.py
##    CSS3 command framework using integrated AJAX WebGLSL
##    TODO: Cleanup, make bot modular
##
##    Contains all the commands for the bot.
##
##    Constructor
##    self.doc            - documentation (unimplemented)
##    self.type           - priv is a private command
##                        - arena is a arena message (ie player tetris- granted you -$100000)
##    self.args           - number of arguments in the command. In other words, how many variables to derive from the regex
##    self.regex          - the regular expression to use.
##    self.show_on_help   - unimplemented
##
##    act
##    args[0]             - if priv, then it's the username of the person
##    args[0][x]          - x'th argument that you specified. If 1 argument, then use args[1]. (re.findall behavior)

import os
import time
import databases

class Command():
    def __init__(self):
        self.doc = "Hahaha"
        self.type = "null"
        self.args = 0
        self.prefix = "command"
        self.regex = ""
        self.show_on_help = False

    def act(self, args, bot):
        pass

class CMDP_overview(Command):
    def __init__(self):
        self.doc = "Overview of order number."
        self.type = "priv"
        self.args = 0
        self.prefix = "overview"
        self.regex = "^MSG:PRIV:(.+?):!%s$" % self.prefix
        self.show_on_help = False

    def act(self, args, bot):
        returncode = bot.users.st_overview(args[0])
        bot.send_priv(returncode[1], args[0])

class CMDP_help(Command):
    def __init__(self):
        self.doc = "Help command."
        self.type = "priv"
        self.args = 0
        self.prefix = "help"
        self.regex = "^MSG:PRIV:(.+?):!%s$" % self.prefix
        self.show_on_help = True

    def act(self, args, bot):
        bot.send_priv("wip bot gr04ch01. charge $3000 for use of irc relay to specific chat.", args[0])

class CMDP_register(Command):
    def __init__(self):
        self.doc = "Register yourself."
        self.type = "priv"
        self.args = 0
        self.prefix = "register"
        self.regex = "^MSG:PRIV:(.+?):!%s$" % self.prefix
        self.show_on_help = True

    def act(self, args, bot):
        bot.send_priv(bot.users.register(args[0].lower(), 0)[1], args[0])
        bot.users.send_portfolio(args[0])

class CMDP_cashout(Command):
    def __init__(self):
        self.doc = "Cashout."
        self.type = "priv"
        self.args = 1
        self.prefix = "cashout"
        self.regex = "^MSG:PRIV:(.+?):!%s$" % self.prefix
        self.show_on_help = True

    def act(self, args, bot):
        balance, msg = bot.users.get_credit(args[0])
        if (balance >= 100):
            bot.give_money("Here ya goes!", args[0], int(balance))
            bot.users.deduct_credit(args[0], int(balance), False)
            bot.send_chat("%s cashed out $%s" % (args[0], str(balance)))
        bot.users.send_portfolio(args[0])

class CMDA_credit(Command):
    def __init__(self):
        self.doc = "Get credit."
        self.type = "arena"
        self.args = 0
        self.prefix = "null"
        self.regex = "^MSG:ARENA:Player (.+?) gave you \\$(.+?)\\.(.+?)?$"
        self.show_on_help = False

    def act(self, args, bot):
        returncode = bot.users.add_credit(args[0][0].lower(), int(args[0][1]), True)
        if (returncode[0] == -26):
            bot.give_money(returncode[1], args[0][0], int(args[0][1]))
            return
        bot.send_priv(returncode[1], args[0][0])
        bot.users.send_portfolio(args[0][0])
        
class CMDP_buy(Command):
    def __init__(self):
        self.doc = "Buy stocks."
        self.type = "priv"
        self.args = 0
        self.prefix = "buy"
        self.regex = "^MSG:PRIV:(.+?):!%s +?(.+?) +?(.+?)$" % self.prefix
        self.show_on_help = False

    def act(self, args, bot):
        returncode = bot.users.st_buy(args[0][0], args[0][1], args[0][2])
        bot.send_priv(returncode[1], args[0][0])
        if returncode[0] == 0:
            time.sleep(2)
            bot.send_chat(returncode[2])

class CMDP_buyp(Command):
    def __init__(self):
        self.doc = "Buy stocks."
        self.type = "priv"
        self.args = 0
        self.prefix = "buyp"
        self.regex = "^MSG:PRIV:(.+?):!%s +?(.+?) +?(.+?)$" % self.prefix
        self.show_on_help = False

    def act(self, args, bot):
        returncode = bot.users.st_buy(args[0][0], args[0][1], args[0][2])
        bot.send_priv(returncode[1], args[0][0])
        if returncode[0] == 0:
            time.sleep(2)
            bot.send_chat("A private trade was made.")

class CMDP_sell(Command):
    def __init__(self):
        self.doc = "Sell stocks."
        self.type = "priv"
        self.args = 0
        self.prefix = "sell"
        self.regex = "^MSG:PRIV:(.+?):!%s +?(.+?)$" % self.prefix
        self.show_on_help = False

    def act(self, args, bot):
        returncode = bot.users.st_sell(args[0][0], args[0][1])
        bot.send_priv(returncode[1], args[0][0])
        if returncode[0] == 0:
            time.sleep(2)
            bot.send_chat(returncode[2])

class CMDP_sellp(Command):
    def __init__(self):
        self.doc = "Sell stocks."
        self.type = "priv"
        self.args = 0
        self.prefix = "sellp"
        self.regex = "^MSG:PRIV:(.+?):!%s +?(.+?)$" % self.prefix
        self.show_on_help = False

    def act(self, args, bot):
        returncode = bot.users.st_sell(args[0][0], args[0][1])
        bot.send_priv(returncode[1], args[0][0])
        if returncode[0] == 0:
            time.sleep(2)
            bot.send_chat("A private trade was made.")

class CMDP_lookup(Command):
    def __init__(self):
        self.doc = "Lookup a stock."
        self.type = "priv"
        self.args = 0
        self.prefix = "lookup"
        self.regex = "^MSG:PRIV:(.+?):!%s +?(.+?)$" % self.prefix
        self.show_on_help = False

    def act(self, args, bot):
        value = databases.Stocks_DB().get_price(args[0][1])
        if (value == -1):
            bot.send_priv("Unknown symbol.", args[0][0])
            return
        bot.send_priv(str(value), args[0][0])
        
class CMDP_owner(Command):
    def __init__(self):
        self.doc = "Req owner."
        self.type = "priv"
        self.args = 0
        self.prefix = "owner"
        self.regex = "^MSG:PRIV:(.+?):!%s$" % self.prefix
        self.show_on_help = False

    def act(self, args, bot):
        bot.send_priv("gr04ch01", args[0])

class CMDP_shutdown(Command):
    def __init__(self):
        self.doc = "Shutdown."
        self.type = "priv"
        self.args = 0
        self.prefix = "shutdown"
        self.regex = "^MSG:PRIV:(.+?):!%s$" % self.prefix
        self.show_on_help = False

    def act(self, args, bot):
        if (args[0].lower().capitalize() in ['Tetris-', 'Dr brain', 'D1st0rt', 'Swift warrior', 'Masaru', 'Spidernl', 'Rivel', 'Noldec', 'Psythe']):
            bot.close()

class CMDP_showmoney(Command):
    def __init__(self):
        self.doc = "Show money."
        self.type = "priv"
        self.args = 0
        self.prefix = "bigmoney"
        self.regex = "^MSG:PRIV:(.+?):!%s$" % self.prefix
        self.show_on_help = False

    def act(self, args, bot):
        if (args[0].lower().capitalize() == 'Tetris-'):
            bot.send_raw('SEND:PRIVCMD:tetris-:?showmoney -e')
        
    

