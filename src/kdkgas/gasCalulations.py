

R = 8314.0
T = 293.0

fO2_air = 0.21
fN_air = 0.79

vwCoeff_O2 = {"a":0.1378, "b":0.00003186}
vwCoeff_nitrox = {"a":0.1370, "b":0.0003870}
vwCoeff_helium = {"a":0.00346, "b":0.00002380}
vwCoeff_air = {"a":0.13725, "b":0.000372}

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
                                        tankSize *1e-3,
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
        
        N=self.calcAmount(self.pTank_old, self.tankSize, self.fO2_old, self.fHe_old)
        self.TankO2 = N*self.fO2_old
        self.TankN  = N*self.fN_old
        self.TankHe = N*self.fHe_old

        
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
        return (self.calcAmount(oldP, size, self.fO2_old, self.fHe_old) -
                self.calcAmount(newP, size, self.fO2_new, self.fHe_new))
        
    def calculateGasToFill(self):

        print "calc He"
        self.amountHeToFill = self.gas_ToFill(self.fHe_old, self.fHe_new)
        print "Calc O2"
        self.amountO2ToFill = self.gas_ToFill(self.fO2_old, self.fO2_new)
        print "calc N"
        self.amountNToFill  = self.gas_ToFill(self.fN_old,  self.fN_new)

        print "HE: %f, %f" % (self.amountHeToFill, self.fHe_new)
        print "O2: %f, %f" % (self.amountO2ToFill, self.fO2_new)
        print "O2: %f, %f" % (self.calcAmountReal(100*1e5, 12), self.molToLiter(self.calcAmountReal(100*1e5, 12)))
        print "N:  %f, %f" % (self.amountNToFill, self.fN_new)

        print "O2 press: %f" % self.calcPressure(self.tankSize,
                                                 self.amountO2ToFill, 1, 0)
        if self.amountO2ToFill < 0:
            raise GasCalcError("To much O2 in the tank!")
        if self.amountHeToFill < 0:
            raise GasCalcError("To much He in the tank!")
            

    def gas_ToFill(self, old_p, new_p):

        n_new = self.calcAmount(self.pTank_new, self.tankSize, self.fO2_new, self.fHe_new)
        
        if old_p == 0:
            n_old = 0
        else:
            n_old = self.calcAmount(self.pTank_old, self.tankSize, self.fO2_old, self.fHe_old) * old_p

        if new_p == 0:
            n_new = 0
        else:
            n_new = self.calcAmount(self.pTank_new,
                                    self.tankSize,
                                    self.fO2_new, 
                                    self.fHe_new) * new_p

        print "n_new: %f, n_old %f, new_p: %d" % ( n_new, n_old, new_p)
            
        return n_new - n_old                    

    #Calculates the end pressure when filling a Tank
    def getHeEndPressure(self, start_p):
        return start_p + self.getHeFillPressure()

    def getO2EndPressure(self, start_p):
        return start_p + self.getO2FillPressure()

    def getEndPressure(self, amount):
        if amount == 0:
            return 0
        p = self.calcPressure(self.tankSize, amount, self.fO2_new, self.fHe_new)
        self.pTank_new = self.pTank_old - p
        return self.pTank_new
        
    #Calculates how many bar the pressure in the tank must increase
    #for the necessary amount of Gas
    
    def getO2FillPressure(self):
        print "Flask tryck: %f" % self.pTank_new
        print "Flask Tryck: %f" % self.pTank_old
        print "luft  tryck: %f " % self.getAirFillPressure()
 
##        n_start = self.calcAmount(self.pTank_old, self.tankSize, self.TankO2, self.TankHe) * self.fN_old
##        n_tot = self.calcAmount(self.pTank_new, self.tankSize, self.TankHe) * self.fN_new

        o2_pre = (self.amountNToFill/0.79) * 0.21

        print "O2_pre %f" % o2_pre

        
        self.TankO2 = self.amountO2ToFill - o2_pre

        amount = self.TankO2 + self.TankN + self.TankHe

##        print "amount: %f" % amount
##        print "TankO2: %f" % self.TankO2
##        
##        print "amoun1t p: %f" % self.calcPressure(self.tankSize, self.TankO2,
##                                 (self.TankO2/amount) * 100,
##                                 (self.TankHe/amount) * 100)


        if self.TankHe == 0:
            fHe = 0
        else:
            fHe = self.TankHe/amount

        if self.amountO2ToFill == 0 or amount == 0:
            return 0

        print "amoun2t p: %f" % self.calcPressure(self.tankSize,
                                                 self.amountO2ToFill,
                                                 self.TankO2/amount,
                                                 self.TankHe/amount)

                                                 
        print "amount: %f" % amount

        if amount == 0:
            return 0

        print "self.TankHe: %f" % self.TankHe
        print "self.TankO2: %f" % (self.TankO2/amount * 100)
        return self.calcPressure(self.tankSize, self.TankO2,
                                 self.TankO2/amount,
                                 fHe)
    
    def getHeFillPressure(self):
        
        self.calculateGasToFill()
        if self.fHe_new == 0:
            return 0
        return self.amountHeToFill*R*T/self.tankSize

    def getAirFillPressure(self):
        return self.pTank_new

    #General gas law in different forms
    def calcAmountReal(self, p, v):
        return p*v/(R*T)

    def calcAmount(self, p, v, fO2, fHe):

        if p == 0:
            return 0
        #Start value
        n_start = p*v/(R*T);


        print "v: %f, n_start: %f, f=2: %f, fHe: %f" % (v, n_start, fO2, fHe)
        p_tst1 = self.calcPressure(v, n_start, fO2, fHe)


        if self.check_p(p_tst1, p):
            return n_start
        
        n_start_2 = n_start * 1.3
        p_tst2 = self.calcPressure(v, n_start_2, fO2, fHe)
        if self.check_p(p_tst1, p):
            return n_start


        #print "n_start: %f, n_start_2: %f, p_tst1: %f, p_tst2: %f" % (n_start, n_start_2, p_tst1, p_tst2)

        if p_tst1 < p and p_tst2 > p:
            return self.recCalcAmount(n_start, n_start_2, p, v, fO2, fHe)
        else:
            n_start_2 = n_start *0.5
            return self.recCalcAmount(n_start, p_tst1, n_start_2, p_tst2, p, v, fO2, fHe)


    def check_p(self, p1, p2):
        #print "p1/p2: %f" % abs(p1/p2)
        diff = abs(p1/p2)
        if (diff < 1.0001) and (diff > 0.9999) :
            #print "T"
            return True
        else:
            #print "F"
            return False

    def getAB(self, fO2, fHe):
 
        if fO2 == 1:
            return vwCoeff_O2
        elif self.fHe_new == 1:
            return vwCoeff_helium
        elif fO2 < 0.25 and fHe == 0:
            return vwCoeff_nitrox
        elif fHe == 0:
            return vwCoeff_air
            
    def recCalcAmount(self, n1, p1, n2, p2, p, v, fO2, fHe):

        vwCoeff = self.getAB(fO2, fHe)
        new_n = (n1 + n2) / 2
        new_p = self.calcPressure(v, new_n, fO2, fHe)

        if self.check_p(new_p, p):
            return new_n

        if new_p < p:
            #print "Other part"
            #print "new_n: %f, new_p: %f, n2: %f, p2: %f, p: %d, v: %d" % (new_n, new_p*1e-5, n2, p2*1e-5, p*1e-5, v)
            return self.recCalcAmount(n1, p1, new_n, new_p, p, v, fO2, fHe)
        else:
            #print "new_n: %f, new_p: %f, n2: %f, p2: %f, p: %d, v: %d" % (new_n, new_p*1e-5, n2, p2*1e-5, p*1e-5, v)
            return self.recCalcAmount(new_n, new_p, n2, p2, p, v, fO2, fHe)        
        
        
    def calcPressure_norm(self, v, n):
        # Allmanna gaslagen
        p = (R*T*n)/v
        return p

    def calcPressure(self, v, n, fO2, fHe):
        # Wan der wal

        if n == 0:
            return 0
##        print "fO2: %f" % fO2
##        print "fHe: %f" % fHe
        vwCoeff = self.getAB(fO2, fHe)
##        print vwCoeff
        
        p = ((R*T)/(v/n-vwCoeff["b"])) - (vwCoeff["a"] *(n/v)*(n/v))
        return p

    def calcPartialPressure(self, part, p):
##        print "p:   %d" % p
##        print "part %d" % part
##        print "partial: %f" % (p*part)
##        print
        return p*part


if __name__ == '__main__':

    print "Module test"
    t1 = Tank(0, 0.2,
              0, 0, 12,
              0, 200)
    g = GasCalculations(0.2, 0.2, 0, 0, 12, 10, 200)
    g_he = GasCalculations(0, 0, 0, 1, 12, 10, 200)
    g_nitrox = GasCalculations(0, 0.3, 0, 0, 12, 10, 200)
    g_o2 = GasCalculations(0, 1, 0, 0, 12, 10, 200)
    print g.getAB(0.2, 0)
    for i in range(10, 300, 10):
        n = g.calcAmountReal(i*1e5, 12)
        n1 = g.calcAmount(i*1e5, 12, 0.2, 0)
        p = g.calcPressure_norm(12, n)
        p1 = g.calcPressure(12, n1, 0.2, 0)
        print "n: %d, n1: %d, p: %d, p1: %f" % (n, n1, p*1e-5, p1*1e-5)
        
    print g_he.getAB(0, 1)
    for i in range(10, 300, 10):
        n = g_he.calcAmountReal(i*1e5, 12)
        n1 = g_he.calcAmount(i*1e5, 12, 0, 1)
        p = g_he.calcPressure_norm(12, n)
        p1 = g_he.calcPressure(12, n1, 0, 1)
        print "n: %d, n1: %d, p: %d, p1: %f" % (n, n1, p*1e-5, p1*1e-5)
        
    print g_o2.getAB(1, 0)
    for i in range(10, 300, 10):
        n = g_o2.calcAmountReal(i*1e5, 12)
        n1 = g_o2.calcAmount(i*1e5, 12,1 ,0)
        p = g_o2.calcPressure_norm(12, n)
        p1 = g_o2.calcPressure(12, n1, 1, 0)
        print "n: %d, n1: %d, p: %d, p1: %f" % (n, n1, p*1e-5, p1*1e-5)
    
