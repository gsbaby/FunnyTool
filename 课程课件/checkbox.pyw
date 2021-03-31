#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import sys

from PyQt4 import QtGui,QtCore
class CheckBox(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        
        self.setGeometry(300,300,250,150)
        self.setWindowTitle(u'单选框')
        
        self.cb = QtGui.QCheckBox(u'美女，选我啊',self)
        self.cb.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cb.move(10,10)
        self.connect(self.cb,QtCore.SIGNAL('stateChanged(int)'),self.changeTitle)
        
    def changeTitle(self,value):
        if self.cb.isChecked():
            self.setWindowTitle(u'单选框')
        else:
            self.setWindowTitle(u'没有选中')
            
            
app = QtGui.QApplication(sys.argv)
w = CheckBox()
w.show()
sys.exit(app.exec_())