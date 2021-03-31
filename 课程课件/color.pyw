#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from PyQt4 import QtGui, QtCore

class ColorDialog(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self)
        color = QtGui.QColor(255, 255, 255)
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle(u'颜色选择盘')
        self.button = QtGui.QPushButton(u'选择颜色', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(20, 20)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.showDialog)
        self.setFocus()
        self.widget = QtGui.QWidget(self)
        self.widget.setStyleSheet('QWidget {background-color: %s}' %color.name())
        self.widget.setGeometry(130, 22, 100, 100)
    def showDialog(self):
        col = QtGui.QColorDialog.getColor()
        if col.isValid():
            self.widget.setStyleSheet('QWidget {background-color: %s}' %col.name())
    
app = QtGui.QApplication(sys.argv)
qb = ColorDialog()
qb.show()
sys.exit(app.exec_())