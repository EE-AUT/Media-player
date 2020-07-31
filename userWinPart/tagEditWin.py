from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtCore, QtGui
import os
from editPart import timeconvert as tc
from editPart.edit import edit_Tags
import re
from editPart.edit import edit_Tags





Form = uic.loadUiType(os.path.join(os.getcwd(), 'userWinPart/editTagWin.ui'))[0]

class tagEditWin(QMainWindow, Form):
    def __init__(self, parent= None, Title= "Change tag", Text= "None", Time= "None"):
        Form.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Title = Title
        self.setWindowTitle(Title)
        self.MediaPlayer = parent
        self.Text = Text
        self.Time = Time
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        if Title == "Change tag":
            self.Ok_Button.setText("Change")
            self.tag_LineEdit.setText(Text)
            self.time_LineEdit.setText(Time)
            
        if Title == "Add tag":
            self.Ok_Button.setText("Create")
            self.tag_LineEdit.setPlaceholderText("Enter Tag here")
            self.time_LineEdit.setPlaceholderText("Time -> format : H:M:S or M:S")
        
        self.Ok_Button.clicked.connect(self.okClicked)
        self.No_Button.clicked.connect(self.noClicked)
        self.closeEvent = self.CloseWin

    # clicked yes
    def okClicked(self):
        try:
            session = self.MediaPlayer.Setting.comboBox_Tag.currentText().split(".")[0]
            text = self.tag_LineEdit.text() #line Edit text
            time = self.time_LineEdit.text() #lineEdit Time
            if not text == "" and not time == "": # if line edit not empty
                if re.search("\d\d:\d\d", time) or re.search("\d\d:\d\d:\d\d", time): #check format of line edit
                    if self.Title == "Change tag": # if change tag
                        del self.MediaPlayer.allTag[session][self.Text]
                        self.MediaPlayer.allTag[session].update({text : time})
                        self.MediaPlayer.set_TagonListwidget(session) # update tags
                        edit_Tags(
                            self.Text + "#" + self.Time, text + "#" + time, self.MediaPlayer.tag_Path)
                        self.close()

                    elif self.Title == "Add tag": # if add tag
                        self.MediaPlayer.allTag[session].update({text : time}) # add tag 
                        self.MediaPlayer.set_TagonListwidget(session) # update tags
                        edit_Tags( # add tag to csv file
                            session + "\n", session + "\n" + text + "#" + time + "\n", self.MediaPlayer.tag_Path)
                        self.close()
                else:
                    print("current format")
            else:
                print("fill all")
        except Exception as e:
            print(e)
        

    # clecked cancel
    def noClicked(self):
        self.close()
    
    def CloseWin(self, val):
        self.MediaPlayer.Setting.pushButton_Edit.setEnabled(True)
        self.MediaPlayer.Setting.pushButton_Add.setEnabled(True)

