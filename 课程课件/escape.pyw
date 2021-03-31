#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from PyQt4 import QtGui,QtCore

class Escape(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self)
        
        self.setWindowTitle(u'重写')
        self.resize(350,250)
        self.connect(self,QtCore.SIGNAL('closeEmitAPP()'),QtCore.SLOT('close()'))
        
    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
            
app = QtGui.QApplication(sys.argv)
qb = Escape()
qb.show()
sys.exit(app.exec_())