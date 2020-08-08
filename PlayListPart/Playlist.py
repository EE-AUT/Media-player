import os
import re
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtMultimedia import QMediaContent


Form = uic.loadUiType(os.path.join(os.getcwd(), 'PlayListPart/Playlist.ui'))[0]


class PlaylistWindow(QMainWindow, Form):
    def __init__(self, MediaPlayer):
        QMainWindow.__init__(self, parent=MediaPlayer)
        Form.__init__(self)
        self.setupUi(self)
        self.MediaPlayer = MediaPlayer
        self.File_Path = os.getcwd()
        # To save File of play list , keys are name of file and values are directories of file
        self.Files = dict()

        # To Specialize flags
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowStaysOnTopHint
        )

        self.pushButton_Close.clicked.connect(lambda: self.close())
        self.listWidget_Playlist.itemActivated.connect(self.listview_clicked)
        self.pushButton_Add.clicked.connect(self.add_file)
        self.pushButton_Delete.clicked.connect(self.del_file)

    def Create_Playlist(self, file_path):
        self.listWidget_Playlist.clear()
        self.FileName = file_path.split("/")[-1]
        File_format = self.FileName.split(".")[-1]
        self.MediaPlayer.setWindowTitle(f" Media Player - {self.FileName}")
        self.File_Path = file_path.replace(f"{self.FileName}", "")
        list_File = os.listdir(self.File_Path)  # File of directory
        list_File.sort(key=lambda x: len(x))  # Sort file
        # Create a dictionary for Files that keys of it are files name and values of it is file path
        self.Files = dict((file, f'{self.File_Path}{file}') for file in list_File if re.search(
            f'.{File_format}', file))  # Create Files
        for file in self.Files:
            self.listWidget_Playlist.addItem(
                f'{self.listWidget_Playlist.count()+1} . {file}')  # Add file to listWidget in playlist
            # To set current item of list that is playing
            if file == self.FileName:
                self.listWidget_Playlist.setCurrentItem(
                    self.listWidget_Playlist.item(list(self.Files.keys()).index(file)))
        # To Enable Next and previous PushButton

        # Reset to Disable Next and previous PushButton
        self.MediaPlayer.pushButton_next.setEnabled(False)
        self.MediaPlayer.pushButton_previous.setEnabled(False)

        # To Enable Next and previous PushButton According to current file
        if self.listWidget_Playlist.currentRow():
            self.MediaPlayer.pushButton_previous.setEnabled(True)
        if self.listWidget_Playlist.currentRow() != self.listWidget_Playlist.count()-1:
            self.MediaPlayer.pushButton_next.setEnabled(True)

        # To update part of Tags of file  Dackwidget
        self.MediaPlayer.ComboBox_Tags_of_file.clear()
        self.MediaPlayer.ComboBox_Tags_of_file.addItems(self.Files.keys())
        self.MediaPlayer.Setting.comboBox_Tag.addItems(self.Files.keys())
        index = self.MediaPlayer.ComboBox_Tags_of_file.findText(self.FileName)
        self.MediaPlayer.ComboBox_Tags_of_file.setCurrentIndex(index)
        self.MediaPlayer.Setting.comboBox_Tag.setCurrentIndex(index)

    def listview_clicked(self, val):
        self.spliter = len(str(self.listWidget_Playlist.currentRow()+1)) + 3

        # Set Media in MediaPlayer and play it
        self.MediaPlayer.player.setMedia(QMediaContent(
            QtCore.QUrl.fromLocalFile(self.Files[val.text()[self.spliter:]])))
        self.MediaPlayer.start()

        # Reset to Disable Next and previous PushButton
        self.MediaPlayer.pushButton_next.setEnabled(False)
        self.MediaPlayer.pushButton_previous.setEnabled(False)

        # To Enable Next and previous PushButton According to current file
        if self.listWidget_Playlist.currentRow():
            self.MediaPlayer.pushButton_previous.setEnabled(True)
        if self.listWidget_Playlist.currentRow() != self.listWidget_Playlist.count()-1:
            self.MediaPlayer.pushButton_next.setEnabled(True)

        self.MediaPlayer.pushButton_stop.setEnabled(True)
        self.MediaPlayer.setWindowTitle(
            f" Media Player - {val.text()[self.spliter:]}")
        self.MediaPlayer.pushButton_volume.setEnabled(True)
        self.MediaPlayer.pushButton_volume.setIcon(
            QtGui.QIcon('./Icons/unmute.png'))
        self.MediaPlayer.pushButton_volume.setToolTip("Mute")
        if not self.MediaPlayer.isFullScreen():
            self.MediaPlayer.pushButton_BookMark.setVisible(True)

        # Updata combo and listwidget of tags
        currentText = val.text()[self.spliter:]
        index = self.MediaPlayer.ComboBox_Tags_of_file.findText(currentText)
        self.MediaPlayer.ComboBox_Tags_of_file.setCurrentIndex(index)
        self.MediaPlayer.Setting.comboBox_Tag.setCurrentIndex(index)
        self.MediaPlayer.set_TagonListwidget(
            ".".join(currentText.split(".")[:-1]))

    def add_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open video", directory=self.File_Path, filter='*.mp4 *.mkv *.mp3')
        if file_path:
            file_name = file_path.split("/")[-1]
            if not file_name in self.Files.keys():
                self.Files[file_name] = file_path  # Add to files
                self.listWidget_Playlist.addItem(
                    f'{self.listWidget_Playlist.count()+1} . {file_name}')  # Add to listwidget in playlist

        # To update part of Tags of file  Dackwidget
        self.MediaPlayer.ComboBox_Tags_of_file.clear()
        self.MediaPlayer.ComboBox_Tags_of_file.addItems(self.Files.keys())
        self.MediaPlayer.Setting.comboBox_Tag.addItems(self.Files.keys())

    def del_file(self):
        self.spliter = len(
            str(self.listWidget_Playlist.currentRow()+1)) + 3
        Selected_Item = self.listWidget_Playlist.currentItem().text()[
            self.spliter:]
        # If the selected Item is playing
        if Selected_Item == self.MediaPlayer.windowTitle()[16:]:
            index = list(self.Files.keys()).index(Selected_Item)

        if self.listWidget_Playlist.count():
            self.Files.pop(Selected_Item)  # delete from Files
            self.listWidget_Playlist.clear()
            for file in self.Files:  # rewrite listwidget of playlist
                self.listWidget_Playlist.addItem(
                    f'{self.listWidget_Playlist.count()+1} . {file}')

        # If the selected Item is playing
        if Selected_Item == self.MediaPlayer.windowTitle()[16:]:
            self.listWidget_Playlist.setCurrentRow(index-1)
        if self.MediaPlayer.windowTitle()[16:] in self.Files.keys():
            # If the playing Item is last item
            if list(self.Files.keys()).index(self.MediaPlayer.windowTitle()[16:]) == self.listWidget_Playlist.count()-1:
                self.MediaPlayer.pushButton_next.setEnabled(False)
            # If the playing Item is first item
            if list(self.Files.keys()).index(self.MediaPlayer.windowTitle()[16:]) == 0:
                self.MediaPlayer.pushButton_previous.setEnabled(False)
        # To update part of Tags of file  Dackwidget
        self.MediaPlayer.ComboBox_Tags_of_file.clear()
        self.MediaPlayer.ComboBox_Tags_of_file.addItems(self.Files.keys())
        self.MediaPlayer.Setting.comboBox_Tag.addItems(self.Files.keys())
