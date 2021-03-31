#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from PyQt4 import QtGui, QtCore

class ProgressBar(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle(u'进度条')
        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.button = QtGui.QPushButton(u'开始', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(40, 80)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.onStart)
        self.timer = QtCore.QBasicTimer()
        self.step = 0
    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            return
        self.step = self.step +1
        self.pbar.setValue(self.step)
    def onStart(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText(u'开始')
        else:
            self.timer.start(100, self)
            self.button.setText(u'停止')


app = QtGui.QApplication(sys.argv)
icon = ProgressBar()
icon.show()
sys.exit(app.exec_())
