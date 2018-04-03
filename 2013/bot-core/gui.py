from tkinter import *
from ycore.application import *
from ycore.module.core import *
from ycore.network.network import *
from ycore.network.util import *
from ycore.builder import *
from ycore.client import *
from anagramscore import *

import threading
import json

# Current GUI design is quick and dirty. 

# Better versions of this GUI--if I seek to continue developing
# this nuclear meltdown--may come out in the future. Please bear with me.

# TODO: Provide a unified controller for /ALL/ bots.

class App:
    def __init__(self):
        root = Tk()
        root.geometry("350x300+300+300")
        frame = Frame(root)
        frame.pack(fill=BOTH, expand=1)

        # Make rows...
        frame.rowconfigure(0, pad=3)
        frame.rowconfigure(1, pad=3)
        frame.rowconfigure(2, pad=3)
        frame.rowconfigure(3, pad=3)
        frame.rowconfigure(4, pad=3, weight=1)
        frame.columnconfigure(0, pad=3, weight=1)
        frame.columnconfigure(1, pad=3)
        frame.columnconfigure(2, pad=3)
        frame.columnconfigure(3, pad=3)
        frame.columnconfigure(4, pad=3)                

        #Make GUI...
        Label(frame, text="Username:").grid(sticky=W, row=0, column=0)
        self.username =  Entry(frame)        
        self.username.grid(row=1, sticky=E+W, column=0, columnspan=2, padx=5)

        Label(frame, text="Password:").grid(sticky=W, row=2, column=0)
        self.password =  Entry(frame)        
        self.password.grid(row=3, sticky=E+W, column=0, columnspan=2, padx=5)

        self.button_stop = Button(frame, text="Disconnect", width=12, state=DISABLED, command=self.disconnect)
        self.button_go = Button(frame, text="Connect", width=12, command=self.connect)
        self.button_clear = Button(frame, text="Clear", width=12, command=self.clear)
        self.button_configure = Button(frame, text="Reload config", width=24, command=self.loadConfig)

        self.button_stop.grid(row=1, column=2)
        self.button_go.grid(row=1, column=3)
        self.button_clear.grid(row=5, column=3)
        self.button_configure.grid(row=3, column=2, columnspan=2)

        self.text = Text(frame)
        self.text.grid(row=4, sticky=E+W+N+S, column=0, rowspan=1, columnspan=4, padx=5, pady=5)

        self.scrollbar_log = Scrollbar(frame, command=self.text.yview, orient=VERTICAL)
        self.scrollbar_log.grid(row=4, column=3, columnspan=4, sticky=N+S+E, padx=5)
        self.text.configure(yscrollcommand=self.scrollbar_log.set)

        # Load data...
        self.loadConfig()        
        self.init()        
        root.mainloop()

    def clear(self):        
        self.text.delete("1.0", END)

    def loadConfig(self):
        # Load config data...
        self.config = ConfigLoader().load()
        self.user = self.config['user']
        self.owner = self.config['owner']
        self.passwd = self.config['password']
        self.wordlist = self.config['wordlist']
        self.bet = self.config['betamount']
        self.betpercent = self.config['betpercent']
        self.chat = self.config['chat']
        self.ip = self.config['ip']
        self.port = self.config['port']

        self.username.delete(0, END)
        self.password.delete(0, END)
        self.password.insert(0, self.passwd)
        self.username.insert(0, self.user)

    def init(self):
        # Initialize core...
        logBuilder = ChatnetLogMethodBuilder(1).setMethod(WindowLogMethod(self.text))
        logger = logBuilder.addFilter("^MSG:PUB(M)?:(.+?):(.+)$").build()
        clientBuilder = ChatnetClientBuilder().networkManager(
            LogWriter(ThrottledNetwork(ChatNetworkManager(self.ip, self.port)), logger))
        self.client = clientBuilder.build()
        self.bot = BotApplication(self.client)
        self.bot.enableModule(CoreModule(self.username.get(), self.password.get()))

        # Could make observer...
        self.bot.enableModule(AnagramsModule(self.chat, self.betpercent, self.bet,
                                             self.wordlist, self.client.getQueue(), self.owner))
        
    def connect(self):
        # Runs main bot thread...
        self.init()
        threading.Thread(target=self.bot.start).start()
        self.button_go.configure(state=DISABLED)
        self.button_stop.configure(state=ACTIVE)

    def disconnect(self):
        # Disconnects gracefully from server...
        try:
            self.client.getQueue().close()
        except:
            pass
        self.button_go.configure(state=ACTIVE)
        self.button_stop.configure(state=DISABLED)

class ConfigLoader:
    def __init__(self, filename="config.ini"):
        self.filename = filename
        self.dict = {}
    
    def load(self):
        with open(self.filename) as f:
            self.dict = json.load(f)
        return self.dict

class WindowLogMethod(LogMethod):
    def __init__(self, text):
        super().__init__()
        self.text = text
        
    def write(self, message):
        # Make template for message filter checking...
        for m in message.split('\n'):
            if (not super().matches(m)):                
                self.text.insert(END, super().parse(m))
                self.text.yview(END)

App()
