from peewee import *
import datetime
import os.path
"""Here we handle our databases, we use PeeWee for abstraction:

Website: https://github.com/coleifer/peewee

"""

DATABASEPATH="db/kdkgaspw.db"

db = SqliteDatabase(DATABASEPATH)

class BaseModel(Model):
    class Meta:
        database = db

class Filler(BaseModel):
    """The person that are allowed to mix gas and fill """
    name = CharField()

class Buyer(BaseModel):
    """The person that is buying gas """
    name = CharField()

class Bottle(BaseModel):
    """A Bottle used for gas"""
    owner = ForeignKeyField(Buyer, related_name='buyer')
    size = IntegerField()
    maxpres = IntegerField()

class Price(BaseModel):
    """Price of gas"""
    name = CharField()
    price = FloatField()

class Bank(BaseModel):
    """Gas bank"""
    name = CharField()
    volume = FloatField()
    cur_pressure = FloatField()
    max_pressure = FloatField()

class Gas(BaseModel):
    """Used in FillLog to keep track of amount of gas filled"""
    name = CharField()
    volume = FloatField()

class FillLog(BaseModel):
    """Log of filles, who, when what..."""
    fill_date = DateTimeField(default=datetime.datetime.now)
    bottle = ForeignKeyField(Bottle, related_name='bottle')
    filler = ForeignKeyField(Filler, related_name='filler')
    buyer = ForeignKeyField(Buyer, related_name='buyer')
    gas_amount = ForeignKeyField(Gas, related_name='gas')
    start_pressure = FloatField()
    end_pressure = FloatField()


def create_db():
    """This needs to be called on when first creating the database,
    it generates some test data. """
    import random
    print "Creating database, filling with test data, hang on..."
    print "Creating tables..."

    print "\t- Filler"
    Filler.create_table()
    print "\t- Buyer"
    Buyer.create_table()
    print "\t- Bottle"
    Bottle.create_table()
    print "\t- Price"
    Price.create_table()
    print "\t- Bank"
    Bank.create_table()
    print "\t- FillLog"
    FillLog.create_table()

    # Time to add some data to the model
    fillers = ["Chuck Norris", "Frank Sinatra", "Sylvester Stallone"]
    for f in fillers:
        print "Adding filler: %s" % f
        Filler.create(name=f).save()

    buyers = ["Barnaby Hughard", "Mellan Vittorio", "Rustam Ori", "Carver Jakob"]
    sizes = [3, 7, 10, 12, 24, 30]
    pres = [200,232,300]
    for b in buyers:
        print "Adding Buyer: %s" % b
        t = Buyer.create(name=b)
        t.save()
        for x in range(3):
            Bottle.create(owner = t, size = random.choice(sizes), maxpres = random.choice(pres)).save()

    print "Adding to pricelist"
    Price.create(name="O2", price=0.05).save()
    Price.create(name="HE", price=0.5).save()

    # Bank
    print "Adding banks"
    for gas in ["HE", "O2"]:
        print "Bank: %s" % gas
        Bank(name = gas, volume = 50, cur_pressure = 200, max_pressure = 200).save()

    print "done."




class dataBaseInterface(object):
    """Class used for databas interfacing"""

    def __init__(self):
        if not os.path.isfile(DATABASEPATH):
            create_db()

    #######################################################
    #
    #  Section with new Database calls:
    #
    #######################################################
    def getHeBankVolume(self):
        return 50
    
    def getO2BankVolume(self):
        return 50

    def getHeBankPressure(self):
        return 150
                
    def getO2BankPressure(self):
        return 110

    def writeHeBankPressure(self, p):
        print "Helium bank pressure: %d" % p
    
    def writeO2BankPressure(self, p):
        print "Oxygen bank pressure: %d" % p

    def moneyToPay(self, price, customer):
        print customer + "skall betala " + price + " kr"

    #######################################################
    
    def getFillers(self):
        fillersdict = {}
        for f in Filler.select():
            fillersdict[f.name] = f.id
        return fillersdict

    def getBuyers(self):
        buyerslist = []
        for b in Buyer.select():
            buyerslist.append(b.name)
        return buyerslist

    def getBottles(self, buyer):
        """Get the different bottles for buyer and return size in L and max pressure in BAR"""
        bottledict = {}
        for bottle in Bottle.select().join(Buyer).where(Buyer.name == buyer):
            bottledict["%sL (%dBAR)" % (bottle.size, bottle.maxpres)] = bottle.id
        return bottledict

    def getBottleSize(self, bottle, owner):
        return "12"
    
    def getBottleMaxPress(self, bottle, owner):
        return "200"

    def getFillNr(self):
        return 1

    def getHePrice(self):
        return Price.select().where(Price.name == 'HE').get()
    
    def getO2Price(self):
        return Price.select().where(Price.name == 'O2').get()
