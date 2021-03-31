#coding:utf-8

from PyQt4 import QtGui,QtCore
import sys
reload(sys)

class SigSlot(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle(u'事件驱动测试')
        lcd = QtGui.QLCDNumber(self)
        slider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(slider)
        
        self.setLayout(vbox)
        self.connect(slider,QtCore.SIGNAL('valueChanged(int)'),lcd,QtCore.SLOT('display(int)'))
        self.resize(350,250)
        
app = QtGui.QApplication(sys.argv)
qb = SigSlot()
qb.show()
sys.exit(app.exec_())