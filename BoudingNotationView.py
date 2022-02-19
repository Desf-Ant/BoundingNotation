from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from BoudingNotationCore import *
from CustomGraphicsScene import *
import sys


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.core = None

    def setCore(self, core) :
        self.core = core
        self.scene.setCore(self.core)

    def setupUi(self, app) :
        screen = app.primaryScreen()
        rect = screen.availableGeometry()
        self.setObjectName("MainWindow")
        self.wwin, self.hwin = rect.width(), rect.height()
        self.resize(self.wwin, self.hwin)
        self.setWindowTitle("Bouding Notation")
        self.initMenu()
        self.initComponents()
        self.initLayout()
        self.initConnect()

    def initMenu(self) :
        self.menubar = QtWidgets.QMenuBar()
        self.setMenuBar(self.menubar)
        self.menuFichier = QtWidgets.QMenu()
        self.menuFichier.setTitle("File")
        self.menubar.addMenu(self.menuFichier)
        self.openAction = QtWidgets.QAction("Open Folder")
        self.menuFichier.addAction(self.openAction)

    def initComponents(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.rectLabel = QtWidgets.QLabel("Rectangle")
        self.scrollView = QtWidgets.QScrollArea()
        self.scrollViewContent = QtWidgets.QWidget()
        self.scrollView.setWidget(self.scrollViewContent)
        self.scrollView.setWidgetResizable(True)
        self.scrollView.setFixedWidth(self.wwin/6)
        self.leftBtn = QtWidgets.QPushButton("<")
        self.currentImgLabel = QtWidgets.QLabel("XXXX/NNNN")
        self.rightBtn = QtWidgets.QPushButton(">")
        self.view = QtWidgets.QGraphicsView()
        self.scene = CustomGraphicsScene()
        self.view.setScene(self.scene)

    def initLayout(self) :
        self.hbox = QtWidgets.QHBoxLayout(self.centralwidget)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox2 = QtWidgets.QHBoxLayout()
        self.vboxScroll = QtWidgets.QVBoxLayout()
        self.hbox2.setAlignment(QtCore.Qt.AlignBottom)
        self.scrollViewContent.setLayout(self.vboxScroll)

        self.hbox.addLayout(self.vbox)
        self.vbox.addWidget(self.rectLabel)
        self.rectLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.vbox.addWidget(self.scrollView)
        self.vbox.addLayout(self.hbox2)
        self.hbox.addWidget(self.view)

        self.hbox2.addWidget(self.leftBtn)
        self.hbox2.addWidget(self.currentImgLabel)
        self.currentImgLabel.setAlignment(QtCore.Qt.AlignCenter)
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
        self.scene.clearRect()
        self.clearScroll()

    def clearScroll (self) :
        for i in reversed(range(self.vboxScroll.count())):
            self.vboxScroll.itemAt(i).removeWidget(self.core.getEditLine(i))
            self.vboxScroll.itemAt(i).removeWidget(self.core.getSuppBtnLine(i))
            self.vboxScroll.removeItem(self.vboxScroll.itemAt(i))


    def drawRect(self,x1,y1,x2,y2) :
        self.scene.drawRect(x1,y1,x2,y2)

    def populateScrollContent(self) :
        layout = QtWidgets.QHBoxLayout()
        line = QtWidgets.QLineEdit()
        suppBtn = QtWidgets.QPushButton("X")
        line.returnPressed.connect(self.didTapOnEditLine)
        suppBtn.clicked.connect(self.didTapOnSuppBtn)
        self.vboxScroll.addLayout(layout)
        layout.addWidget(line)
        layout.addWidget(suppBtn)
        self.core.addLine(line, suppBtn)

    def didTapOnEditLine(self) :
        print("press Enter")

    def didTapOnSuppBtn(self) :
        print("press supp")

    # def sayNumber(self) :
    #     for i, l in enumerate( self.lines) :
    #         if l.hasFocus() :
    #             print("focus on ",i)


if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    core = BoudingNotationCore()
    ui.setupUi(app)
    ui.setCore(core)
    core.setView(ui)
    ui.showMaximized()
    sys.exit(app.exec_())
