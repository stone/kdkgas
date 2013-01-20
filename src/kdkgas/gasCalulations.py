

R = 8314.0
T = 293.0

fO2_air = 0.21
fN_air = 0.79

class GasCalcError(Exception):
    pass

class Tank(object):
    def __init__(self, fO2_old, fO2_new,
                 fHe_old, fHe_new, tankSize,
                 pTank_old, pTank_new):
        
        self.gas_calc = GasCalculations(fO2_old,
                                        fO2_new,
                                        fHe_old,
                                        fHe_new,
                                        tankSize,
                                        self.barToPascal(pTank_old),
                                        self.barToPascal(pTank_new))
    
    def pascalToBar(self, pascal):
        return pascal*1e-5
    def barToPascal(self, bar):
        return bar*1e5

    def setStartPressure(self, p):
        self.gas_calc.pTank_old = self.barToPascal(p)
        
    def molToLiter(self, mol):
        return self.gas_calc.molToLiter(mol)

    def getTankPressure(self):
        return self.pascalToBar(self.gas_calc.getTankPressure())
 
    def getFilledHeGas(self):
        return self.gas_calc.getFilledHeGas()
 
    def getFilledO2Gas(self):
        return self.gas_calc.getFilledO2Gas()
    
    def getFilledGas(self, oldP, newP, size):
        oldP_pascal = self.barToPascal(oldP)
        newP_pascal = self.barToPascal(newP)
        return self.gas_calc.getFilledGas(oldP_pascal, newP_pascal, size)


    def getO2Fraction(self):
        return self.gas_calc.fO2_old
    def getHeFraction(self):
        return self.gas_calc.fHe_old
        
    def getO2FillPressure(self):
        return self.pascalToBar(self.gas_calc.getO2FillPressure())
    
    def getHeFillPressure(self):
        return self.pascalToBar(self.gas_calc.getHeFillPressure())

    def getAirFillPressure(self):
        return self.pascalToBar(self.gas_calc.getAirFillPressure())

    def getHeEndPressure(self, start_p):
        return self.pascalToBar(
            self.gas_calc.getHeEndPressure(self.barToPascal(start_p)))

    def getO2EndPressure(self, start_p):
        return self.pascalToBar(
            self.gas_calc.getO2EndPressure(self.barToPascal(start_p)))

    def getEndPressure(self, amount):
        return self.pascalToBar(self.gas_calc.getEndPressure(amount))

class GasCalculations(object):
    def __init__(self, fO2_old, fO2_new, fHe_old, fHe_new, tankSize, pTank_old, pTank_new):
        self.fO2_old = fO2_old
        self.fO2_new = fO2_new
        self.fHe_old = fHe_old
        self.fHe_new = fHe_new
        self.fN_old = 1 - fO2_old - fHe_old
        self.fN_new = 1 - fO2_new - fHe_new
        self.tankSize = tankSize
        self.pTank_old = pTank_old
        self.pTank_new =  pTank_new

    def molToLiter(self, mol):
        return mol*R*T/1e5

    def getTankPressure(self):
        return self.pTank_old
        
    def getFilledHeGas(self):
        self.calculateGasToFill()
        return self.amountHeToFill

    def getFilledO2Gas(self):
        self.calculateGasToFill()
        return self.amountO2ToFill

    def getFilledGas(self, oldP, newP, size):
        return (self.calcAmount(oldP, size) -
                self.calcAmount(newP, size))
        
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

    def getEndPressure(self, amount):
        p = self.calcPressure(self.pTank_old, self.tankSize, amount)
        self.pTank_new = self.pTank_old - p
        return self.pTank_new
        
    #Calculates how many bar the pressure in the tank must increase
    #for the necessary amount of Gas
    
    def getO2FillPressure(self):
        return (self.pTank_new - self.getHeFillPressure() -
                self.getAirFillPressure() - self.pTank_old)
    
    def getHeFillPressure(self):
        self.calculateGasToFill()
        return self.amountHeToFill*R*T/self.tankSize

    def getAirFillPressure(self):
        return (self.amountO2ToFill*R*T/self.tankSize)/self.fN_new

    #General gas law in different forms
    def calcAmount(self, p, v):
        return p*v/(R*T)

    def calcPressure(self, p, v, n):
        return (R*T*n)/v

    def calcPartialPressure(self, part, p):
##        print "p:   %d" % p
##        print "part %d" % part
##        print "partial: %f" % (p*part)
##        print
        return p*part
