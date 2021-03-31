#coding=utf-8

from PyQt4 import QtGui
import sys
reload(sys)
sys.setdefaultencoding='utf8'

class GridLayout(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self)
        
        self.setWindowTitle(u'迷你写字板')
        
        title = QtGui.QLabel(u'标题')
        
        author = QtGui.QLabel(u'作者')
        
        review = QtGui.QLabel(u'预览')
        
        titleEdit = QtGui.QLineEdit()
        
        authorEdit = QtGui.QLineEdit()
        
        reviewEdit = QtGui.QLineEdit()
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(title,1,0)
        grid.addWidget(titleEdit,1,1)
        
        grid.addWidget(author,2,0)
        grid.addWidget(authorEdit,2,1)
        
        grid.addWidget(review,3,0)
        grid.addWidget(reviewEdit,3,1,5,1)
        
        self.setLayout(grid)
        self.resize(350,300)
        
app = QtGui.QApplication(sys.argv)
qb = GridLayout()
qb.show()
sys.exit(app.exec_())