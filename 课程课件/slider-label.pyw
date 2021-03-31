#-*- coding=utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from PyQt4 import QtGui,QtCore

class SliderLabel(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self)
        self.setGeometry(200,200,1500,600)
        self.setWindowTitle(u'滑动块')
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        self.slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider.setGeometry(30,40,100,60)
        self.connect(self.slider,QtCore.SIGNAL('valueChanged(int)'),self.changeValue)
        self.label = QtGui.QLabel(self)
        self.label.setPixmap(QtGui.QPixmap('01.png'))
        self.label.setGeometry(160,40,1400,600)
    
    def changeValue(self, value):
        pos = self.slider.value()
        
        if pos == 0:
            self.label.setPixmap(QtGui.QPixmap('01.png'))
        elif 0 < pos <= 30:
            self.label.setPixmap(QtGui.QPixmap('02.png'))
        elif 30 < pos < 80:
            self.label.setPixmap(QtGui.QPixmap('03.png'))
        else:
            self.label.setPixmap(QtGui.QPixmap('04.png'))

app = QtGui.QApplication(sys.argv)
w = SliderLabel()
w.show()
sys.exit(app.exec_())