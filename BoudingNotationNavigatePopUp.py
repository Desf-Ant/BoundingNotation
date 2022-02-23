from PyQt5.QtWidgets import QDialog ,QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIntValidator

class BoudingNotationNavigatePopUp(QDialog) :
    def __init__(self, parent=None) :
        super().__init__()
        self.parent = parent
        self.resize(260,120)
        self.setWindowTitle("Choose which index go to")
        self.initComponents()
        self.initLayout()
        self.initConnect()

    def initComponents(self) :
        self.lineInput = QLineEdit()
        self.okBtn = QPushButton("Ok")
        self.lineInput.setValidator(QIntValidator())

    def initLayout(self) :
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.addWidget(self.lineInput)
        self.vbox.addWidget(self.okBtn)

    def initConnect(self) :
        self.okBtn.clicked.connect(self.returnAndCloseApp)
        self.lineInput.returnPressed.connect(self.returnAndCloseApp)

    def returnAndCloseApp(self) :
        self.parent.getIndexToNavigate(int(self.lineInput.text()))
        self.close()
