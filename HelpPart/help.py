from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic, QtCore, QtGui
import os


Form = uic.loadUiType(os.path.join(os.getcwd(), 'HelpPart/Help.ui'))[0]


class helpWindow(QMainWindow, Form):
    def __init__(self, Mediaplayer):
        QMainWindow.__init__(self, parent=Mediaplayer)
        Form.__init__(self)
        self.setupUi(self)

        # To Specialize flags
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.setWindowTitle("Help")

        self.pushButton_Exit.clicked.connect(self.close)