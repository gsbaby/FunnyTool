from PyQt4 import QtGui
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class GrildLayout(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self)
        
        self.setWindowTitle(u'计算器布局图')
        
        names = [u'清除',u'后退','',u'关闭','7','8','9','/','4','5','6','*','1','2','3','-','0','.','=','+']
        
        grid = QtGui.QGridLayout()
        
        j = 0
        
        pos = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3),(4,0),(4,1),(4,2),(4,3)]
        
        for i in names:
            button = QtGui.QPushButton(i)
            if j == 2:
                grid.addWidget(QtGui.QLabel(''),0,2)
            else:
                grid.addWidget(button,pos[j][0],pos[j][1])
            j += 1
                
        self.setLayout(grid)

app = QtGui.QApplication(sys.argv)
qb = GrildLayout()
qb.show()
sys.exit(app.exec_())        