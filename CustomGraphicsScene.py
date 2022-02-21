from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush, QColor
from CustomGraphicsRectItem import *

class CustomGraphicsScene(QGraphicsScene) :

    def __init__(self, parent=None,core=None) :
        QGraphicsScene.__init__(self,parent)
        self.tempStartPoint = None
        self.tempStopPoint = None
        self.defaultPen = QPen(QColor(55,255,55),5)
        self.selectedPen = QPen(QColor(255,0,0),5)
        self.currentRect = None
        self.currentHandler = None
        self.core = core
        self.rects = []
        self.handlers = []

    def setCore(self, core) :
        self.core = core

    def mousePressEvent(self, event):
        print("start",event.scenePos().x(), event.scenePos().y())
        self.tempStartPoint = event.scenePos()
        if self.core.getMode() == 2 :
            self.selectFromEvent(event)
        if self.core.getMode() == 3 and len(self.handlers) > 0:
            self.selectHandler(event)

    def mouseReleaseEvent(self, event) :
        print("stop",event.scenePos().x(), event.scenePos().y())
        self.tempStopPoint = event.scenePos()
        if abs(self.tempStartPoint.x() - self.tempStopPoint.x()) < 10 and  abs(self.tempStartPoint.y() - self.tempStopPoint.y()) < 10 :
            # On ne créer pas de rect et on compte ca comme un clic
            self.selectFromEvent(event)
            return
        if self.core.getMode() == 1 :
            self.core.addRect(self.tempStartPoint, self.tempStopPoint)
        elif self.core.getMode() == 2 :
            self.core.updateData(self.rects.index(self.currentRect),self.currentRect.rect())
        elif self.core.getMode() == 3 :
            self.core.updateData(self.rects.index(self.currentRect),self.currentRect.rect())

    def mouseDoubleClickEvent(self,event):
        self.selectFromEvent(event)

    def mouseMoveEvent(self,event) :
        if len(self.rects) < 0 : return
        if self.core.getMode() == 2:
            newPos = event.scenePos()
            self.currentRect.changePos(newPos.x()-self.delta.x(),newPos.y()-self.delta.y())
        if self.core.getMode() == 3 and self.currentHandler is not None :
            self.moveHandler(event)

    def selectFromEvent(self, event) :
        index = None
        for i, r in enumerate(self.rects) :
            if r.rect().contains(event.scenePos()) :
                index = i
                break
        self.selecteRect(index)

    def deselectAll(self) :
        # Remet en normal tous les rect
        self.currentRect = None
        self.currentHandler = None
        for r in self.rects :
            r.deselect()
        self.core.update()

    def selecteRect(self, index) :
        self.deselectAll()
        # Met en rouge le rect specific
        if index is not None :
            self.currentRect = self.rects[index]
            self.delta = self.tempStartPoint - self.currentRect.rect().topLeft()
            self.currentRect.select()
            if self.core.getMode() == 3 :
                self.drawHandler(self.currentRect.getHandler())

    def selectHandler(self,event) :
        for i, h in enumerate(self.handlers):
            if h.rect().contains(event.scenePos()):
                self.currentHandler = h

    def moveHandler(self,event) :
        if self.handlers.index(self.currentHandler) == 0 :
            self.currentRect.changeY1(event.scenePos().y())
        if self.handlers.index(self.currentHandler) == 1 :
            self.currentRect.changeX2(event.scenePos().x())
        if self.handlers.index(self.currentHandler) == 2 :
            self.currentRect.changeY2(event.scenePos().y())
        if self.handlers.index(self.currentHandler) == 3 :
            self.currentRect.changeX1(event.scenePos().x())
        self.currentRect.refreshHandlers()
        self.refreshHandlers(self.currentRect.getHandler())

    def drawRect(self,x1,y1,x2,y2) :
        rect = CustomGraphicsRectItem(self.defaultPen, self.selectedPen, x1,y1,x2,y2)
        self.rects.append(rect)
        self.addItem(rect)

    def drawHandler(self, rects) :
        self.handlers.clear()
        for h in rects :
            self.handlers.append(self.addRect(h, QPen(Qt.magenta), QBrush(Qt.magenta)))

    def refreshHandlers(self, rects):
        for i, h in enumerate(rects) :
            self.handlers[i].setRect(rects[i])

    def clearRect(self) :
        self.rects.clear()
