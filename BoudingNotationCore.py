from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from BoudingNotationView import *
import sys

class BoudingNotationCore :

    def __init__(self) :
        self.view = None
        self.pathFolder = ""

    def setView(self, view):
        self.view = view

    def sendFolder(self, path) :
        self.pathFolder = path



if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    core = BoudingNotationCore()
    ui.setupUi(app,MainWindow)
    ui.setCore(core)
    core.setView(ui)
    MainWindow.showMaximized()
    sys.exit(app.exec_())
