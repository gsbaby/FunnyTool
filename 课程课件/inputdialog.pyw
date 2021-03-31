#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from PyQt4 import QtGui,QtCore

class InputDialog(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self)
        
        self.setGeometry(300,300,350,80)
        self.setWindowTitle(u'输入对话框')
        self.button = QtGui.QPushButton(u'对话',self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(20,20)
        self.connect(self.button,QtCore.SIGNAL('clicked()'),self.showDialog)
        self.setFocus()
        
        self.label = QtGui.QLineEdit(self)
        self.label.move(130,22)
    
    def showDialog(self):
        text, ok = QtGui.QInputDialog.getText(self,u'输入对话框',u'输入姓名：')
        
        if ok :
            self.label.setText(unicode(text))

app = QtGui.QApplication(sys.argv)
icon = InputDialog()
icon.show()
sys.exit(app.exec_())