from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor
from CustomGraphicsRectItem import *

class CustomGraphicsScene(QGraphicsScene) :

    def __init__(self, parent=None,core=None) :
        QGraphicsScene.__init__(self,parent)
        self.tempStartPoint = None
        self.tempStopPoint = None
        self.defaultPen = QPen(QColor(55,255,55),5)
        self.selectedPen = QPen(QColor(255,0,0),5)
        self.core = core
        self.rects = []

    def setCore(self, core) :
        self.core = core

    def mousePressEvent(self, event):
        print("start",event.scenePos().x(), event.scenePos().y())
        self.tempStartPoint = event.scenePos()

    def mouseReleaseEvent(self, event) :
        print("stop",event.scenePos().x(), event.scenePos().y())
        self.tempStopPoint = event.scenePos()
        if abs(self.tempStartPoint.x() - self.tempStopPoint.x()) < 10 and  abs(self.tempStartPoint.y() - self.tempStopPoint.y()) < 10 :
            # On ne créer pas de rect et on compte ca comme un clic
            self.selectFromEvent(event)
            return
        self.core.addRect(self.tempStartPoint, self.tempStopPoint)

    def mouseDoubleClickEvent(self,event):
        self.selectFromEvent(event)

    def selectFromEvent(self, event) :
        index = None
        for i, r in enumerate(self.rects) :
            if r.rect().contains(event.scenePos()) :
                index = i
                break
        self.selecteRect(index)

    def deselectAll(self) :
        # Remet en normal tous les rect
        for r in self.rects :
            r.deselect()

    def selecteRect(self, index) :
        self.deselectAll()
        # Met en rouge le rect specific
        if index is not None : self.rects[index].select()

    def drawRect(self,x1,y1,x2,y2) :
        rect = CustomGraphicsRectItem(self.defaultPen, self.selectedPen, x1,y1,x2,y2)
        self.rects.append(rect)
        self.addItem(rect)

    def clearRect(self) :
        self.rects.clear()
