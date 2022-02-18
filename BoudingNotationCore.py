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
        self.rowData = []
        self.data = {}
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
        if len(self.rowData) :
            self.currentImageIndex = self.allFiles.index(self.rowData[-1]["pathFile"])

    def update(self) :
        self.view.clearScene()
        self.view.loadImage(self.pathFolder + "/" +self.allFiles[self.currentImageIndex])
        self.view.setImgLabel(str(self.currentImageIndex+1) + "/" + str(len(self.allFiles)))
        for r in self.data[self.allFiles[self.currentImageIndex]] :
            self.view.drawRect(int(r["x1"]),int(r["y1"]),int(r["x2"]),int(r["y2"]))

    def getAllFiles(self) :
        print("get all files")
        self.allFiles = os.listdir(self.pathFolder)
        if not self.checkBoudingAnnot() :
            print("no bouding annotation found try to create the csv")
            self.createCSV()
        self.cleanAllFiles()
        self.openCSV()
        self.convertData()

    def cleanAllFiles(self) :
        for element in self.allFiles :
            if element[-4:] != ".jpg" and element[-4:] != ".png" :
                self.allFiles.remove(element)

    def convertData(self) :
        for im in self.allFiles :
            self.data[im] = []
        for d in self.rowData :
            self.data[d["pathFile"]].append({"x1":d["x1"],"y1":d["y1"],"x2":d["x2"],"y2":d["y2"],"label":d["label"]})

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
                self.rowData.append(dict(row))
        print("all rowData is in rowData variable")

    def addRect(self, p1,p2):
        x1, x2 = min(p1.x(),p2.x()), max(p1.x(),p2.x())
        y1, y2 = min(p1.y(),p2.y()), max(p1.y(),p2.y())
        self.data[self.allFiles[self.currentImageIndex]].append({"x1":x1,"y1":y1,"x2":x2,"y2":y2,"label":""})
        self.update()

    def tapOnPrevButton(self) :
        if self.currentImageIndex > 0 and len(self.allFiles) > 0:
            self.currentImageIndex -= 1
            self.update()

    def tapOnNextButton(self) :
        if self.currentImageIndex < len(self.allFiles)-1 and len(self.allFiles) > 0:
            self.currentImageIndex += 1
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
