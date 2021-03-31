#-*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from PyQt4 import QtGui

class Center(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle(u'居中')
        self.resize(550,450)
        self.center()
    
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)
        
        
app = QtGui.QApplication(sys.argv)
qb = Center()
qb.show()
sys.exit(app.exec_())