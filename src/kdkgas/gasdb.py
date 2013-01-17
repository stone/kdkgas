from peewee import *
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
    name = CharField()

class Buyer(BaseModel):
    name = CharField()

class Bottle(BaseModel):
    owner = ForeignKeyField(Buyer, related_name='buyer')
    size = IntegerField()
    maxpres = IntegerField()

class Price(BaseModel):
    name = CharField()
    price = FloatField()

class Bank(BaseModel):
    name = CharField()
    volume = FloatField()
    cur_pressure = FloatField()
    max_pressure = FloatField()

def create_db():
    """This needs to be called on when first creating the database,
    it generates some test data. """
    import random
    print "Creating database, filling with test data, hang on..."
    print "Creating tables..."
    Filler.create_table()
    Buyer.create_table()
    Bottle.create_table()
    Price.create_table()

    # Time to add some data to the model
    fillers = ["Chuck Norris", "Frank Sinatra", "Sylvester Stallone"]
    for f in fillers:
        print "Adding filler: %s" % f
        t = Filler.create(name=f)
        t.save()

    buyers = ["Barnaby Hughard", "Mellan Vittorio", "Rustam Ori", "Carver Jakob"]
    sizes = [3, 7, 10, 12, 24, 30]
    pres = [200,232,300]
    for b in buyers:
        print "Adding Buyer: %s" % b
        t = Buyer.create(name=b)
        t.save()
        for x in range(3):
            b1 = Bottle.create(owner = t, size = random.choice(sizes), maxpres = random.choice(pres))
            b1.save()

    print "Adding to pricelist"
    p1 = Price.create(name="O2", price=0.05)
    p1.save()
    p2 = Price.create(name="HE", price=0.5)
    p2.save()
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
