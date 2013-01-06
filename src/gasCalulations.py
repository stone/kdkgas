

R = 8314.0
T = 293.0

fO2_air = 0.21
fN_air = 0.79

class GasCalcError(Exception):
    pass

class GasCalculations(object):
    def __init__(self, fO2_old, fO2_new, fHe_old, fHe_new, tankSize, pTank_old, pTank_new):
        self.fO2_old = fO2_old
        self.fO2_new = fO2_new
        self.fHe_old = fHe_old
        self.fHe_new = fHe_new
        self.fN_old = 1 - fO2_old - fHe_old
        self.fN_new = 1 - fO2_new - fHe_new
        self.tankSize = tankSize
        self.pTank_old = self.barToPascal(pTank_old)
        self.pTank_new =  self.barToPascal(pTank_new)

    def pascalToBar(self, pascal):
        return pascal*1e-5
    def barToPascal(self, bar):
        return bar*1e5

    def molToLiter(self, mol):
        return mol*R*T/1e5
        
    def getFilledGas(self):
        self.calculateGasToFill()
        return {"O2": self.amountO2ToFill, "He" : self.amountHeToFill}
        
    def calculateGasToFill(self):
        self.amountHeToFill = self.gas_ToFill(self.fHe_old, self.fHe_new)
        self.amountO2ToFill = self.gas_ToFill(self.fO2_old, self.fO2_new)
        self.amountNToFill  = self.gas_ToFill(self.fN_old,  self.fN_new)
        if self.amountO2ToFill < 0:
            raise GasCalcError("To much O2 in the tank!")
        if self.amountHeToFill < 0:
            raise GasCalcError("To much He in the tank!")
            

    def gas_ToFill(self, old_p, new_p):
        n_old = self.calcAmount(self.calcPartialPressure(old_p, self.pTank_old),
                                  self.tankSize)
        n_new = self.calcAmount(self.calcPartialPressure(new_p, self.pTank_new),
                                  self.tankSize)
        return n_new - n_old                    

    #Calculates the end pressure when filling a Tank
    def getHeEndPressure(self, start_p):
        return start_p + self.getHeFillPressure()

    def getO2EndPressure(self, start_p):
        return start_p + self.getO2FillPressure()
    
    #Calculates how many bar the pressure in the tank must increase
    #for the necessary amount of Gas
    
    def getO2FillPressure(self):
        return (self.pascalToBar(self.pTank_new) - self.getHeFillPressure() -
                self.getAirFillPressure() - self.pascalToBar(self.pTank_old))
    
    def getHeFillPressure(self):
        return self.pascalToBar(self.amountHeToFill*R*T/self.tankSize)

    def getAirFillPressure(self):
        return self.pascalToBar((self.amountO2ToFill*R*T/self.tankSize)/self.fN_new)

    #General gas law in different forms
    def calcAmount(self, p, v):
        return p*v/(R*T)

    def calcPartialPressure(self, part, p):
        print "partial: %f" % (p*part)
        return p*part
