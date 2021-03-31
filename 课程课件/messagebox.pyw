#-*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from PyQt4 import QtGui

class MessageBox(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setGeometry(300,300,350,250)
        self.setWindowTitle(u'消息窗口')
    
    def closeEvent(self,event):
        reply = QtGui.QMessageBox.question(self,u'警告',u'确认退出',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
app = QtGui.QApplication(sys.argv)
qb = MessageBox()
qb.show()
sys.exit(app.exec_())            
            
            
            
        