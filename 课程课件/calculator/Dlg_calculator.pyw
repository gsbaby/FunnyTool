# -*- coding: utf-8 -*-

"""
Module implementing Dlg_calculator.
"""

#from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QDialog

from Ui_calculator_ui import Ui_Dialog
from PyQt4 import QtGui,  QtCore
import sys


class Dlg_calculator(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    lcdstring = ''
    operation = ''
    currentNum = 0
    previousNum = 0
    result = 0
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.action()
        
    def action(self):
        #定义按下数字执行的方法
        self.connect(self.b0, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b1, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b2, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b3, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b4, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b5, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b6, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b7, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b8, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b9, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.point, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        
        #定义按下操作符执行的方法
        self.connect(self.b_plus, QtCore.SIGNAL('clicked()'), self.opClicked)
        self.connect(self.b_sub, QtCore.SIGNAL('clicked()'), self.opClicked)
        self.connect(self.b_mul, QtCore.SIGNAL('clicked()'), self.opClicked)
        self.connect(self.b_div, QtCore.SIGNAL('clicked()'), self.opClicked)
        
        #定义按下清除键执行的方法
        self.connect(self.b_clear, QtCore.SIGNAL('clicked()'), self.clrClicked)
        
       #定义按下等于号执行的方法
        self.connect(self.b_eq, QtCore.SIGNAL('clicked()'), self.eqClicked)
        
    def buttonClicked(self):
        if len(Dlg_calculator.lcdstring) <= 7:
            Dlg_calculator.lcdstring = Dlg_calculator.lcdstring + self.sender().text()
            if Dlg_calculator.lcdstring == '.':
                Dlg_calculator.lcdstring = '0.'
            else:
                if str(Dlg_calculator.lcdstring).count('.') > 1:
                    Dlg_calculator.lcdstring = str(Dlg_calculator.lcdstring)[:-1]
                else:
                    self.lcd.display(Dlg_calculator.lcdstring)
                    Dlg_calculator.currentNum = float(Dlg_calculator.lcdstring)
        else:
            pass

    def opClicked(self):
        Dlg_calculator.previousNum = Dlg_calculator.currentNum
        Dlg_calculator.currentNum = 0
        Dlg_calculator.lcdstring = ''
        Dlg_calculator.operation = self.sender().objectName()

    def clrClicked(self):
        Dlg_calculator.lcdstring = ''
        Dlg_calculator.currentNum = 0
        Dlg_calculator.previousNum = 0
        self.lcd.display(0)
    
    def eqClicked(self):
        if Dlg_calculator.operation == 'b_plus':
            Dlg_calculator.result = Dlg_calculator.previousNum + Dlg_calculator.currentNum
            self.lcd.display(Dlg_calculator.result)
        
        elif Dlg_calculator.operation == 'b_sub':
            Dlg_calculator.result = Dlg_calculator.previousNum - Dlg_calculator.currentNum
            self.lcd.display(Dlg_calculator.result)
            
        elif Dlg_calculator.operation == 'b_mul':
            Dlg_calculator.result = Dlg_calculator.previousNum * Dlg_calculator.currentNum  
            self.lcd.display(Dlg_calculator.result)  
    
        elif Dlg_calculator.operation == 'b_div':
            if Dlg_calculator.currentNum == 0:
                self.lcd.display('Error')  
                Dlg_calculator.result = 0
                Dlg_calculator.previousNum = 0
            else:
                Dlg_calculator.result = Dlg_calculator.previousNum / Dlg_calculator.currentNum
                self.lcd.display(Dlg_calculator.result)
        
        Dlg_calculator.currentNum = Dlg_calculator.result
        Dlg_calculator.lcdstring = ''
    
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, u'警告', u'确认退出', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mycal = Dlg_calculator()
    mycal.show()
    sys.exit(app.exec_())
