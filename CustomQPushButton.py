from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt

class CustomQPushButton(QPushButton):

    def __init__(self, index,*args) :
        super().__init__(*args)
        self.index = index

    def getIndex(self) :
        return self.index
