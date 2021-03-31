# -*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from PyQt4 import QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self)
        
        self.resize(350,250)
        self.setWindowTitle(u'状态栏')
        self.statusBar().showMessage(u'准备好啦')

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())        
   