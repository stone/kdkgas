import sqlite3

class dataBaseInterface(object):
    """Class used for databas interfacing"""

    def __init__(self):
        self.conn = sqlite3.connect("db/kdkgas.db")
        self.cursor = self.conn.cursor()

    def queryfetchall(self, sql):
        """Returns a sqlite fetchall()"""
        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        return ret

    def queryfetchone(self, sql):
        """Returns a sqlite fetchone()"""
        self.cursor.execute(sql)
        ret = self.cursor.fetchone()
        return ret

    def getFillers(self):
        sql = "SELECT filler_name FROM filler"
        fillers = self.queryfetchall(sql)
        fillersdict = {}
        for name in fillers:
            fillersdict[name[0]] = None
        return fillersdict

    def getBuyers(self):
        sql = "SELECT buyer_name from buyer"
        buyers = self.queryfetchall(sql)
        buyerslist = []
        for name in buyers:
            buyerslist.append(name[0])
        return buyerslist

    def getBottles(self, buyer):
        """Get the different bottles for buyer and return size in L and max pressure in BAR"""
        sql = "SELECT size, maxpres from buyer JOIN bottle USING (buyer_id) where buyer_name = \"%s\";" % buyer
        tmp = self.queryfetchall(sql)
        bottledict = {}
        for b in tmp:
            bottledict["%dL (%dBAR)" % b] = None
        return bottledict
        #return {"bottle_1", "bottle_2"}

    def getBottleSize(self, bottle, owner):
        return "12"
    
    def getBottleMaxPress(self, bottle, owner):
        return "200"

    def getFillNr(self):
        return 1

    def getHePrice(self):
        price = self.queryfetchone("SELECT price from pricelist where name = \"HE\"")
        return float(price[0])
        #return 0.05
    
    def getO2Price(self):
        price = self.queryfetchone("SELECT price from pricelist where name = \"O2\"")
        return float(price[0])
        #return 0.05
