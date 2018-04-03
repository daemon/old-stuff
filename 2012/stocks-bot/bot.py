##    Bot.py
##
##    Insert brilliant documentation here

import socket
import time
import threading
import command
import databases
import re

USERNAME    = 0xDEADBEEF        #make your user
PASSWORD    = 0xCAFEBABE        #make your pw

class Bot():
    def __init__(self, host, port, user, pw):
        self.host = host
        self.port = port
        self.user = user
        self.pw = pw
        self.sock = socket.socket()
        self.users = databases.User_DB("")
        self.commands = []

    def add(self, command):
        self.commands.append(command)

    def close(self):
        self.sock.close()

    def send_priv(self, data, user):
        self.sock.send((("SEND:PRIV:%s:%s\n") % (user, data)).encode())

    def send_raw(self, data):
        self.sock.send(("%s\n" % data).encode())

    def send_chat(self, data):
        self.sock.send((("SEND:CHAT:1;%s\n") % (data)).encode())

    def give_money(self, msg, user, amount):
        self.sock.send((("SEND:PRIVCMD:%s:?give %d %s\n") % (user, amount, msg)).encode())

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.sock.send(("LOGIN:1:%s:%s\n" % (self.user, self.pw)).encode())
        time.sleep(3)
        self.sock.send("GO:\n".encode())
        time.sleep(2)

    def handle_arena(self, line):
        for c in self.commands:
            if c.type == "arena" and re.match(c.regex, line, re.IGNORECASE):
                c.act(re.findall(c.regex, line, re.IGNORECASE), self)

    def handle_priv(self, line):
        for c in self.commands:
            if c.type == "priv" and re.match(c.regex, line, re.IGNORECASE):
                c.act(re.findall(c.regex, line, re.IGNORECASE), self)

    def main_loop(self):
        while True:
            try:
                buffer = self.sock.recv(4096).decode("utf-8", 'ignore')
                data_lines = buffer.split('\n')
                for line in data_lines:
                    if (line.startswith("MSG:ARENA:")):
                        threading.Thread(target=self.handle_arena, args=(line,)).start()
                        continue
                    if (line.startswith("MSG:PRIV:")):
                        threading.Thread(target=self.handle_priv, args=(line,)).start()
                        time.sleep(1.5)
                        continue

                print(buffer)
                time.sleep(0.02)
            except:
                self.close()

def main():
    b = Bot("208.122.59.226", 5005, USERNAME, PASSWORD)
    b.add(command.CMDP_help())
    '''b.add(command.CMDP_register())
    b.add(command.CMDA_credit())
    b.add(command.CMDP_cashout())
    b.add(command.CMDP_buy())'''
    b.add(command.CMDP_owner())
    '''b.add(command.CMDP_sell())
    b.add(command.CMDP_buyp())
    b.add(command.CMDP_sellp())
    b.add(command.CMDP_lookup())
    b.add(command.CMDP_overview())
    b.add(command.CMDP_shutdown())
    b.add(command.CMDP_showmoney())'''
    b.connect()
    b.send_raw("SEND:CMD:?chat=minecraft")
    b.main_loop()    

main()
