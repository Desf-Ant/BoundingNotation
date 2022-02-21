from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QColor

class CustomGraphicsRectItem(QGraphicsRectItem) :

    def __init__(self, defaultPen, selectedPen, x1,y1,x2,y2):
        super().__init__()
        self.defaultPen = defaultPen
        self.selectedPen = selectedPen
        self.handlers = []
        self.setRect(x1,y1,x2-x1,y2-y1)
        self.x = x1
        self.y = y1
        self.w = x2-x1
        self.h = y2-y1
        self.setPen(defaultPen)
        self.createHandlers()

    def createHandlers(self) :
        h1 = QRectF(self.x-6+self.w/2, self.y-6, 12,12)
        h2 = QRectF(self.x+self.w-6, self.y+self.h/2-6, 12,12)
        h3 = QRectF(self.x-6+self.w/2, self.y+self.h-6, 12,12)
        h4 = QRectF(self.x-6,self.y+self.h/2-6, 12,12)
        self.handlers = [h1,h2,h3,h4]

    def refreshHandlers(self) :
        self.createHandlers()

    def deselect(self) :
        self.setPen(self.defaultPen)

    def select(self):
        self.setPen(self.selectedPen)

    def changePos(self, x,y) :
        self.changeRect(x,y,self.w+x,self.h+y)

    def changeRect(self, x1,y1,x2,y2) :
        self.x = x1
        self.y = y1
        self.w = x2-x1
        self.h = y2-y1
        self.setRect(self.x,self.y,self.w,self.h)

    def getHandler(self) :
        return self.handlers

    def changeX1(self,x):
        if x < self.x+self.w - 10 :
            self.w = (self.w+self.x)-x
            self.x = x
            self.setRect(self.x,self.y,self.w,self.h)

    def changeX2(self, x2) :
        if x2 > self.x + 10 :
            self.w = x2 - self.x
            self.setRect(self.x,self.y,self.w,self.h)

    def changeY1(self,y):
        if y < self.y + self.h - 10 :
            self.h = (self.h+self.y)-y
            self.y = y
            self.setRect(self.x,self.y,self.w,self.h)

    def changeY2(self, y2) :
        if y2 > self.y + 10 :
            self.h = y2 - self.y
            self.setRect(self.x,self.y,self.w,self.h)
