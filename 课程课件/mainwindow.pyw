from PyQt4 import QtGui,QtCore
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self)
        
        self.resize(350,250)
        self.setWindowTitle(u'主界面')
        
        textEdit = QtGui.QTextEdit()
        self.setCentralWidget(textEdit)
        
        exit = QtGui.QAction(QtGui.QIcon('exit.png'),u'退出',self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip(u'退出程序')
        self.connect(exit,QtCore.SIGNAL('triggered()'),QtGui.qApp,QtCore.SLOT('quit()'))
        
        self.statusBar()
        
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)
        
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit)
        
app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())