from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtCore, QtGui
import os
from editPart import timeconvert as tc





Form = uic.loadUiType(os.path.join(os.getcwd(), 'userWinPart/confirm.ui'))[0]

class confrimWin(QMainWindow, Form):
    def __init__(self, parent= None, session = None, tag_Text = None, Text = "Are You sure", Title = "confirm"):
        Form.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(Title)
        self.MediaPlayer = parent
        self.session = session
        self.tag_Text = tag_Text

        self.yes_Button.clicked.connect(self.yes_Clicked)
        self.no_Button.clicked.connect(self.no_Clicked)
        self.Msg_Lebel.setText(Text)
    
    def yes_Clicked(self):
        self.MediaPlayer.change_Video(self.session)
        try:
            time_second = tc.to_second(self.MediaPlayer.allTag[self.session][self.tag_Text])
            self.MediaPlayer.change_Position(time_second)
        except Exception as e:
            print(e)
        self.close()
    
    
    def no_Clicked(self):
        self.close()
        