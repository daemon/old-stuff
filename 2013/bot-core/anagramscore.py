import random
import time
import threading
from ycore.module.module import *
from ycore.module.listener import *
from ycore.event.event import Events

# Refactor..

class AnagramsModule(Module):
    def __init__(self, chats, betpercent, betamount, wordlist, queue, owner):
        super().__init__()
        self.chats = chats
        self.owner = owner
        self.queue = queue
        self.betpercent = betpercent
        self.betamount = betamount
        self.wordlist = wordlist
    
    def run(self):
        game = AnagramsGame(self.wordlist, self.betamount,
                            self.betpercent, self.queue)
        self.addListener(MoneyListener(game), Events.EVT_MSG_ARENA_MONEY)
        self.addListener(LoginOkListener(self.chats), Events.EVT_LOGIN)
        self.addListener(GameCommandListener(game, self.owner),
                         Events.EVT_MSG_PRIVATE_CMD)

class LoginOkListener(Listener):
    def __init__(self, chats):
        super().__init__()
        self.chats = chats

    def perform(self, loginEvent, queue, eventHandler):
        if (loginEvent.isSuccessful()):            
            queue.sendCommand("?chat=%s" % (self.chats))

class AnagramsGame():
    def __init__(self, wordlist, betamount, betpercent, queue):
        self.wordlist = wordlist
        with open(wordlist) as f:
            words = f.readlines()
            for word in words:
                word = word.replace('\n', '').lower()
        self.words = words
        self.nwords = len(words)
        self.betamount = betamount
        self.betpercent = betpercent
        self.word = ""
        self.queue = queue
        self.scrambled = ""
        self.isRunning = False
        self.prize = 0
        self.win = False

    def isRunning(self):
        return self.isRunning

    @staticmethod
    def isAnagram(word, anagram):
        histogramWord = {}
        histogramAnagram = {}
        separateWord = list(word)
        separateAnagram = list(anagram)

        for x in separateWord:
            if x in histogramWord:
                histogramWord[x] += 1
            else:
                histogramWord[x] = 1
        for x in separateAnagram:
            if x in histogramAnagram:
                histogramAnagram[x] += 1
            else:
                histogramAnagram[x] = 1

        for key in histogramAnagram:
            try:
                if (histogramAnagram[key] != histogramWord[key]):
                    return False
            except KeyError:
                return False
            
        return True

    @staticmethod
    def scramble(word):
        wordlist = list(word)
        keys = {}
        for w in wordlist:
            keys[random.random()] = w
        joined = ''
        for (k, v) in sorted(keys.items(), key=lambda k: k[0]):
            joined += v
        return joined
            
    def generateNext(self):
        self.word = self.words[random.randint(0, self.nwords - 1)].replace('\n', '')
        self.scrambled = AnagramsGame.scramble(self.word).replace('\n', '')
    
    def startGame(self, timeout=25):
        self.generateNext()
        self.isRunning = True
        self.prize = 0
        self.queue.sendChat("A game of Unscramble is beginning...", True)
        self.queue.sendChat("Unscramble %s. Good luck!" % self.scrambled)
        self.loseTimer = threading.Timer(timeout, self.nextWord)
        self.loseTimer.start()
        self.time = time.clock()

    def guessWord(self, word, player):        
        if (word.lower() == self.word and not self.win):            
            self.prize += self.betamount
            prize = int(self.prize * self.betpercent)
            deltatime = round(time.clock() - self.time, 2)

            self.sendChat = "%s correctly guessed %s in %d seconds! Prize: $%i" % (player, self.word, deltatime, prize)
            self.win = True            
            self.player = player
            self.sendPrivateMessage(player, "Nice! You got it.")            
        else:
            self.prize += self.betamount
            self.queue.sendChat("%s incorrectly guessed. (+$%i), ($%i)." % (player, self.betamount, int(self.prize * self.betpercent)))            

    def nextWord(self, win=False, timeout=25):
        if (self.win):
            self.queue.sendChat(self.sendChat)
            self.win = False
            self.queue.sendPrivateCommand(self.player, "?give %i You win!" % int(self.prize * self.betpercent))
            win = True
        if (not win):
            self.queue.sendChat("Time's up! No one guessed %s." % (self.word))
        self.generateNext()
        self.prize = 0
        self.queue.sendChat("The next unscramble is %s. Good luck!" % (self.scrambled))
        self.loseTimer = threading.Timer(timeout, self.nextWord)
        self.loseTimer.start()
        self.time = time.clock()        

    def stopGame(self):
        self.isRunning = False
        self.queue.sendChat("Game ended.")
        try:
            self.loseTimer.cancel()
        except:
            pass

    def isEnough(self, money):
        return self.betamount == money
    
class MoneyListener(Listener):
    def __init__(self, game):
        super().__init__()
        self.game = game
        
    def perform(self, event, queue, handler):
        if (not self.game.isRunning):
            queue.sendPrivateCommand(event.getPlayer(), "?give %i No game running! PM !about" % event.getMoney())
            return
        
        if (not self.game.isEnough(event.getMoney())):
            queue.sendPrivateCommand(event.getPlayer(), "?give %i Incorrect guess amount. PM !about" % event.getMoney())
            return
        
        if (not event.getMessage()):
            queue.sendPrivateCommand(event.getPlayer(), "?give %i You didn't guess anything! PM !about" % event.getMoney())
            return
        
        self.game.guessWord(event.getMessage(), event.getPlayer())

class GameCommandListener(Listener):
    START_CMD = "start"        
    STOP_CMD = "stop"
    WITHDRAW_CMD = "withdraw"
    ABOUT_CMD = "about"
    ABOUT_MSG = "Unscramble word game bot. Join ?chat=jowie, then PM \"?give %i <word>\" to guess <word>."
    
    def __init__(self, game, owner):
        super().__init__()
        self.owner = owner
        self.game = game

    def perform(self, commandEvent, queue, eventHandler):
        if (commandEvent.getCommand() == self.ABOUT_CMD):                    
            queue.sendPrivateMessage(commandEvent.getPlayer(), self.ABOUT_MSG % self.game.betamount)
        elif (commandEvent.getCommand() == self.START_CMD and commandEvent.getPlayer().lower() == self.owner):
            if (self.game.isRunning):
                queue.sendPrivateMessage(commandEvent.getPlayer(), "Running already!")
                return
            self.game.startGame()
        elif (commandEvent.getCommand() == self.STOP_CMD and commandEvent.getPlayer().lower() == self.owner):
            if (not self.game.isRunning):
                queue.sendPrivateMessage(commandEvent.getPlayer(), "No game running!")
                return
            self.game.stopGame()
        elif (commandEvent.getCommand() == self.WITHDRAW_CMD and commandEvent.getPlayer().lower() == self.owner):
            if (commandEvent.getArgs()):
                try:
                    queue.sendPrivateCommand(self.owner, "?give %s" % commandEvent.getArgs()[0])
                except:
                    pass
        
    
