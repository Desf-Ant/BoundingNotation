from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor

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
            self.selecteRect(event)
            return
        self.core.addRect(self.tempStartPoint, self.tempStopPoint)

    def mouseDoubleClickEvent(self,event):
        self.selecteRect(event)

    def selecteRect(self, event) :
        i = -1
        # Met en rouge le rect selected
        for j, r in enumerate(self.rects) :
            if r.rect().contains(event.scenePos()) :
                r.setPen(self.selectedPen)
                i = j
                break
        # Remet tous les autres en couleur normale
        for j in range(len(self.rects)) :
            if j != i :
                self.rects[j].setPen(self.defaultPen)

    def drawRect(self,x1,y1,x2,y2) :
        self.rects.append(self.addRect(x1,y1,x2-x1,y2-y1,self.defaultPen))

    def clearRect(self) :
        self.rects.clear()
