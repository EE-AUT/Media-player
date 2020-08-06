from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from PyQt5 import uic, QtCore, QtGui
import os
from editPart import timeconvert as tc
from editPart.edit import edit_Tags


# window for get accept from user to do some works


Form = uic.loadUiType(os.path.join(os.getcwd(), 'userWinPart/confirm.ui'))[0]


class confrimWin(QMainWindow, Form):
    def __init__(self, parent=None, session=None, tag_Text=None, Text="Are You sure", Title="change video", tagPartText=None):
        Form.__init__(self)
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.Title = Title
        self.setWindowTitle(Title)
        if Title == "message for close tag":
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
        self.Msg_Lebel.setText(Text)

    # accept and do some works
    def yes_Clicked(self):
        if self.Title == "change video":
            self.MediaPlayer.change_Video(self.session)
            try:
                time_second = tc.to_second(
                    self.MediaPlayer.allTag[self.session][self.tag_Text])
                self.MediaPlayer.change_Position(time_second)
            except:
                pass
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
            except:
                pass

        # close curent tag
        if self.Title == "Close Tag":
            self.closeTag()

        # create new tag
        if self.Title == "Create Tag":
            self.closeTag()
            dialog = QFileDialog(self, 'file tag', directory=os.getcwd())
            dialog.setFileMode(QFileDialog.DirectoryOnly)
            if dialog.exec_() == QDialog.Accepted:
                _path = dialog.selectedFiles()[0]
                self.tag_Path = _path + "/Created_tag.csv"
                open(self.tag_Path, "w")
                self.MediaPlayer.actionCreate_Tag.setEnabled(True)

        self.MediaPlayer.actionClose_Tag.setEnabled(True)
        self.close()

    # no clicked

    def no_Clicked(self):
        self.close()

    # close current tag in Media

    def closeTag(self):
        self.MediaPlayer.allTag = {}
        self.MediaPlayer.tag_Path = None
        self.MediaPlayer.ListWidget_Tags_of_file.clear()
        self.MediaPlayer.sch_listWidget.clear()
        self.MediaPlayer.Setting.Edit_tag_Listwidget.clear()
