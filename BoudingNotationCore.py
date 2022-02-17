from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from BoudingNotationView import *
import sys
import csv
import os

class BoudingNotationCore :

    def __init__(self) :
        self.view = None
        self.pathFolder = ""
        self.allFiles = []
        self.data = []
        self.csvLine = 0
        self.currentImageIndex = 0

    def setView(self, view):
        self.view = view

    def sendFolder(self, path) :
        self.pathFolder = path
        self.initialization()
        self.update()

    def initialization(self) :
        print("Init the begining of the process")
        self.getAllFiles()
        if len(self.data) :
            self.csvLine = len(self.data)-1
            self.currentImageIndex = self.allFiles.index(self.data[-1]["pathFile"])

    def update(self) :
        self.view.loadImage(self.pathFolder + "/" +self.allFiles[self.currentImageIndex])
        self.view.setImgLabel(str(self.currentImageIndex+1) + "/" + str(len(self.allFiles)))

    def getAllFiles(self) :
        print("get all files")
        self.allFiles = os.listdir(self.pathFolder)
        if not self.checkBoudingAnnot() :
            print("no bouding annotation found try to create the csv")
            self.createCSV()
        self.cleanAllFiles()
        self.openCSV()

    def cleanAllFiles(self) :
        for element in self.allFiles :
            if element[-4:] != ".jpg" and element[-4:] != ".png" :
                self.allFiles.remove(element)

    def checkBoudingAnnot(self) :
        return "boudingAnnotations.csv" in self.allFiles

    def createCSV (self) :
        with open(self.pathFolder+"\\boudingAnnotations.csv", "w",newline='') as file :
            writer = csv.writer(file)
            writer.writerow(["pathFile","x1","y1","x2","y2","label"])

    def openCSV (self) :
        print("try to open the file")
        with open(self.pathFolder+"\\boudingAnnotations.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader :
                self.data.append(dict(row))
        print("all data is in data variable")

    def tapOnPrevButton(self) :
        if self.currentImageIndex > 0 and len(self.allFiles) > 0:
            self.currentImageIndex -= 1
            for el in self.data :
                if el["pathFile"] == self.allFiles[self.currentImageIndex] :
                    self.csvLine = self.data.index(el)
                    break
            self.update()

    def tapOnNextButton(self) :
        if self.currentImageIndex < len(self.allFiles)-1 and len(self.allFiles) > 0:
            self.currentImageIndex += 1
            for el in self.data :
                if el["pathFile"] == self.allFiles[self.currentImageIndex] :
                    self.csvLine = self.data.index(el)
                    break
            self.update()


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
