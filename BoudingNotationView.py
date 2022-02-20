from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from BoudingNotationCore import *
from CustomGraphicsScene import *
from CustomQPushButton import *
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
        self.defaultLabel = QtWidgets.QLabel("Default Label :")
        self.defaultLabelEdit = QtWidgets.QLineEdit()
        self.defaultLabelEdit.setFixedWidth(self.wwin/6)
        self.groupMode = QtWidgets.QButtonGroup()
        self.drawModeBtn = QtWidgets.QRadioButton("Draw")
        self.moveModeBtn = QtWidgets.QRadioButton("Move")
        self.editModeBtn = QtWidgets.QRadioButton("Edit")
        self.groupMode.addButton(self.drawModeBtn)
        self.groupMode.addButton(self.moveModeBtn)
        self.groupMode.addButton(self.editModeBtn)
        self.groupMode.setId(self.drawModeBtn,1)
        self.groupMode.setId(self.moveModeBtn,2)
        self.groupMode.setId(self.editModeBtn,3)
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
        self.vbox.addWidget(self.defaultLabel)
        self.vbox.addWidget(self.defaultLabelEdit)
        self.vbox.addWidget(self.drawModeBtn)
        self.vbox.addWidget(self.moveModeBtn)
        self.vbox.addWidget(self.editModeBtn)
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
        self.defaultLabelEdit.textChanged.connect(self.didEditDefaultLabel)
        self.groupMode.buttonClicked.connect(self.changeMode)

    def changeMode(self, btn):
        self.core.setMode(self.groupMode.id(btn))

    def openFolder(self) :
        fname = QtWidgets.QFileDialog.getExistingDirectory()
        if fname :
            self.core.sendFolder(fname)

    def setImgLabel(self, label) :
        self.currentImgLabel.setText(label)

    def setRadioBtnCheck(self, index) :
        if index ==  1 : self.drawModeBtn.setChecked(True)
        elif index == 2: self.moveModeBtn.setChecked(True)
        else : self.editModeBtn.setChecked(True)

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

    def populateScrollContent(self,index,label) :
        layout = QtWidgets.QHBoxLayout()
        line = QtWidgets.QLineEdit()
        line.setText(label)
        suppBtn = CustomQPushButton(index,"X")
        line.returnPressed.connect(self.didPressEnterEditLine)
        line.textChanged.connect(self.didTapTextEditLine)
        line.cursorPositionChanged.connect(self.wantFocus)
        suppBtn.clicked.connect(self.didTapOnSuppBtn)
        self.vboxScroll.addLayout(layout)
        layout.addWidget(line)
        layout.addWidget(suppBtn)
        self.core.addLine(line, suppBtn)

    def didEditDefaultLabel(self) :
        self.core.setDefaultLabel(self.sender().text())

    def wantFocus(self) :
        self.core.tapTextEditLine(self.sender().text())

    def didPressEnterEditLine(self) :
        self.sender().clearFocus()
        self.scene.deselectAll()

    def didTapTextEditLine(self) :
        self.core.tapTextEditLine(self.sender().text())

    def didTapOnSuppBtn(self) :
        self.core.tapOnSuppBtn(self.sender().getIndex())

    def selectRectFromIndex(self,index) :
        self.scene.selecteRect(index)

    def keyPressEvent(self, event):
        if event.key()== Qt.Key_D :
            self.setRadioBtnCheck(1)
            self.changeMode(self.drawModeBtn)
        if event.key()== Qt.Key_M :
            self.setRadioBtnCheck(2)
            self.changeMode(self.moveModeBtn)
        if event.key()== Qt.Key_E :
            self.setRadioBtnCheck(3)
            self.changeMode(self.editModeBtn)


if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    core = BoudingNotationCore()
    ui.setupUi(app)
    ui.setCore(core)
    core.setView(ui)
    ui.showMaximized()
    sys.exit(app.exec_())
