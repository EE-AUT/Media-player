import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic, QtCore, QtGui

Form = uic.loadUiType(os.path.join(os.getcwd(), 'PlayListPart/Playlist.ui'))[0]


class PlaylistWindow(QMainWindow, Form, QtCore.QThread):
    def __init__(self, MediaPlayer):
        QMainWindow.__init__(self)
        Form.__init__(self)
        QtCore.QThread.__init__(self, parent=MediaPlayer)
        self.setupUi(self)
        self.MediaPlayer = MediaPlayer

        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowStaysOnTopHint
        )


        self.pushButton_Close.clicked.connect(lambda:self.close())


