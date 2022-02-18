from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from BoudingNotationCore import *
from CustomGraphicsScene import *
import sys


class Ui_MainWindow(object):
    def __init__(self):
        self.core = None

    def setCore(self, core) :
        self.core = core
        self.scene.setCore(self.core)

    def setupUi(self, app, MainWindow) :
        screen = app.primaryScreen()
        rect = screen.availableGeometry()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(rect.width(), rect.height())
        MainWindow.setWindowTitle("Bouding Notation")
        self.initMenu(MainWindow)
        self.initComponents(MainWindow)
        self.initLayout(MainWindow)
        self.initConnect()

    def initMenu(self, MainWindow) :
        self.menubar = QtWidgets.QMenuBar()
        MainWindow.setMenuBar(self.menubar)
        self.menuFichier = QtWidgets.QMenu()
        self.menuFichier.setTitle("File")
        self.menubar.addMenu(self.menuFichier)
        self.openAction = QtWidgets.QAction("Open Folder")
        self.menuFichier.addAction(self.openAction)

    def initComponents(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.rectLabel = QtWidgets.QLabel("Rectangle")
        self.scrollView = QtWidgets.QScrollArea()
        self.scrollViewContent = QtWidgets.QWidget()
        self.leftBtn = QtWidgets.QPushButton("<")
        self.currentImgLabel = QtWidgets.QLabel("XXXX/NNNN")
        self.rightBtn = QtWidgets.QPushButton(">")
        self.view = QtWidgets.QGraphicsView()
        self.scene = CustomGraphicsScene()
        self.view.setScene(self.scene)

    def initLayout(self, MainWindow) :
        self.hbox = QtWidgets.QHBoxLayout(self.centralwidget)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox2 = QtWidgets.QHBoxLayout()
        self.hbox2.setAlignment(QtCore.Qt.AlignBottom)

        self.hbox.addLayout(self.vbox)
        self.vbox.addWidget(self.rectLabel)
        self.rectLabel.setAlignment(QtCore.Qt.AlignHCenter)
        #self.vbox.addWidget(self.scrollViewContent)
        self.vbox.addLayout(self.hbox2)
        self.hbox.addWidget(self.view)

        self.hbox2.addWidget(self.leftBtn)
        self.hbox2.addWidget(self.currentImgLabel)
        self.hbox2.addWidget(self.rightBtn)

    def initConnect(self) :
        self.openAction.triggered.connect(self.openFolder)
        self.leftBtn.clicked.connect(self.didTapOnLeftBtn)
        self.rightBtn.clicked.connect(self.didTapOnRightBtn)

    def openFolder(self) :
        fname = QtWidgets.QFileDialog.getExistingDirectory()
        if fname :
            self.core.sendFolder(fname)

    def setImgLabel(self, label) :
        self.currentImgLabel.setText(label)

    def loadImage(self, pathImage) :
        print(pathImage)
        self.currentImage = self.scene.addPixmap(QtGui.QPixmap(pathImage))

    def didTapOnLeftBtn(self):
        print("previous image")
        self.core.tapOnPrevButton()

    def didTapOnRightBtn(self) :
        print("next image")
        self.core.tapOnNextButton()

    def clearScene(self) :
        self.scene.clear()

    def drawRect(self,x1,y1,x2,y2) :
        self.scene.drawRect(x1,y1,x2,y2)


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
