# -*- coding: cp1252 -*-
import sys
from PySide.QtGui import *
from PySide import QtCore
from kdkgas.mainWindow import Ui_MainWindow
from kdkgas.addTank import Ui_addTank
from kdkgas.gasdb import *
from kdkgas.gasCalulations import *


enable = True
disable = False

max_pressure_list = {"200", "232", "300"}
bottle_size_list = {"4", "6", "7", "8", "10", "12", "14", "15", "24", "30"}

class addTankWindow(QMainWindow, Ui_addTank):
    def __init__(self, parent=None):
        super(addTankWindow, self).__init__(parent)
        self.setupUi(self)

        
        # Connect GUI actions with functions
        self.OKPushButton.clicked.connect(self.OKButton_clicked)
        self.CancelPushButton.clicked.connect(self.cancelPushButton_clicked)

        # Fill GUI
        for item in max_pressure_list:
            self.MaxPressComboBox.addItem(item)

        for item in bottle_size_list:
            self.bottleSizeComboBox.addItem(item)

    def get_db(self, big_db):
        self.db = big_db;
    
    def message(self, string):
        QMessageBox.information(self,
                                "kdkGas information", string)

    def checkForEmpty(self, string, obj):

        if isinstance(obj, QComboBox):
            check = obj.currentText()
        elif isinstance(obj, QLineEdit):
            check = obj.text()
            
        if check == "":
            self.message(string)
            obj.setFocus()
            return True
        else:
            return False
            
    def OKButton_clicked(self):
        try:
            # Check that all fields are filled in
            if self.checkForEmpty("Flaskans namn (ID) m�ste vara ifyllt", self.NamelineEdit):
                return
            if self.checkForEmpty("Sorleken p� flaskan m�ste vara ifyllt", self.bottleSizeComboBox):
                return
            if self.checkForEmpty("Flaskans arbetstryck m�ste vara ifyllt", self.MaxPressComboBox):
                return

            if self.db.addTank(self.NamelineEdit.text().strip(), self.bottleSizeComboBox.currentText(),
                                self.MaxPressComboBox.currentText()):
                self.setVisible(False)
            else:
                self.message("Flaskan finns redan i databasen, byt namn p� flaskan.")

            
        except Exception as e:
            self.message(str(e))

        
    def cancelPushButton_clicked(self):
        self.setVisible(False)
    
class MainWindow(QMainWindow, Ui_MainWindow):
    try:
        def __init__(self, child, parent=None):
            super(MainWindow, self).__init__(parent)
            self.setupUi(self)

            self.db = dataBaseInterface()
            child.get_db(self.db)

            # Create actions
            exitAction = QAction('&Exit', self)
            exitAction.setShortcut('Ctrl+Q')
            exitAction.setStatusTip('Exit application')
            exitAction.triggered.connect(self.close)

            
            #Add file menu
            fileMenu = self.menuBar.addMenu('&File')
            fileMenu.addAction(exitAction)

            self.addDbActions()
        
            # Fill GUI
            self.fillercomboBox.addItem("")
            for item in self.db.getFillers():
                self.fillercomboBox.addItem(item)

            self.gasBuyercomboBox.addItem("")
            for item in self.db.getBuyers():
                self.gasBuyercomboBox.addItem(item)

            for item in max_pressure_list:
                self.maxTryckcomboBox.addItem(item)

            self.HeBankVolymlineEdit.setText(str(self.db.getHeBankVolume()))     
            self.bankHeTryckBeforelineEdit.setText(str(self.db.getHeBankPressure()))
                                                           
            self.O2BankVolymlineEdit.setText(str(self.db.getO2BankVolume()))                                         
            self.O2BankTryckBeforelineEdit.setText(str(self.db.getO2BankPressure()))

            self.FyllNrlabel.setText(self.db.getFillNr())
            

            # Connect GUI actions with functions
            self.prCalcpushButton.clicked.connect(self.on_prCalcpushButton_clicked)
            self.startFillpushButton.clicked.connect(self.on_startFillpushButton_clicked)        
            self.AnalyzeReadypushButton.clicked.connect(self.on_analyzeReady_clicked)
            self.PaymentpushButton.clicked.connect(self.on_payment_clicked)
            
            self.gasBuyercomboBox.activated[str].connect(self.on_gasBuyercombBox_changed)
            self.tankNrcomboBox.activated[str].connect(self.on_tankNrcomboBox_changed)

            #Set the tab order
            #QGraphicsWidget.setTabOrder(self.fillercomboBox, self.gasBuyercomboBox)
            #QGraphicsWidget.setTabOrder(self.gasBuyercomboBox, bottleSizecomboBox)
            
            
            self.updateUiStart()

        def addDbActions(self):            
            addFillerAction = QAction('&Addera gas blandare', self)
            addFillerAction.setStatusTip('Lagg till en person som kan blanda gas')
            addFillerAction.triggered.connect(self.addFiller)

            addBuyerAction = QAction('Addera gaskopare', self)
            addBuyerAction.setStatusTip('Lagg till en person som kan kopa gas')
            addBuyerAction.triggered.connect(self.addByuer)

            addTankAction = QAction('Ny flaska', self)
            addTankAction.setStatusTip('Lagg till en ny flaska')
            addTankAction.triggered.connect(self.addTank)

            TankToCustomerAction = QAction('Koppla kund till Flask', self)
            TankToCustomerAction.setStatusTip('L�t kunden kunna k�pa gas till en till flaska')
            TankToCustomerAction.triggered.connect(self.TankToCustomer)
            

            #Add databas menu
            dbMenu = self.menuBar.addMenu('&Databas')
            dbMenu.addAction(addFillerAction)
            dbMenu.addAction(addBuyerAction)
            dbMenu.addAction(addTankAction)
            dbMenu.addAction(TankToCustomerAction)

        def addFiller(self):
            text, ok = QInputDialog.getText(self, 'Input Dialog', 
            'Blenders namn:')
        
            if ok:
                if not self.db.addBlender(str(text).strip()):
                    self.message("Namnet finns redan som 'blender' i databasen, v�lj ett annat namn")
                    return
                
                for i in range(0, self.fillercomboBox.count()):
                    self.fillercomboBox.removeItem(0)
                self.fillercomboBox.addItem("")
                for item in self.db.getFillers():
                    self.fillercomboBox.addItem(item)
                
            
                
        def addByuer(self):
            text, ok = QInputDialog.getText(self, 'Input Dialog', 
            'K�parens namn:')
        
            if ok:
                if self.db.addCustomer(str(text).strip()):
                    for i in range(0, self.gasBuyercomboBox.count()):
                        self.gasBuyercomboBox.removeItem(0)
                    self.gasBuyercomboBox.addItem("")
                    for item in self.db.getBuyers():
                        self.gasBuyercomboBox.addItem(item)
                else:
                    self.message ("Kunden finns redan i databasen, v�lj ett annat namn")
            else:
                self.message("Kunden kunde inte l�gags till databasen")
            
            
        def addTank(self):
            tankFrame.show()        

        def TankToCustomer(self):
            if self.checkForEmpty("Gaskund maste vara ifyllt", self.gasBuyercomboBox):
                return

            customer = self.gasBuyercomboBox.currentText().strip()

            bottleList = self.db.getAllBottles()
            bottle = QInputDialog.getItem(self, 'V�lj flaska dialog', 'V�lj flask', bottleList)
            if bottle[1]:
                bottle = str(bottle[0]).strip()
                if self.db.addBottleToCustomer(bottle, customer):
                    for i in range(0, self.tankNrcomboBox.count()):
                        self.tankNrcomboBox.removeItem(0)
                    for item in self.db.getBottles(customer):
                        self.tankNrcomboBox.addItem(item)
            else:
                message("Denna flaska kan redan fyllas av den h�r kunden!")
        
            
        def updateUiStart(self):
            self.prCalcpushButton.setEnabled(enable)
            self.PaymentpushButton.setEnabled(disable)
            self.AnalyzeReadypushButton.setEnabled(disable)
            self.startFillpushButton.setEnabled(disable)
                
        def updateUiFill(self):
            self.prCalcpushButton.setEnabled(enable)
            self.PaymentpushButton.setEnabled(disable)
            self.AnalyzeReadypushButton.setEnabled(disable)
            self.startFillpushButton.setEnabled(enable)
            self.FyllNrlabel.setText(self.db.getFillNr())

        def updateUiAfterFill(self):
            self.prCalcpushButton.setEnabled(disable)
            self.PaymentpushButton.setEnabled(disable)
            self.AnalyzeReadypushButton.setEnabled(enable)
            self.startFillpushButton.setEnabled(disable)

        def updateUiAfterAnalyze(self):
            self.prCalcpushButton.setEnabled(disable)
            self.PaymentpushButton.setEnabled(enable)
            self.AnalyzeReadypushButton.setEnabled(disable)
            self.startFillpushButton.setEnabled(disable)

        def message(self, string):
            QMessageBox.information(self,
                                   "kdkGas information", string)

        def checkForEmpty(self, string, obj):

            if isinstance(obj, QComboBox):
                check = obj.currentText()
            elif isinstance(obj, QLineEdit):
                check = obj.text()
                
            if check == "":
                self.message(string)
                obj.setFocus()
                return True
            else:
                return False
                
        def on_prCalcpushButton_clicked(self):

            # Check that all fields are filled in
            if self.checkForEmpty("Fyllare maste vara ifyllt", self.fillercomboBox):
                return

            if self.checkForEmpty("Gaskopare maste vara ifyllt", self.gasBuyercomboBox):
                return

            if self.checkForEmpty("Flaskstorlek maste vara ifyllt", self.bottleSizecomboBox):
                return

            if self.checkForEmpty("Maxtrycket for flaskan maste vara ifyllt", self.maxTryckcomboBox):
                self.maxTryckcomboBox.setFocus()
                return
                
            if self.checkForEmpty("sluttrycket maste vara ifyllt", self.finalPressurelineEdit):
                self.finalPressurelineEdit.setFocus()
                return

            if self.checkForEmpty("nuvarande tryck maste vara ifyllt", self.flaskTrycklineEdit):
                self.flaskTrycklineEdit.setFocus()
                return

            if self.checkForEmpty("Nuvarande partialtryck for Oxygen maste vara ifyllt",
                                  self.partialO2lineEdit):
                self.partialO2lineEdit.setFocus()
                return

            if self.checkForEmpty("Nuvarande partialtryck for Helium maste vara ifyllt",
                                      self.PartialHelineEdit):
                self.PartialHelineEdit.setFocus()
                return

            if self.checkForEmpty("Onskat partialtryck for Helium maste vara ifyllt",
                                      self.finalPHelineEdit):
                return

            if self.checkForEmpty("Onskat partialtryck for Oxygen maste vara ifyllt",
                                      self.finalPO2lineEdit):
                return
                
            if self.checkForEmpty("Trycket i bankflaskan f�r Helium m�ste vara ifyllt",
                                      self.bankHeTryckBeforelineEdit):
                return

            if self.checkForEmpty("Trycket i bankflaskan f�r Oxygen m�ste vara ifyllt",
                                      self.O2BankTryckBeforelineEdit):
                return

            
            #Calculate how much gas shall be filled and in what order
            self.fO2_old = int(self.partialO2lineEdit.text()) * 0.01
            self.fHe_old = int(self.PartialHelineEdit.text()) * 0.01
            self.pTank_old = int(self.flaskTrycklineEdit.text())
            self.pHebank = int(self.bankHeTryckBeforelineEdit.text())
            self.pO2bank = int(self.O2BankTryckBeforelineEdit.text())
            self.O2BankSize = int(self.O2BankVolymlineEdit.text())
            self.HeBankSize = int(self.HeBankVolymlineEdit.text())

            self.customer = self.gasBuyercomboBox.currentText()
            self.filler   = self.fillercomboBox.currentText()
                            
            fO2_new   = int(self.finalPO2lineEdit.text()) * 0.01
            fHe_new   = int(self.finalPHelineEdit.text()) * 0.01
            pTank_new = int(self.finalPressurelineEdit.text())
                
            self.tankSize  = int(self.bottleSizecomboBox.currentText())
            try:
                self.gas_calc = Tank(self.fO2_old, fO2_new,
                                       self.fHe_old, fHe_new,        
                                       self.tankSize, self.pTank_old, pTank_new)
            

                HeFill_p = self.gas_calc.getHeFillPressure()
                self.HeFyllTryckHelabel.setText(str(int(HeFill_p)))
                
                O2Fill_p = self.gas_calc.getO2FillPressure()
                self.o2FyllTryckLabel.setText(str(int(O2Fill_p)))

                self.LuftFyllTrycklabel.setText(str(int(self.gas_calc.getAirFillPressure())))
                                       
                print "self.HeBankSize: %f" %  self.HeBankSize
                print "self.pHebank: %f" %  self.pHebank
                
                self.HeTank = Tank(0, 0, 1, 1, self.HeBankSize, self.pHebank, 0)
                self.O2Tank = Tank(1, 1, 0, 0, self.O2BankSize, self.pO2bank, 0)
            except GasCalcError as e:
                self.message(str(e))
                return
                
            
            self.updateUiFill()

        def on_startFillpushButton_clicked(self):
            try:

                     
                O2BankEndPressure = self.O2Tank.getEndPressure(self.gas_calc.getFilledO2Gas());
                HeBankEndPressure = self.HeTank.getEndPressure(self.gas_calc.getFilledHeGas());
                
                O2EndPressure = self.gas_calc.getO2EndPressure(self.gas_calc.getTankPressure())
                HeEndPressure = self.gas_calc.getHeEndPressure(O2EndPressure)

                # Calculate minimum possible start pressure
                minP = int(self.o2FyllTryckLabel.text()) + int(self.HeFyllTryckHelabel.text())
                

                print "O2BankEndPressure: %d" % O2BankEndPressure
                print "O2BankEndPressure: " + self.o2FyllTryckLabel.text()
                if O2BankEndPressure < int(self.o2FyllTryckLabel.text()):
                    self.message("Trycket i oxygen bankflaskan ar for lagt for att kunna fylla dykflaskan!")
                    self.updateUiStart()
                    return
                
                if HeBankEndPressure < int(self.HeFyllTryckHelabel.text()):
                    self.message("Trycket i Helium bankflaskan ar for lagt for att kunna fylla dykflaskan!")
                    self.updateUiStart()
                    return

                if minP > O2BankEndPressure + HeBankEndPressure:
                    self.message("Trycket i bankflaskorna ar for lagt for att kunna fylla dykflaskan!")
                    
                    self.updateUiStart()
                    return
                
                #Calculate if any gas must be dumped
                dump = False
                min_start = self.gas_calc.getTankPressure()

                if self.gas_calc.getO2FillPressure() < 0:
                    min_start = self.gas_calc.getEndPressure(self.gas_calc.getFilledO2Gas());
                    dump = True

                if self.gas_calc.getHeFillPressure() < 0:
                    He_min_start = self.gas_calc.getEndPressure(self.gas_calc.getFilledHeGas());
                    dump = True
                    if He_min_start < min_start:
                        min_start = He_min_start
                        
                
                if (O2BankEndPressure < HeBankEndPressure) and self.fHe_old != 0:

                    #Start with O2, since it has the lowest end pressure in this case
                    if O2BankEndPressure < O2EndPressure:
                        O2min_start = O2BankEndPressure - self.gas_calc.getO2FillPressure()
                        dump = True
                        if O2min_start < min_start:
                            min_start = O2min_start
                        
                    if HeBankEndPressure < (min_start + self.gas_calc.getO2FillPressure() +
                                            self.gas_calc.getHeFillPressure()):
                        min_start = (HeBankEndPressure - self.gas_calc.getO2FillPressure() -
                                     self.gas_calc.getHeFillPressure())
                        dump = True

                elif self.fHe_old != 0:
                    #Start with He, since it has the lowest end pressure in this case
                    
                    HeEndPressure = self.gas_calc.getO2EndPressure(self.gas_calc.getTankPressure())
                    O2EndPressure = self.gas_calc.getHeEndPressure(HeEndPressure)
                    
                    if HeBankEndPressure < HeEndPressure:
                        Hemin_start= HeBankEndPressure - self.gas_calc.getHeFillPressure()
                        if Hemin_start < min_start:
                            min_start = Hemin_start
                        dump = True

                    if O2BankEndPressure < (min_start + self.gas_calc.getHeFillPressure() +
                                            self.gas_calc.getO2FillPressure()) :
                        min_start = (O2BankEndPressure - self.gas_calc.getHeFillPressure() -
                                     self.gas_calc.getO2FillPressure())
                        dump = True

                else: 
                    #Start with O2, since it has the lowest end pressure in this case
                    if O2BankEndPressure < O2EndPressure:
                        O2min_start = O2BankEndPressure - self.gas_calc.getO2FillPressure()
                        dump = True
                        if O2min_start < min_start:
                            min_start = O2min_start

                if dump:
                    self.message("Slapp ut gas till %d Bar �r kvar i flaskan och starta sedan om fyllningen" % min_start)
                    self.gas_calc.setStartPressure(min_start)                   
                    O2EndPressure = self.gas_calc.getO2EndPressure(self.gas_calc.getTankPressure())
                    HeEndPressure = self.gas_calc.getHeEndPressure(O2EndPressure)
                    
                    self.updateUiStart()
                    return
                    
                if (O2BankEndPressure < HeBankEndPressure) and self.fHe_old != 0:                   
                    O2EndPressure = self.gas_calc.getO2EndPressure(self.gas_calc.getTankPressure())
                    HeEndPressure = self.gas_calc.getHeEndPressure(O2EndPressure)   
                    self.message("Fyll Oxygen till %d Bar" % O2EndPressure)                
                    self.message("Fyll Helium till %d Bar" % self.gas_calc.getHeEndPressure(O2EndPressure))
                    self.message("Fyll luft till %d Bar" % int(self.finalPressurelineEdit.text()))
                    filledHe = gas_calc.getFilledHeGas()
                    filledO2 = gas_calc.getFilledO2Gas() 
                    self.db.write_filled_gas(self.filler, self.customer,
                                             self.gas_calc.filledO2Gas(), self.gas_calc.filledHeGas())
                elif  self.fHe_old != 0:                   
                    HeEndPressure = self.gas_calc.getHeEndPressure(self.gas_calc.getTankPressure())
                    O2EndPressure = self.gas_calc.getHeEndPressure(HeEndPressure)   
                    self.message("Fyll Helium till %d Bar" % HeEndPressure)                
                    self.message("Fyll Oxygen till %d Bar" % O2EndPressure)
                    self.message("Fyll luft till %d Bar" % int(self.finalPressurelineEdit.text()))
                    filledHe = gas_calc.getFilledHeGas()
                    filledO2 = gas_calc.getFilledO2Gas() 
                    self.db.write_filled_gas(self.filler, self.customer,
                                             self.gas_calc.filledO2Gas(), self.gas_calc.filledHeGas())

                else:
                    O2EndPressure = self.gas_calc.getHeEndPressure(HeEndPressure)   
                    self.message("Fyll Oxygen till %d Bar" % O2EndPressure)
                    self.message("Fyll luft till %d Bar" % int(self.finalPressurelineEdit.text()))
                    filledHe = self.gas_calc.getFilledHeGas()
                    filledO2 = self.gas_calc.getFilledO2Gas() 
                    self.db.write_filled_gas(self.filler, self.customer,
                                             self.gas_calc.filledO2Gas(), self.gas_calc.filledHeGas())


                
                self.O2AnalyseratlineEdit.setFocus()
                
              
                self.updateUiAfterFill()
                
            except GasCalcError as e:
                self.message(str(e))
                    
        def on_analyzeReady_clicked(self):

            if self.HeAnalyseratlineEdit.text() == "" and self.finalPHelineEdit.text() != str(0):
                self.message("Analyserat partialtryck for Helium maste vara ifyllt")
                self.HeAnalyseratlineEdit.setFocus()
                return

            if self.checkForEmpty("Trycket i flaskan efter fyllning �r inte ifyllt",
                                  self.luftAnalyseratlineEdit):
                return
            
            if self.checkForEmpty("Analyserat partialtryck for Oxygen maste vara ifyllt",
                                  self.O2AnalyseratlineEdit):
                return

            if self.checkForEmpty("Trycket efter fyllning f�r Helium bank flaskan maste vara ifyllt",
                                  self.HeBankTryckAfterlineEdit):
                return
            
            if self.checkForEmpty("Trycket efter fyllning f�r Oxygen bank flaskan maste vara ifyllt",
                                  self.O2BankTryckAfterlineEdit):
                return
                    

            #Calculate the amount of gas bought
            gas_calc = Tank(self.fO2_old, int(self.O2AnalyseratlineEdit.text()) * 0.01,
                                       self.fHe_old, int(self.HeAnalyseratlineEdit.text()) * 0.01,        
                                       self.tankSize, self.pTank_old, int(self.luftAnalyseratlineEdit.text()))
            filledHe = gas_calc.getFilledHeGas()
            filledO2 = gas_calc.getFilledGas(self.pO2bank,
                                             int(self.O2BankTryckAfterlineEdit.text()),
                                             int(self.O2BankVolymlineEdit.text()))   

                    
            self.boughtO2MolLabel.setText(str(round(filledO2, 2)))
            self.boughtHeMolLlabel.setText(str(round(filledHe, 2)))

            self.boughtO2label.setText(str(int(gas_calc.molToLiter(filledO2))))
            self.boughtHelabel.setText(str(int(gas_calc.molToLiter(filledHe))))
            

            #Calculate the price
            HeCost = filledHe * int(self.db.getHePrice()) * 0.01
            O2Cost = filledO2 * int(self.db.getO2Price()) * 0.01
            tot_cost = str(round(HeCost + O2Cost, 2))
            self.Prislabel.setText(tot_cost) 

            self.db.writeAnalyzedGas(self.O2AnalyseratlineEdit.text(), str(round(filledO2, 2)),
                                     self.HeAnalyseratlineEdit.text(), str(round(filledHe, 2)),
                                     tot_cost, self.tankName)
                                             
                
            self.updateUiAfterAnalyze()

        def on_payment_clicked(self):

            self.bankHeTryckBeforelineEdit.setText(self.HeBankTryckAfterlineEdit.text())
            self.O2BankTryckBeforelineEdit.setText(self.O2BankTryckAfterlineEdit.text())
            self.HeBankTryckAfterlineEdit.setText("")
            self.O2BankTryckAfterlineEdit.setText("")

            self.O2AnalyseratlineEdit.setText("")
            self.HeAnalyseratlineEdit.setText("")
            self.luftAnalyseratlineEdit.setText("")
            
            self.db.moneyToPay(self.Prislabel.text(), self.customer)
            self.gasBuyercomboBox.setFocus()

            
            
            self.updateUiFill()
                
        def on_gasBuyercombBox_changed(self, arg):        
            for item in self.db.getBottles(arg):
                self.tankNrcomboBox.addItem(item)
            
            self.updateUiStart()

        def on_tankNrcomboBox_changed(self, arg):
            size = self.db.getBottleSize(arg)
            self.tankName = arg.strip()
            self.bottleSizecomboBox.setCurrentIndex(self.bottleSizecomboBox.findText(size))
            max_press = self.db.getBottleMaxPress(arg,self.gasBuyercomboBox.currentText())
            self.maxTryckcomboBox.setCurrentIndex(self.maxTryckcomboBox.findText(max_press))
            self.finalPressurelineEdit.insert(max_press)
                                                
    except Exception as e:
        self.message(str(e))

       
app = QApplication(sys.argv)
tankFrame = addTankWindow()
frame = MainWindow(tankFrame)  
frame.show()    
app.exec_()


