# -*- coding: cp1252 -*-
import sys
from PySide.QtGui import *
from PySide import QtCore
from mainWindow import Ui_MainWindow
from data_base_interface import *
from gasCalulations import *

enable = True
disable = False

max_pressure_list = {"200", "232", "300"}
bottle_size_list = {"4", "6", "7", "8", "10", "12", "14", "15", "24", "30"}

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.db = dataBaseInterface()

        # Fill GUI
        self.fillercomboBox.addItem("")
        for item in self.db.getFillers():
            self.fillercomboBox.addItem(item)

        self.gasBuyercomboBox.addItem("")
        for item in self.db.getBuyers():
            self.gasBuyercomboBox.addItem(item)

        for item in max_pressure_list:
            self.maxTryckcomboBox.addItem(item)

        self.FyllNrlabel.setText(str(self.db.getFillNr()))
        

        # Connect GUI actions with functions
        self.prCalcpushButton.clicked.connect(self.on_prCalcpushButton_clicked)
        self.startFillpushButton.clicked.connect(self.on_startFillpushButton_clicked)        
        self.AnalyzeReadypushButton.clicked.connect(self.on_analyzeReady_clicked)
        self.PaymentpushButton.clicked.connect(self.on_payment_clicked)
        
        self.gasBuyercomboBox.activated[str].connect(self.on_gasBuyercombBox_changed)
        self.tankNrcomboBox.activated[str].connect(self.on_tankNrcomboBox_changed)

        self.updateUiStart()

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
        
    def on_prCalcpushButton_clicked(self):

        # Check that all fields are filled in
        if self.fillercomboBox.currentText() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "Fyllare maste vara ifyllt")
            return

        if self.gasBuyercomboBox.currentText() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "Gaskopare maste vara ifyllt")
            return

        if self.bottleSizecomboBox.currentText() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "Flaskstorlek maste vara ifyllt")
            return

        if self.maxTryckcomboBox.currentText() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "Maxtrycket for flaskan maste vara ifyllt")
            return
        
        if self.finalPressurelineEdit.text() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "sluttrycket maste vara ifyllt")
            return
        
        if self.flaskTrycklineEdit.text() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "nuvarande tryck maste vara ifyllt")
            return
        if self.partialO2lineEdit.text() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "Nuvarande partialtryck for Oxygen maste vara ifyllt")
            return
        if self.PartialHelineEdit.text() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "Nuvarande partialtryck for Helium maste vara ifyllt")
            return
        
        if self.finalPHelineEdit.text() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "Onskat partialtryck for Helium maste vara ifyllt")
            return

        if self.finalPO2lineEdit.text() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "Onskat partialtryck for Oxygen maste vara ifyllt")
            return
        
        if self.bankHeTryckBeforelineEdit.text() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "Trycket i bankflaskan för Helium måste vara ifyllt")
            return
        
        if self.O2BankTryckBeforelineEdit.text() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "Trycket i bankflaskan för Oxygen måste vara ifyllt")
            return

        
        #Calculate how much gas shall be filled and in what order
        self.fO2_old = int(self.partialO2lineEdit.text()) * 0.01
        self.fHe_old = int(self.PartialHelineEdit.text()) * 0.01
        self.pTank_old = int(self.flaskTrycklineEdit.text())
        self.pHebank = int(self.O2BankTryckBeforelineEdit.text())
        self.pO2bank = int(self.O2BankTryckBeforelineEdit.text())
                        
        fO2_new   = int(self.finalPO2lineEdit.text()) * 0.01
        fHe_new   = int(self.finalPHelineEdit.text()) * 0.01
        pTank_new = int(self.finalPressurelineEdit.text())
        
        self.tankSize  = int(self.bottleSizecomboBox.currentText())
        try:
            self.gas_calc = GasCalculations(self.fO2_old, fO2_new,
                                   self.fHe_old, fHe_new,        
                                   self.tankSize, self.pTank_old, pTank_new)
        
            self.gas_calc.calculateGasToFill()
            HeFill_p = self.gas_calc.getHeFillPressure()
            self.HeFyllTryckHelabel.setText(str(int(HeFill_p)))
            
            O2Fill_p = self.gas_calc.getO2FillPressure()
            self.o2FyllTryckLabel.setText(str(int(O2Fill_p)))

            self.LuftFyllTrycklabel.setText(str(int(self.gas_calc.getAirFillPressure())))
                                            
            

        except GasCalcError as e:
            QMessageBox.information(self,
                    "QMessageBox.information()", str(e))
            return
        
        
        self.updateUiFill()

    def on_startFillpushButton_clicked(self):
        try:
            O2EndPressure = self.gas_calc.getO2EndPressure(int(self.flaskTrycklineEdit.text()))
            QMessageBox.information(self,
                                    "QMessageBox.information()",
                                    "Fyll Oxygen till %d Bar" % O2EndPressure)

            
            QMessageBox.information(self,
                                    "QMessageBox.information()",
                                    "Fyll Helium till %d Bar" % self.gas_calc.getHeEndPressure(O2EndPressure))

            QMessageBox.information(self,
                                    "QMessageBox.information()",
                                    "Fyll luft till %d Bar" % int(self.finalPressurelineEdit.text()))
          
            self.updateUiAfterFill()
            
        except GasCalcError as e:
            QMessageBox.information(self,
                    "QMessageBox.information()", str(e))
            
    def on_analyzeReady_clicked(self):

        if self.HeAnalyseratlineEdit.text() == "" and self.finalPHelineEdit.text() != str(0):
            QMessageBox.information(self,
                    "QMessageBox.information()", "Analyserat partialtryck for Helium maste vara ifyllt")
            return

        if self.luftAnalyseratlineEdit.text() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "Trycket i flaskan efter fyllning är inte ifyllt")
            return
        
        if self.O2AnalyseratlineEdit.text() == "":
            QMessageBox.information(self,
                    "QMessageBox.information()", "Analyserat partialtryck for Oxygen maste vara ifyllt")
            return

        #Calculate the amount of gas bought
        gas_calc = GasCalculations(self.fO2_old, int(self.O2AnalyseratlineEdit.text()) * 0.01,
                                   self.fHe_old, int(self.HeAnalyseratlineEdit.text()) * 0.01,        
                                   self.tankSize, self.pTank_old, int(self.luftAnalyseratlineEdit.text()))
        filledGas = gas_calc.getFilledGas()
        self.boughtO2MolLabel.setText(str(round(filledGas["O2"], 2)))
        self.boughtHeMolLlabel.setText(str(round(filledGas["He"], 2)))

        self.boughtO2label.setText(str(int(gas_calc.molToLiter(filledGas["O2"]))))
        self.boughtHelabel.setText(str(int(gas_calc.molToLiter(filledGas["He"]))))
        

        #Calculate the price
        HeCost = filledGas["He"] * self.db.getHePrice()
        O2Cost = filledGas["O2"] * self.db.getO2Price()
        self.Prislabel.setText(str(round(HeCost + O2Cost, 2)))
        
        self.updateUiAfterAnalyze()

    def on_payment_clicked(self):

        self.updateUiFill()
        
    def on_gasBuyercombBox_changed(self, arg):        
        for item in self.db.getBottles(arg):
            self.tankNrcomboBox.addItem(item)
        
        self.updateUiStart()

    def on_tankNrcomboBox_changed(self, arg):
        size = self.db.getBottleSize(arg,self.gasBuyercomboBox.currentText())
        self.bottleSizecomboBox.setCurrentIndex(self.bottleSizecomboBox.findText(size))
        max_press = self.db.getBottleMaxPress(arg,self.gasBuyercomboBox.currentText())
        self.maxTryckcomboBox.setCurrentIndex(self.maxTryckcomboBox.findText(max_press))
        self.finalPressurelineEdit.insert(max_press)
                                            


       
app = QApplication(sys.argv)
frame = MainWindow()
frame.show()    
app.exec_()


