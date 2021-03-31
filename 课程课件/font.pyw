#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from PyQt4 import QtGui, QtCore


class FontDialog(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self)
        hbox = QtGui.QHBoxLayout()
        self.setGeometry(300, 300, 250, 110)
        self.setWindowTitle(u'字体对话框')
        button = QtGui.QPushButton(u'选择字体', self)
        button.setFocusPolicy(QtCore.Qt.NoFocus)
        button.move(20, 20)
        hbox.addWidget(button)
        self.connect(button, QtCore.SIGNAL('clicked()'), self.showDialog)
        self.label = QtGui.QLabel(u'我要学点编程吧', self)
        self.label.move(130, 20)
        hbox.addWidget(self.label, 1)
        self.setLayout(hbox)
    def showDialog(self):
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.label.setFont(font)


app = QtGui.QApplication(sys.argv)
cd = FontDialog()
cd.show()
sys.exit(app.exec_())