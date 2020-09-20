from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QSizePolicy
from PyQt5 import uic, QtCore, QtGui
import os
from editPart import timeconvert as tc
from editPart.edit import edit_Tags


# window for get accept from user to do some works


Form = uic.loadUiType(os.path.join(os.getcwd(), 'userWinPart/confirm.ui'))[0]


class confrimWin(QMainWindow, Form):
    def __init__(self, parent=None, session=None, tag_Text=None, Text="Are You sure", Title="Change video", tagPartText=None):
        Form.__init__(self)
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.Title = Title
        self.setWindowTitle(Title)
        if Title == "Warning":
            self.no_Button.setVisible(False)
            self.yes_Button.setText("Ok")
        self.MediaPlayer = parent
        self.session = session
        self.tag_Text = tag_Text
        self.tagPartText = tagPartText
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowStaysOnTopHint
        )

        self.yes_Button.clicked.connect(self.yes_Clicked)
        self.no_Button.clicked.connect(self.no_Clicked)

        if len(Text) > 60:
            Font_Size = int((60 / len(Text)) * 12)
        else:
            Font_Size = 10
        self.Msg_Lebel.setFont(QtGui.QFont('Arial', Font_Size)) 
        self.Msg_Lebel.setText(Text)

    # accept and do some works
    def yes_Clicked(self):
        if self.Title == "Change video":
            self.MediaPlayer.change_Video(self.session)
            try:
                time_second = tc.to_second(
                    self.MediaPlayer.allTag[self.session][self.tag_Text])
                self.MediaPlayer.change_Position(time_second)
            except:
                pass
        if self.Title == "Delete tag":
            try:
                del self.MediaPlayer.allTag[self.session][self.tagPartText[0]]
                self.MediaPlayer.set_TagonListwidget(self.session)
                # delete bookmark
                edit_Tags(
                    self.tagPartText[0] + "#" + self.tagPartText[1] + "#" + "\*", "", self.MediaPlayer.tag_Path)
                # delete tag
                edit_Tags(
                    self.tagPartText[0] + "#" + self.tagPartText[1], "", self.MediaPlayer.tag_Path)
                self.MediaPlayer.Setting.comboBox_Tag.setEnabled(True)
            except:
                self.MediaPlayer.Setting.comboBox_Tag.setEnabled(True)

        # close curent tag
        if self.Title == "Close Tag":
            self.closeTag()

        # create new tag
        if self.Title == "Create Tag":
            self.close()
            self.closeTag()
            dialog = QFileDialog(self, 'File tag', directory=os.getcwd())
            _path = dialog.getSaveFileName(filter= "*.csv")[0]
            try:
                if _path:
                    self.tag_Path = _path
                    open(self.tag_Path, "w")
            except:
                pass
            self.MediaPlayer.actionCreate_Tag.setEnabled(True)
        try:
            self.MediaPlayer.actionClose_Tag.setEnabled(True)
        except:
            pass
        try:
            self.close()
        except: 
            pass

    # no clicked

    def no_Clicked(self):
        self.MediaPlayer.actionCreate_Tag.setEnabled(True)
        self.close()

    # close current tag in Media

    def closeTag(self):
        self.MediaPlayer.allTag = {}
        self.MediaPlayer.tag_Path = None
        self.MediaPlayer.ListWidget_Tags_of_file.clear()
        self.MediaPlayer.sch_listWidget.clear()
        self.MediaPlayer.Setting.Edit_tag_Listwidget.clear()
