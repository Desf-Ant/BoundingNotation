from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor

class CustomGraphicsRectItem(QGraphicsRectItem) :

    def __init__(self, x1,y1,x2,y2,pen):
        super().__init__()
        self.setRect(x1,y1,x2-x1,y2-y1)
        self.setPen(pen)
