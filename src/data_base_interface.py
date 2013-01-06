

class dataBaseInterface(object):

    def getFillers(self):
        return {"Johan Ivarsson", "Fredrik Helliksson"}

    def getBuyers(self):
        return ["Johan Ivarsson", "Fredrik Helliksson", "Fredrik Steen", "Micke Stentrom"]

    def getBottles(self, byer):

##        byers = self.getBuyers()
##        if not byer in byers:
##            raise not_a_byer(byer + "is not a registered customer")

        return {"bottle_1", "bottle_2"}

    def getBottleSize(self, bottle, owner):
        return "12"
    
    def getBottleMaxPress(self, bottle, owner):
        return "200"

    def getFillNr(self):
        return 1

    def getHePrice(self):
        return 0.05
    
    def getO2Price(self):
        return 0.05
