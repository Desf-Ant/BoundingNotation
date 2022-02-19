from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor

class CustomGraphicsRectItem(QGraphicsRectItem) :

    def __init__(self, defaultPen, selectedPen, x1,y1,x2,y2):
        super().__init__()
        self.defaultPen = defaultPen
        self.selectedPen = selectedPen
        self.setRect(x1,y1,x2-x1,y2-y1)
        self.setPen(defaultPen)

    def deselect(self) :
        self.setPen(self.defaultPen)

    def select(self):
        self.setPen(self.selectedPen)
