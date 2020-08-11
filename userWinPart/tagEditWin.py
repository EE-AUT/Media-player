from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtCore, QtGui
import os
from editPart import timeconvert as tc
from editPart.edit import edit_Tags
import re
from editPart.edit import edit_Tags
from bookmarkPart.bookmark import add_Bookmark
from userWinPart.confirm import confrimWin


# window for edit end add tag


Form = uic.loadUiType(os.path.join(
    os.getcwd(), 'userWinPart/editTagWin.ui'))[0]


class tagEditWin(QMainWindow, Form):
    def __init__(self, parent=None, Title="Change tag", Text="None", Time="None"):
        Form.__init__(self)
        QMainWindow.__init__(self, parent=parent)
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
            self.time_LineEdit.setPlaceholderText(
                "Time -> format : H:M:S or M:S")

        self.Ok_Button.clicked.connect(self.okClicked)
        self.No_Button.clicked.connect(self.noClicked)
        self.closeEvent = self.CloseWin

    # clicked yes
    def okClicked(self):
        try:
            session = self.MediaPlayer.Setting.comboBox_Tag.currentText().split(".")[
                0]
            text = self.tag_LineEdit.text()  # line Edit text
            time = self.time_LineEdit.text()  # lineEdit Time
            if not text == "" and not time == "":  # if line edit not empty
                # check format of line edit
                if re.search("\d\d:\d\d", time) or re.search("\d\d:\d\d:\d\d", time):
                    if self.Title == "Change tag":  # if change tag
                        del self.MediaPlayer.allTag[session][self.Text]
                        self.MediaPlayer.allTag[session].update({text: time})
                        self.MediaPlayer.set_TagonListwidget(
                            session)  # update tags in Edit part
                        if self.check_Timeformat(time): # check time format
                            edit_Tags(
                                self.Text + "#" + self.Time, text + "#" + time, self.MediaPlayer.tag_Path)
                            self.close()
                        else: #show error message to user if enter incorrect format for time
                            self.error_TimeFormat()
                        

                    elif self.Title == "Add tag":  # if add tag
                        if self.check_Timeformat(time):
                            if session in self.MediaPlayer.allTag:
                                self.MediaPlayer.allTag[session].update(
                                    {text: time})  # add tag
                                edit_Tags(  # add tag to csv file
                                    session + "\n", session + "\n" + text + "#" + time + "\n", self.MediaPlayer.tag_Path)
                            else:
                                # if there is no tag for session in database
                                self.MediaPlayer.allTag.update(
                                    {session: {text: time}})
                                add_Bookmark(text + "#" + time, session,
                                            self.MediaPlayer.tag_Path)

                            # check for syncronise media tags and setting tags
                            if session == ".".join(self.MediaPlayer.ComboBox_Tags_of_file.currentText().split(".")[:-1]):
                                self.MediaPlayer.set_TagonListwidget(
                                    session)  # update tags in add part
                            else:
                                self.MediaPlayer.set_TagonListwidget(
                                    session, Media_Tags=False)  # update tags in add part
                            self.close()
                        else: #show error message to user if enter incorrect format for time
                            self.error_TimeFormat()
                else: #show error message to user if enter incorrect format for time
                    self.error_TimeFormat()
        except:
            pass


    # error message for user if time format is incorrect
    def error_TimeFormat(self):
        _Warning = confrimWin(self, Title= "Warning", Text= "Please enter current format for time")
        _Warning.show()


    def check_Timeformat(self, Time):
        items = Time.split(":") # get hour and minute and seconds
        try:
            if len(items) == 2: # if hour:minute format
                if int(items[0]) < 24 and int(items[1]) < 60: # check correction
                    for item in items:
                        if len(item) != 2:
                            return False
                    return True
            
            elif len(items) == 3: # if hour:minute:second format
                if int(items[0]) < 24 and int(items[1]) < 60 and int(items[2]) < 60 : #check correction
                    for item in items:
                        if len(item) != 2:
                            return False
                    return True
            else:
                return False 
        except:
            return False
        return False

    # clecked cancel
    def noClicked(self):
        self.close()

    def CloseWin(self, val):
        self.MediaPlayer.Setting.comboBox_Tag.setEnabled(True)
        self.MediaPlayer.Setting.pushButton_Edit.setEnabled(True)
        self.MediaPlayer.Setting.pushButton_Add.setEnabled(True)
