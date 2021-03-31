from PyQt4 import QtGui,QtCore
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self)
        self.resize(350,250)
        self.setWindowTitle(u'工具栏')
        
        self.exit = QtGui.QAction(QtGui.QIcon('exit.png'),u'退出',self)
        self.exit.setShortcut('Ctrl+Q')
        self.connect(self.exit,QtCore.SIGNAL('triggered()'),QtGui.qApp,QtCore.SLOT('quit()'))
        self.toolbar = self.addToolBar(u'退出')
        self.toolbar.addAction(self.exit)

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())


