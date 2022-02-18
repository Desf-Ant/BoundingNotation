from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor

class CustomGraphicsScene(QGraphicsScene) :

    def __init__(self, parent=None,core=None) :
        QGraphicsScene.__init__(self,parent)
        self.tempStartPoint = None
        self.tempStopPoint = None
        self.core = core
        self.rects = []

    def setCore(self, core) :
        self.core = core

    def mousePressEvent(self, event):
        print(event.scenePos().x(), event.scenePos().y())
        self.tempStartPoint = event.scenePos()

    def mouseReleaseEvent(self, event) :
        print(event.scenePos().x(), event.scenePos().y())
        self.tempStopPoint = event.scenePos()
        self.core.addRect(self.tempStartPoint, self.tempStopPoint)

    def drawRect(self,x1,y1,x2,y2) :
        self.addRect(x1,y1,x2-x1,y2-y1,QPen(QColor(55,255,55), 5))

    def clearRect(self) :
        self.rects.clear()
