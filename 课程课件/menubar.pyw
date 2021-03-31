# -*- coding=utf-8 -*-

from PyQt4 import QtGui,QtCore
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent = None):
        QtGui.QMainWindow.__init__(self)
        
        self.resize(350, 250)
        self.setWindowTitle(u'菜单')
        
        exit = QtGui.QAction(QtGui.QIcon('exit.png'), u'退出', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip(u'退出程序')
        exit.connect(exit,QtCore.SIGNAL('triggered()'),QtGui.qApp,QtCore.SLOT('quit()'))
        
        self.statusBar()
        
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)
        
app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())