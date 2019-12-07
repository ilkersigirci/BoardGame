import random
import string
from enum import Enum
import secrets
import json
from utilities import NotificationModule
import re


class User:
    """
     User class docs
    """
    def _validation_decorator(method):
        def validate(*args):
            if args[0].verified:
                return method(*args)
            else:
                with open("verification.json", "r") as f:
                    data = json.load(f)
                    args[0].verified = data[args[0].email]["status"]
                    if not args[0].verified:
                        raise Exception("Not verified")
                return method(*args)
        return validate
    
    obs = NotificationModule()

    def __init__(self, email, namesurname, password, balance=0):
        if not re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" , email):
            raise ValueError("Email is not valid")
        self.email = email
        if not re.search("[A-Za-z]{2,25}\s[A-Za-z]{2,25}$", namesurname):
            raise ValueError("Namesurname is invalid")
        self.namesurname = namesurname
        if not re.search("^[a-zA-Z0-9_.+-]{8,16}$", password):
            raise ValueError("Password is invalid")
        self.password = password
        self.balance = balance
        self.reserved_balance = 0
        self.expenses = 0
        self.income = 0
        self.verification_number = secrets.token_urlsafe(32)
        self.items = []
        self.bought_items = []


        print(self.verification_number)
        self.verified = False
        data = {}
        try:
            with open("verification.json", "r") as f:
                data = json.load(f)
        except:
            pass
        with open("verification.json", "w") as f:
            data[self.email] = {"number": self.verification_number, "status": False}
            json.dump(data,f)

    @staticmethod
    def verify(email, verification_number):
        data = None
        with open("verification.json", "r") as f:
            data = json.load(f)
            if data[email]["number"] == verification_number:
                data[email]["status"] = True
            else:
                raise Exception("Verification number is not valid!")
        with open("verification.json", "w") as f:
            json.dump(data,f)
            

    @_validation_decorator
    def changepassword(self, newpassword, oldpassword=None):
        if not re.search("^[a-zA-Z0-9_.+-]{8,16}$", newpassword):
            raise ValueError("Password is invalid")
        if oldpassword is None:
            self.password = "".join([random.choice(string.ascii_letters) for i in range(15)])
            print("temp password is {}".format(self.password))
        else:
            if self.password == oldpassword:
                self.password = newpassword
            else:
                print("password is wrong")


    @_validation_decorator
    def listitems(self, user, itemtype = None, state='all'):
        if not isinstance(user,User):
            raise ValueError("invalid user")
        if user.items == []:
            print("There is no item in itemlist of {}".format(user.namesurname))
        ret = []
        for item in user.items:
            if (item.itemtype == itemtype or itemtype == None) and (item.state == state or state == 'all'):
                ret.append(item.title)
        return ret

    @_validation_decorator
    def notification(self,descr="user.notification"):
        print("Notification to {} with descr:{}".format(self.namesurname,descr))

    @staticmethod
    def watch(itemtype, watchmethod):
        User.obs.register(itemtype,watchmethod)
    
    @_validation_decorator
    def addBalance(self, amount):
        if not (type(amount) is float or type(amount) is int):
            raise ValueError("amount is invalid")
        self.balance += amount

        if amount > 0:
            self.income += amount

    @_validation_decorator
    def report(self):
        items_sold = [i.title for i in self.items if i.state == "sold"]
        items_onsale = [i.title for i in self.items if i.state == "active"]
        boug = [i.title for i in self.bought_items]

        return {
            "name": self.namesurname,
            "email": self.email,
            "items_sold": items_sold,
            "on_sale": items_onsale,
            "bought": boug,
            "all_expenses": self.expenses,
            "income": self.income,
            "balance": self.balance
        }

    @_validation_decorator
    def sell_item(self, item):
        if item in self.items:
            item.sell(self)
        else:
            raise Exception("Cannot be sold")

    @_validation_decorator
    def release_amount(self, amount):
        if not (type(amount) is float or type(amount) is int):
            raise ValueError("amount is invalid")
        self.reserved_balance -= amount

    @_validation_decorator
    def checkout(self, amount, item, owner, overall_bids = None):
        if not overall_bids is None:
            ''' type instant increment checkout from all '''
            for user in overall_bids:
                user.reserved_balance -= overall_bids[user]
                user.balance -= overall_bids[user]
                user.expenses += overall_bids[user]
                owner.addBalance(overall_bids[user])

            self.bought_items.append(item)

        else:
            self.reserved_balance -= amount
            self.balance -= amount
            owner.addBalance(amount)
            #owner.release_item(item)
            #self.add_item(item)
            self.bought_items.append(item)
            self.expenses += amount

    @_validation_decorator
    def release_item(self, item):
        try:
            self.items.remove(item)
        except ValueError as e:
            raise Exception("item not found")
    
    @_validation_decorator
    def add_item(self, item):
        self.items.append(item)

    @_validation_decorator
    def reserve_amount(self, amount):
        if amount <= self.balance - self.reserved_balance:
            self.reserved_balance += amount
            return True
        else:
            return False