#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from PyQt4 import QtGui,QtCore

class OpenFile(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        
        self.setGeometry(300,300,350,300)
        self.setWindowTitle(u'打开文件')
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()
        self.setFocus()
        
        exit = QtGui.QAction(QtGui.QIcon('open.ico'),u'打开',self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip(u'打开新文件')
        
        self.connect(exit,QtCore.SIGNAL('triggered()'),self.showDialog)
        
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)
        
    def showDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,u'打开文件','./')
        file = open(filename)
        data = file.read()
        self.textEdit.setText(data)

app = QtGui.QApplication(sys.argv)
cd = OpenFile()
cd.show()
sys.exit(app.exec_())        