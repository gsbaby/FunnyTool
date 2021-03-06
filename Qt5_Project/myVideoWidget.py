#!/usr/bin/python3
# coding = utf-8
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import *
class myVideoWidget(QVideoWidget):
    doubleClickedItem = pyqtSignal(str)  # 创建双击信号
    def __init__(self,parent=None):
        super(QVideoWidget,self).__init__(parent)
    def mouseDoubleClickEvent(self,QMouseEvent):     #双击事件
        self.doubleClickedItem.emit("双击")