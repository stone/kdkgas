# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addTank.ui'
#
# Created: Sat Sep 07 18:13:01 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_addTank(object):
    def setupUi(self, addTank):
        addTank.setObjectName("addTank")
        addTank.resize(305, 298)
        self.centralWidget = QtGui.QWidget(addTank)
        self.centralWidget.setObjectName("centralWidget")
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 71, 16))
        self.label.setObjectName("label")
        self.bottleSizeComboBox = QtGui.QComboBox(self.centralWidget)
        self.bottleSizeComboBox.setGeometry(QtCore.QRect(140, 60, 81, 22))
        self.bottleSizeComboBox.setObjectName("bottleSizeComboBox")
        self.label_2 = QtGui.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 91, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 46, 13))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(20, 140, 121, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtGui.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(20, 180, 71, 16))
        self.label_5.setObjectName("label_5")
        self.lastPressDateEdit = QtGui.QDateEdit(self.centralWidget)
        self.lastPressDateEdit.setGeometry(QtCore.QRect(140, 140, 110, 22))
        self.lastPressDateEdit.setObjectName("lastPressDateEdit")
        self.lastWashDateEdit = QtGui.QDateEdit(self.centralWidget)
        self.lastWashDateEdit.setGeometry(QtCore.QRect(140, 180, 110, 22))
        self.lastWashDateEdit.setObjectName("lastWashDateEdit")
        self.MaxPressComboBox = QtGui.QComboBox(self.centralWidget)
        self.MaxPressComboBox.setGeometry(QtCore.QRect(140, 100, 74, 22))
        self.MaxPressComboBox.setObjectName("MaxPressComboBox")
        self.OKPushButton = QtGui.QPushButton(self.centralWidget)
        self.OKPushButton.setGeometry(QtCore.QRect(40, 210, 75, 23))
        self.OKPushButton.setObjectName("OKPushButton")
        self.CancelPushButton = QtGui.QPushButton(self.centralWidget)
        self.CancelPushButton.setGeometry(QtCore.QRect(150, 210, 75, 23))
        self.CancelPushButton.setObjectName("CancelPushButton")
        self.NamelineEdit = QtGui.QLineEdit(self.centralWidget)
        self.NamelineEdit.setGeometry(QtCore.QRect(140, 30, 113, 20))
        self.NamelineEdit.setObjectName("NamelineEdit")
        addTank.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(addTank)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 305, 18))
        self.menuBar.setObjectName("menuBar")
        addTank.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(addTank)
        self.mainToolBar.setObjectName("mainToolBar")
        addTank.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(addTank)
        self.statusBar.setObjectName("statusBar")
        addTank.setStatusBar(self.statusBar)

        self.retranslateUi(addTank)
        QtCore.QMetaObject.connectSlotsByName(addTank)

    def retranslateUi(self, addTank):
        addTank.setWindowTitle(QtGui.QApplication.translate("addTank", "addCustomer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("addTank", "Flaskans namn namn", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("addTank", "Flaskans storlek", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("addTank", "max tryck", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("addTank", "Senaste provtryckning", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("addTank", "Senaste tvätt", None, QtGui.QApplication.UnicodeUTF8))
        self.OKPushButton.setText(QtGui.QApplication.translate("addTank", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelPushButton.setText(QtGui.QApplication.translate("addTank", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

