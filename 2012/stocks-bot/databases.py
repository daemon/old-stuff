##    Databases
##
##    Don't bother trying to understand this. It's not meant to be modular.

import urllib.request
import random
import urllib.parse
import hashlib
import re
import os

class Stocks_DB():
    def __init__(self):
        pass

    def get_price(self, symbol):
        try:
            with urllib.request.urlopen("http://www.google.com/finance/info?infotype=infoquoteall&q=%s" % symbol) as u:
                content = u.read().decode("utf-8", "ignore")
            if ('This is an unknown symbol.' in content):
                return -1
            value = re.findall(',"l_cur" : "(.+?)"', content)[0].replace(',', '')
        except:
            return -1

        return value

class User_DB():
    def __init__(self, path):
        self.path = path
        self.lists = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j','k','l','m','n','o','p','q','r','s','t','u','v','w','y','z', '1','2','3','4','5','6','7','8','9','0']
        self.numb = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j','k','l','m','n','o','p','q','r','s','t','u','v','w','y','z', '1','2','3','4','5','6','7','8','9','0']

    def st_buy(self, user, symbol, shares):
        if (self.is_registered(user)):
            try:
                shares = int(shares)
            except:
                return (-1, 'Enter a valid number of shares. !buy symbol shares')
            value = float(Stocks_DB().get_price(symbol))
            if value == -1:
                return (-1, 'Enter a valid symbol. !buy symbol shares')
            
            assets = self.get_credit(user)[0]
            total_price = value * shares
            
            if (total_price > assets):
                return (-1, 'You do not have enough money.')

            sanitized_user = self.sanitized(user)
            order_num = ''
            order_num += self.lists[random.randint(0, len(self.lists) - 1)]
            order_num += self.numb[random.randint(0, len(self.numb) - 1)]
            order_num += self.lists[random.randint(0, len(self.lists) - 1)]
            
            with open('database/%s.log' % sanitized_user, 'a') as f:
                f.write('Order # %s) bought:%d:%s at %s for $%s\n' % (order_num, shares, symbol.lower(), str(value), str(round(total_price, 2))))

            self.deduct_credit(user, total_price, False)
            self.send_portfolio(user)
            return (0, 'Buy successful. Balance: $%s. Order number %s http://www.t--t.info/%s' % (str(round(assets - total_price, 2)), order_num, self.web_sanitized(user)),
                    '%s bought %s of %s for $%s.' % (user, str(shares), symbol.upper(), str(round(total_price, 2))))
        else:
            return (-1, 'Not registered. Give money or do !register to register.')

    def st_sell(self, user, order_number):
        if (self.is_registered(user)):
            sanitized_user = self.sanitized(user)

            with open('database/%s.log' % sanitized_user) as f:
                lines = f.readlines()

            final_str = ''
            flag = False
            for x in range(0, len(lines)):
                if lines[x].startswith('Order # %s' % order_number.lower()):
                    stock_data = lines[x]
                    stock_ord = x
                    flag = True
                    break
            
            if (not flag):
                return (-1, "Enter a valid order number. http://www.t--t.info/%s" % self.web_sanitized(user))          
            
            shares, symbol = re.findall('Order # .+?\\) bought:(.+?):(.+?) at .+? for \\$.+?\n', stock_data)[0]
            shares = int(shares)
            value = float(Stocks_DB().get_price(symbol))
            assets = self.get_credit(user)[0]
            total_price = value * shares
            self.add_credit(user, total_price, False)
            with open('database/%s.log' % sanitized_user) as f:
                lines = f.readlines()
            lines.pop(stock_ord)
            with open('database/%s.log' % sanitized_user, 'w') as f:
                for x in lines:
                    f.write(x)
            self.send_portfolio(user)
            return (0, 'Sell successful. Balance: $%s. http://www.t--t.info/%s' % (str(round(assets + total_price, 2)), self.web_sanitized(user)),
                    '%s sold %s of %s for $%s.' % (user, str(shares), symbol.upper(), str(round(total_price, 2))))
        else:
            return (-1, 'Not registered. Give money or do !register to register.')

    def sanitized(self, string):
        h = hashlib.new('ripemd160')
        h.update(string.lower().encode())
        return h.hexdigest()

    def web_sanitized(self, string):
        s = string.lower()
        final_str = ''
        for x in range(0, len(s)):
            if s[x].isalpha():
                final_str += s[x]
            else:
                final_str += str((ord(s[x]) % 100) % 10)

        return final_str

    def is_registered(self, name):
        return ("%s.log" % self.sanitized(name) in os.listdir("database"))

    def register(self, name, money):
        if (self.is_registered(name)):
            return (False, 'Already registered.')
        else:
            with open("database/%s.log" % self.sanitized(name), 'w') as f:
                f.write("balance:%s\n" % money)
            return (True, 'Registered with $%s. Send !help for help. Portfolio: http://www.t--t.info/%s' % (money, self.web_sanitized(name)))

    def get_credit(self, name):
        if (self.is_registered(name)):
            balance = 0
            with open("database/%s.log" % self.sanitized(name)) as f:
                database = f.readlines()
            for x in database:
                if x.startswith("balance:"):
                    balance = float(x.replace('balance:', '').replace('\n', ''))

            return (balance, "You have $%f" % round(balance, 2))
        else:
            self.register(name, money)
            return (-1, "You are not registered.")

    def get_worth(self, name):
        with open("database/%s.log" % self.sanitized(name)) as f:
            lines = ''.join(f.readlines())

        monies = re.findall('Order # .+?\\) bought:.+?:.+? at .+? for \\$(.+?)\n', lines)
        tot = 0
        for x in monies:
            tot += float(x)

        return tot

    def add_credit(self, name, money, user_supplied):
        if (self.is_registered(name)):
            balance = 0
            with open("database/%s.log" % self.sanitized(name)) as f:
                database = f.readlines()
            for x in database:
                if x.startswith("balance:"):
                    balance = float(x.replace('balance:', '').replace('\n', ''))
            if (user_supplied and balance + float(money) > 100000):
                return (-26, 'Initial balance cannot exceed 100k')
            elif (user_supplied and balance + float(money) + self.get_worth(name) > 100000):
                return (-26, 'Initial balance cannot exceed 100k.')

            with open("database/%s.log" % self.sanitized(name), 'w') as f:
                for x in database:
                    x = x.replace('\n', '')
                    if x.startswith('balance:'):
                        f.write("balance:%s\n" % (str(round(balance + float(money), 2))))
                    else:
                        f.write(x + '\n')
            return (balance + round(float(money), 2),'New balance: $%s. Portfolio: http://www.t--t.info/%s' % (str(balance + round(float(money), 2)), self.web_sanitized(name)))
        else:
            self.register(name, money)
            return (round(float(money), 2),'Registered with $%s. Send !help for help. Portfolio: http://www.t--t.info/%s' % (money, self.web_sanitized(name)))

    def send_portfolio(self, name):
        data_string = ''
        with open("database/%s.log" % self.sanitized(name)) as f:
            data = f.readlines()
        for x in data:
            data_string += x
        data_string.replace('\n', '</br>')                               
        with urllib.request.urlopen("http://www.t--t.info/send.php?user=%s" % self.web_sanitized(name), urllib.parse.urlencode([('text', data_string)]).encode()) as u:
            pass

    def st_overview(self, user):
        if (self.is_registered(user)):
            sanitized_user = self.sanitized(user)
            with open('database/%s.log' % sanitized_user) as f:
                lines = ''.join(f.readlines())

            find_array = re.findall('Order # .+?\\) bought:(.+?):(.+?) at .+? for \\$(.+?)\n', lines)
            buy_price = 0
            now_price = 0
            for x in find_array:
                shares, symbol, buys = x
                shares = int(shares)
                buy_price += float(buys)
                now_price += float(Stocks_DB().get_price(symbol)) * shares

            percent = str(round(100 * ((now_price - buy_price) / buy_price), 2))
            return(0, "Changed a total of $%s (%s%s)" % (str(round(now_price - buy_price, 2)), percent, "%"))
        else:
            return (-1, 'Not registered. Give money or do !register to register.')
        
    def deduct_credit(self, name, money, user_supplied):
        return self.add_credit(name, '-%s' % money, user_supplied)
    
        
