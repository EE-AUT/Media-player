from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtCore, QtGui
import os
from editPart import timeconvert as tc
from editPart.edit import edit_Tags





Form = uic.loadUiType(os.path.join(os.getcwd(), 'userWinPart/confirm.ui'))[0]

class confrimWin(QMainWindow, Form):
    def __init__(self, parent= None, session = None, tag_Text = None, Text = "Are You sure", Title = "change video", tagPartText= None):
        Form.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Title = Title
        self.setWindowTitle(Title)
        self.MediaPlayer = parent
        self.session = session
        self.tag_Text = tag_Text
        self.tagPartText = tagPartText

        self.yes_Button.clicked.connect(self.yes_Clicked)
        self.no_Button.clicked.connect(self.no_Clicked)
        self.Msg_Lebel.setText(Text)
    
    def yes_Clicked(self):
        if self.Title == "change video":
            self.MediaPlayer.change_Video(self.session)
            try:
                time_second = tc.to_second(self.MediaPlayer.allTag[self.session][self.tag_Text])
                self.MediaPlayer.change_Position(time_second)
            except Exception as e:
                print(e)
        if self.Title == "delete tag":
            try:
                del self.MediaPlayer.allTag[self.session][self.tagPartText[0]]
                self.MediaPlayer.set_TagonListwidget(self.session)
                # delete bookmark
                edit_Tags(
                    self.tagPartText[0] + "#" + self.tagPartText[1] + "#" + "\*", "", self.MediaPlayer.tag_Path)
                # delete tag
                edit_Tags(
                    self.tagPartText[0] + "#" + self.tagPartText[1], "", self.MediaPlayer.tag_Path)
            except Exception as e:
                print(e)
        
        self.close()
    
    
    def no_Clicked(self):
        self.close()
        