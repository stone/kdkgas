import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
import datetime
import os.path
import os

LOGFILEPTH="db/logfile.txt"
XMLDATABASEPATH = "db/db_xml.xml"


def create_db():
  print "create DB"


class dataBaseInterface(object):
 
    def __init__(self):
        
        self.tree = ElementTree("db_top", XMLDATABASEPATH)
        
        if not os.path.isfile(LOGFILEPTH):
            self.log = open(LOGFILEPTH, "a")
            self.log.write("date\tfiller\tcustomer\tfilled O2\t filled HE\tO2 from Bank\tanalyzed O2\tHe From Bank\tanalyzed HE\tprice\n")
        else:
            self.log = open(LOGFILEPTH, "a")
            self.log.write("\n")

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
        
    def getFillers(self):
        fillersdict = []
        for item in self.tree.getiterator('filler'):
            fillersdict.append(item.get('name').strip())
        return fillersdict

    def getBuyers(self):
        buyerDict = []
        for item in self.tree.getiterator('customer'):
            buyerDict.append(item.get('name').strip())
        return buyerDict


    def getAllBottles(self):
        bottleDict = []
        for item in self.tree.getiterator('tank'):
          bottleDict.append(item.get('name'))
        return bottleDict                 
            
    def getBottles(self, buyer):
        bottleDict = []
        for item in self.tree.getiterator('customer'):
            if item.get('name').strip() == buyer:
                tankList = item.getchildren()
                for tank in tankList:
                    bottleDict.append(tank.get('name').strip())

        return bottleDict
        

    def getBottleSize(self, bottle):
        for item in self.tree.getiterator('tank'):
            if item.get('name').strip() == bottle:
                return item.get('size').strip()
        return "0"
    
    def getBottleMaxPress(self, bottle, owner):
        for item in self.tree.getiterator('tank'):
            if item.get('name').strip() == bottle:
                return item.get('maxPressure').strip()
        return "0"

    def getHePrice(self):
        return self.tree.find('general').get('HE').strip()
    
    def getO2Price(self):
        return self.tree.find('general').get('O2').strip()

    def getFillNr(self):
            return self.tree.find('general').get('fillNr').strip()

    def addBlender(self, blender):
        current = ET.SubElement(self.tree.getroot(), 'filler')
        current.set('name', blender.strip())
        self.saveDb()

    def addCustomer(self, customer):
      current = ET.SubElement(self.tree.getroot(), 'customer')
      current.set('name', customer.strip())
      self.saveDb()

    def addBottleToCustomer(self, bottle, customer):
        for item in self.tree.getiterator('customer'):
            if item.get('name').strip() == buyer.strip():
                current = ET.SubElement(item, 'tankName')
                current.set('name', bottle.strip())
                self.saveDb()
                return


            
    def saveDb(self):
        print "save the DB"
        self.tree.write("db_temp.xml")
        os.remove(XMLDATABASEPATH)
        os.rename("db_temp.xml", XMLDATABASEPATH)
        
    def write_filled_gas(self, filler, customer, nO2, nHe):
        print "date: %s" % datetime.datetime.now()
        print "filler %s" % filler
        print "customer %s" % customer
        print "O2: %s" % nO2
        print "He: %s " % nHe
        gen = self.tree.find('general')
        fillnr = gen.get('fillNr').strip()
        self.log.write("%s\t%s\t%s\t%s\t%s\t%s\t" % (datetime.datetime.now(), fillnr, filler, customer, nO2, nHe))
        self.log.flush()
        gen.set('fillNr', str(int(fillnr)+1))
        self.saveDb()

    def writeAnalyzedGas(self, fO2, nO2, fHe, nHe, price, bottle):
        self.log.write("%s\t%s\t%s\t%s\t%s\n" % (nO2, fO2, nHe, fHe, price)) 
        self.log.flush()      
        for item in self.tree.getiterator('tank'):
            if item.get('name').strip() == bottle:
                item.set('lastHe', fHe)
                item.set('lastO2', fO2)
        self.saveDb()

                             
if __name__ == '__main__':

    tst = tst_xml()
    fillers = tst.getFillers()
    print fillers
    buyers = tst.getBuyers()
    print buyers
    botles = tst.getBottles('cust1')
    print botles
    print tst.getO2Price()
    print tst.getHePrice()
    
