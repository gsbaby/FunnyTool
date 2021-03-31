from PyQt4 import QtGui
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Boxlayout(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self)
        
        self.setWindowTitle(u'Box布局')
        
        ok = QtGui.QPushButton(u'确定')
        cancel = QtGui.QPushButton(u'取消')
        
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok)
        hbox.addWidget(cancel)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        self.resize(400,250)
        
app = QtGui.QApplication(sys.argv)
qb = Boxlayout()
qb.show()
sys.exit(app.exec_())