import sys
import os
import LoginPart.Login as Login
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog 
from PyQt5 import uic , QtMultimedia
from PyQt5 import QtCore 




Form = uic.loadUiType(os.path.join(os.getcwd(), 'Mediaplayer.ui'))[0]

class MediaPlayer(QMainWindow,Form):
    def __init__(self):
        Form.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Media Player")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    Loginw = Login.LoginWindow()
    Loginw.show()
    app.exec_()
    if Loginw.Login():
        # app=QApplication(sys.argv)
        Mainw =MediaPlayer()
        url=QtCore.QUrl.fromLocalFile("./S01-981120.mp4")
        content=QtMultimedia.QMediaContent(url)
        
        Mainw.show()
        sys.exit(app.exec_())

    