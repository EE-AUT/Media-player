import sys
import os
import csv
import re
import subprocess
from time import sleep
import LoginPart.Login as Login
import SettingPart.Setting as Setting
import PlayListPart.Playlist as Playlist
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QLabel, QFrame, QMainWindow, QComboBox, QVBoxLayout, QDockWidget, QMenuBar, QFileDialog, QLineEdit, QListWidget, QSlider, QShortcut, QTreeWidgetItem, QGraphicsView, QDialog
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QKeySequence
from tagPart import readTag
from bookmarkPart.bookmark import add_Bookmark
from editPart import timeconvert as tc
from SearchPart import searchTag as STag
import SettingPart.Theme as Theme_module
from userWinPart.confirm import confrimWin
import FullScreen.Fullscreen as Full_screen

Form = uic.loadUiType(os.path.join(os.getcwd(), 'Mediaplayer.ui'))[0]


class MediaPlayer(QMainWindow, Form):
    def __init__(self):
        Form.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        # Video Part
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(self.videowidget)
        self.setWindowTitle(" Media Player")
        self.setAcceptDrops(True)

        # Define some Events
        self.videowidget.mouseDoubleClickEvent = self.Doubleclick_mouse
        self.wheelEvent = self.Scroll_mouse
        self.mouseReleaseEvent = self.MainWindow_Event
        self.videowidget.mouseMoveEvent = self.MousePos
        self.resizeEvent = self.main_size_Change

        self.lineEdit_Bookmark.setVisible(False)
        self.lineEdit_Bookmark.returnPressed.connect(self.save_Bookmarks)

        # threads part
        self.tag_thread = None
        self.search_Thread = None
        self.SearchAnimation = None
        self.BookMarkAnimation = None

        # Create Tags
        self.allTag = {}
        self.tag_Path = None

        # create Volume Slide
        self.Slider_Volume = Slider(self)
        self.Slider_Volume.setOrientation(Qt.Horizontal)
        self.horizontalLayout_3.addWidget(self.Slider_Volume, 0)
        self.Slider_Volume.setMaximumWidth(100)
        self.Slider_Volume.setMaximumHeight(30)

        # create Play Slider
        self.Slider_Play = Slider(self)
        self.Slider_Play.setOrientation(Qt.Horizontal)
        self.Slider_Play.resize(644, 22)
        self.horizontalLayout_4.addWidget(self.label_Time)
        self.horizontalLayout_4.addWidget(self.Slider_Play)
        self.horizontalLayout_4.addWidget(self.label_Duration)

        # To Apply initial Theme
        self.Setting = Setting.SettingWindow(self)
        Theme_module.Theme_apply(self.Setting)

        # PushButttons
        self.pushButton_Start.setEnabled(False)
        self.pushButton_Start.clicked.connect(self.start)

        self.pushButton_volume.setEnabled(False)
        self.pushButton_volume.clicked.connect(self.volumeOnOff)

        self.pushButton_stop.setEnabled(False)
        self.pushButton_stop.clicked.connect(self.stop)
        self.pushButton_stop.setToolTip("Stop (Ctrl+Z)")

        self.pushButton_next.setEnabled(False)
        self.pushButton_next.clicked.connect(self.next)
        self.pushButton_next.setToolTip("Next (PgUp)")

        self.pushButton_previous.setEnabled(False)
        self.pushButton_previous.clicked.connect(self.previous)
        self.pushButton_previous.setToolTip("Previous (PgDn)")

        self.pushButton_open.clicked.connect(self.Load_video)
        self.pushButton_open.setToolTip("Open (Ctrl+O)")

        self.pushButton_Search.clicked.connect(self.sch_icon_Event)
        self.pushButton_Search.setToolTip("Search (Ctrl+S)")

        self.pushButton_BookMark.setVisible(False)
        self.pushButton_BookMark.clicked.connect(self.add_BookMarks)
        self.pushButton_BookMark.setToolTip("Add BookMark (Ctrl+B)")

        self.pushButton_Setting.clicked.connect(self.Settingshow)
        self.pushButton_Setting.setToolTip("Setting")

        self.pushButton_Playlist.clicked.connect(self.Play_list)
        self.pushButton_Playlist.setToolTip("Play list")
        self.PlaylistW = Playlist.PlaylistWindow(self)

        # Create Tags of file Dockwidget
        self.pushButton_Tag_of_file.clicked.connect(self.Show_Tags_of_file)
        self.pushButton_Tag_of_file.setToolTip("Tags of file")
        self.DockWidget_Tags_of_file = QDockWidget("Tags of file", self)
        self.DockWidget_Tags_of_file.setVisible(False)
        self.DockWidget_Tags_of_file.setMinimumWidth(150)
        self.ComboBox_Tags_of_file = QComboBox(self)
        self.ListWidget_Tags_of_file = QListWidget()
        widget = QWidget()  # Create Widget for Tags of file DockWidget
        layout = QVBoxLayout()  # Create Layout for Tags of file DockWidget
        # Add Listwiget and ComboBox to layout
        layout.addWidget(self.ComboBox_Tags_of_file)
        layout.addWidget(self.ListWidget_Tags_of_file)
        widget.setLayout(layout)  # Set layout on the widget
        # set Widget on Tags of file DockWidget
        self.DockWidget_Tags_of_file.setWidget(widget)
        self.addDockWidget(Qt.RightDockWidgetArea,
                           self.DockWidget_Tags_of_file)
        self.ComboBox_Tags_of_file.activated.connect(self.ListWidget_Tag)
        self.ListWidget_Tags_of_file.itemActivated.connect(self.GoToTagtime)

        # Slider Play
        self.Slider_Play.setRange(0, 0)
        self.player.positionChanged.connect(self.Position_changed)
        self.player.durationChanged.connect(self.Duration_changed)
        self.Slider_Play.setUP_Slider.connect(self.Set_Position)
        self.Slider_Play.moveMent_Position.connect(self.slider_play_pos)

        # Label Time
        self.Slider_play_label = QLabel("Time", parent=self)
        self.Slider_play_label.resize(50, 20)
        self.Slider_play_label.setAlignment(Qt.AlignCenter)
        self.Slider_play_label.setVisible(False)

        # Slider Volume
        self.Slider_Volume.setRange(0, 0)
        self.Slider_Volume.setUP_Slider.connect(self.Set_volume)
        self.Slider_Volume.moveMent_Position.connect(self.slider_volume_pos)

        # Label Volume
        self.Slider_Volume_label = QLabel("Volume", parent=self)
        self.Slider_Volume_label.resize(30, 20)
        self.Slider_Volume_label.setAlignment(Qt.AlignCenter)
        self.Slider_Volume_label.setVisible(False)

        # Create listWidget for search part
        self.sch_listWidget = QListWidget(self)
        self.sch_listWidget.setVisible(False)
        self.search_lineEdit.setVisible(False)
        # Search signals
        self.sch_listWidget.itemDoubleClicked.connect(
            self.item_searchlist_Event)
        self.search_lineEdit.textChanged.connect(self.search_Tag)

        # Define Action for Tool Bar
        self.actionOpen.triggered.connect(self.Load_video)
        self.actionChange_Password.triggered.connect(self.menuBarAccout)
        self.actionDelete_Account.triggered.connect(self.menuBarAccout)

        self.actionLogOut.triggered.connect(self.Logout)
        self.actionExit.triggered.connect(lambda: self.close())

        self.actionFullScreen.triggered.connect(self.fullscreen)
        self.actionSpeed.triggered.connect(self.menuBarSpeed)
        self.actionThme.triggered.connect(self.menuBarTheme)
        self.actionFont.triggered.connect(self.menuBarFont)

        self.actionCreate_Tag.triggered.connect(self.menuBarCreateTag)
        self.actionOpen_Tags.triggered.connect(self.openTags)
        self.actionEdit_Tag.triggered.connect(self.menuBarEditTag)
        self.actionClose_Tag.triggered.connect(self.menuBarCloseTag)

        # Shortcut
        QShortcut(QKeySequence('Ctrl+B'),
                  self).activated.connect(self.add_BookMarks)
        QShortcut(QKeySequence('Ctrl+Z'),
                  self).activated.connect(self.stop)
        QShortcut(QKeySequence('Ctrl+M'),
                  self).activated.connect(self.volumeOnOff)
        QShortcut(QKeySequence('Ctrl+S'),
                  self).activated.connect(self.sch_icon_Event)
        QShortcut(QKeySequence('Ctrl+O'),
                  self).activated.connect(self.Load_video)

        # For FullScreen part
        self.firstTime_fullscreen = True

        # close event to stop running thread
        self.closeEvent = self.Close

    # KeyPress Event
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown and self.pushButton_next.isEnabled():
            self.next()
        if event.key() == Qt.Key_PageUp and self.pushButton_previous.isEnabled():
            self.previous()
        if event.key() == Qt.Key_F5:
            self.fullscreen()
        if event.key() == Qt.Key_6:
            self.Move_Slider_play(self.width()*4500/self.player.duration())
        if event.key() == Qt.Key_4:
            self.Move_Slider_play(
                (-1*self.width()*4500/self.player.duration()))
        if event.key() == Qt.Key_8:
            self.Move_Slider_volume(+1)
        if event.key() == Qt.Key_2:
            self.Move_Slider_volume(-1)

    def menuBarTheme(self):
        # Open Theme Tab of Setting Window
        self.Setting.Account_changing = False
        self.Settingshow()
        self.Setting.Tab.setCurrentIndex(0)

    def menuBarFont(self):
        # Open Font Tab of Setting Window
        self.Setting.Account_changing = False
        self.Settingshow()
        self.Setting.Tab.setCurrentIndex(1)

    def menuBarSpeed(self):
        # Open Speed Tab of Setting Window
        self.Setting.Account_changing = False
        self.Settingshow()
        self.Setting.Tab.setCurrentIndex(2)

    def menuBarEditTag(self):
        # Open Tag Tab of Setting Window
        self.Setting.Account_changing = False
        self.Settingshow()
        self.Setting.Tab.setCurrentIndex(3)

    def menuBarAccout(self):
        # Open Account Tab of Setting Window
        self.Setting.Account_changing = False
        self.Settingshow()
        self.Setting.Tab.setCurrentIndex(4)

    def menuBarCreateTag(self):
        # create new Tag file
        if self.tag_Path:
            self.confirmCloseTag = confrimWin(self, Title="Create Tag",
                                              Text="Are you sure to close current tag and create new one")
            self.actionCreate_Tag.setEnabled(False)
            self.confirmCloseTag.show()
        else:
            dialog = QFileDialog(self, 'File tag', directory=os.getcwd())
            _path = dialog.getSaveFileName(filter= "*.csv")[0]
            try:
                if _path:
                    self.tag_Path = _path
                    open(self.tag_Path, "w")
            except:
                pass


    def menuBarCloseTag(self):
        # close current tags
        if self.tag_Path:
            self.confirmCloseTag = confrimWin(
                self, Title="Close Tag", Text="Are you sure to close current tag")
            self.confirmCloseTag.show()
            self.actionClose_Tag.setEnabled(False)
        else:
            self.confirmCloseTag = confrimWin(
                self, Title="Warning", Text="There is no tag to close")
            self.confirmCloseTag.show()
            self.actionClose_Tag.setEnabled(False)

    def fullscreen(self):
        self.DockWidget_Tags_of_file.setVisible(False)
        self.Slider_play_label.setVisible(False)
        self.Slider_Volume_label.setVisible(False)

        Full_screen.fullscreen(self)

    # Define some Events
    def MousePos(self, position):
        if self.isFullScreen():
            Full_screen.MousePosition(self, position)
        self.Slider_play_label.setVisible(False)
        self.Slider_Volume_label.setVisible(False)

    def Doubleclick_mouse(self, position):
        if self.pushButton_Start.isEnabled():
            self.start()

    def Scroll_mouse(self, event):
        if self.player.isAudioAvailable() or self.player.isVideoAvailable():
            self.Set_volume(int(self.player.volume() +
                                event.angleDelta().y()/120))

    def Move_Slider_play(self, move):
        if self.player.isAudioAvailable() or self.player.isVideoAvailable():
            Now = self.player.position()*self.Slider_Play.width()/self.player.duration()
            self.Set_Position(Now+move)

    def Move_Slider_volume(self, move):
        if self.player.isAudioAvailable() or self.player.isVideoAvailable():
            self.Set_volume(self.player.volume() + move)

    def Settingshow(self):
        # To show Setting window
        self.Setting.Tab.setCurrentIndex(0)
        self.Setting.lineEdit_CurrentPass.clear()
        self.Setting.lineEdit_NewPass.clear()
        self.Setting.lineEdit_ReNewpass.clear()
        self.Setting.label_finish.setVisible(False)
        self.Setting.label_NotMatch.setVisible(False)
        self.Setting.label_PassLong.setVisible(False)
        self.Setting.label_OldPass.setVisible(False)
        self.Setting.label_Wait.setVisible(False)
        self.Setting.label_Error.setVisible(False)
        self.Setting.Account_changing = False
        self.Setting.show()

    def start(self):
        # Start and Pause the player
        if self.player.state() == QMediaPlayer.PlayingState:  # Stop
            self.player.pause()
            self.pushButton_Start.setEnabled(True)
            self.pushButton_Start.setIcon(QIcon('./Icons/play.png'))
            self.pushButton_Start.setToolTip("Play")

        else:  # Start
            self.player.play()
            self.pushButton_Start.setEnabled(True)
            self.pushButton_Start.setIcon(QIcon('./Icons/pause.png'))
            self.pushButton_Start.setToolTip("Pause")
        self.pushButton_Start.setFocus(True)

    def stop(self):
        # Stop player
        if self.player.isAudioAvailable() or self.player.isVideoAvailable():
            self.player.stop()
            self.pushButton_next.setEnabled(False)
            self.pushButton_previous.setEnabled(False)
            self.pushButton_volume.setEnabled(False)
            self.pushButton_Start.setEnabled(False)
            self.pushButton_stop.setEnabled(False)
            self.pushButton_BookMark.setVisible(False)
            self.label_Duration.setText("00:00:00")
            self.label_Time.setText("00:00:00")
            self.Slider_Volume.setEnabled(False)

    def next(self):
        # Play next file from playlist
        # If the playing file is in the playlist
        if self.windowTitle()[16:] in self.PlaylistW.Files.keys():
            self.PlaylistW.listWidget_Playlist.setCurrentRow(
                list(self.PlaylistW.Files.keys()).index(self.windowTitle()[16:])+1)
        else:  # If the playing file is not in the playlist
            self.PlaylistW.listWidget_Playlist.setCurrentRow(
                self.PlaylistW.listWidget_Playlist.currentRow()+1)

        self.PlaylistW.spliter = len(
            str(self.PlaylistW.listWidget_Playlist.currentRow()+1)) + 3
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(
            self.PlaylistW.Files[self.PlaylistW.listWidget_Playlist.currentItem().text()[self.PlaylistW.spliter:]])))
        # Change title
        self.setWindowTitle(
            f" Media Player - {self.PlaylistW.listWidget_Playlist.currentItem().text()[self.PlaylistW.spliter:]}")
        currentText = self.PlaylistW.listWidget_Playlist.currentItem().text()[
            self.PlaylistW.spliter:]
        index = self.ComboBox_Tags_of_file.findText(currentText)
        self.ComboBox_Tags_of_file.setCurrentIndex(index)
        self.set_TagonListwidget(".".join(currentText.split(".")[:-1]))
        self.start()
        # To handle Next button
        if self.PlaylistW.listWidget_Playlist.currentRow() == self.PlaylistW.listWidget_Playlist.count()-1:
            self.pushButton_next.setEnabled(False)

        self.pushButton_previous.setEnabled(True)

    def previous(self):
        # Play previous file from playlist
        # If the playing file is in the playlist
        if self.windowTitle()[16:] in self.PlaylistW.Files.keys():
            self.PlaylistW.listWidget_Playlist.setCurrentRow(
                list(self.PlaylistW.Files.keys()).index(self.windowTitle()[16:])-1)
        else:  # If the playing file is not in the playlist
            self.PlaylistW.listWidget_Playlist.setCurrentRow(
                self.PlaylistW.listWidget_Playlist.currentRow())

        self.PlaylistW.spliter = len(
            str(self.PlaylistW.listWidget_Playlist.currentRow()+1)) + 3

        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(
            self.PlaylistW.Files[self.PlaylistW.listWidget_Playlist.currentItem().text()[self.PlaylistW.spliter:]])))
        self.setWindowTitle(
            f" Media Player - {self.PlaylistW.listWidget_Playlist.currentItem().text()[self.PlaylistW.spliter:]}")
        currentText = self.PlaylistW.listWidget_Playlist.currentItem().text()[
            self.PlaylistW.spliter:]
        index = self.ComboBox_Tags_of_file.findText(currentText)
        self.ComboBox_Tags_of_file.setCurrentIndex(index)
        self.set_TagonListwidget(".".join(currentText.split(".")[:-1]))
        self.start()

        # To handle previous button
        if not self.PlaylistW.listWidget_Playlist.currentRow():
            self.pushButton_previous.setEnabled(False)
        self.pushButton_next.setEnabled(True)

    def Load_video(self, filepath=None):
        # Load Files of directory
        # just mp4 ,mkv , mp3
        if not filepath:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Open video", directory=os.path.join(os.getcwd(), 'Video'), filter='*.mp4 *.mkv *.mp3')
        else:
            file_path = filepath

        if file_path:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.start()
            self.pushButton_volume.setEnabled(True)
            self.pushButton_volume.setIcon(QIcon('./Icons/unmute.png'))
            self.pushButton_volume.setToolTip("Mute (Ctrl+M)")
            if not self.isFullScreen():
                self.pushButton_BookMark.setVisible(True)
            self.pushButton_stop.setEnabled(True)
            # Handle Volume Slider
            self.Slider_Volume.setEnabled(True)
            self.Slider_Volume.setRange(0, self.player.volume())
            self.Slider_Volume.setValue(60)
            self.player.setVolume(60)

            # Create Playlist
            self.Setting.comboBox_Tag.clear()
            self.ComboBox_Tags_of_file.clear()
            self.PlaylistW.Create_Playlist(file_path)
            self.set_TagonListwidget(".".join(self.windowTitle()[16:].split(".")[:-1]))

    def Position_changed(self, position):
        if position > self.player.duration():
            position = self.player.duration()
        if self.player.isAudioAvailable() or self.player.isVideoAvailable():
            hour = position//(1000*3600)
            minute = (position % (1000*3600))//(60*1000)
            second = ((position % (1000*3600)) % (60*1000))//1000
            # Show Time
            self.label_Time.setText(
                f'{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}')
        # Automatic Next
        if self.player.duration() and position == self.player.duration():
            if self.pushButton_next.isEnabled():
                self.next()
            else:
                self.stop()
        self.Slider_Play.setValue(position)

    def Duration_changed(self, duration):
        # To set file duration
        self.Slider_Play.setRange(0, duration)
        # convert millsec to xx:xx:xx format
        hour = duration//(1000*3600)
        minute = (duration % (1000*3600))//(60*1000)
        second = ((duration % (1000*3600)) % (60*1000))//1000
        self.label_Duration.setText(
            f'{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}')

        self.Slider_Volume.setEnabled(True)

    def Set_Position(self, position):
        if self.Slider_Play.width()-1 <= position:
            position = self.Slider_Play.width()-1
            self.player.pause()
            self.pushButton_Start.setEnabled(True)
            self.pushButton_Start.setIcon(QIcon('./Icons/play.png'))
            self.pushButton_Start.setToolTip("Paly")

        # if not (position < 0 and position > self.Slider_Play.width()):
        position = int(self.player.duration() *
                       (position / self.Slider_Play.width()))
        self.Slider_Play.setValue(position)
        self.player.setPosition(position)

    def slider_play_pos(self, position):
        if self.player.isAudioAvailable() or self.player.isVideoAvailable():
            # Convert Width of Slider to time
            Time = int(self.player.duration() *
                       position/self.Slider_Play.width())
            # convert millsec to xx:xx:xx format
            hour = Time//(1000*3600)
            minute = (Time % (1000*3600))//(60*1000)
            second = ((Time % (1000*3600)) % (60*1000))//1000
            self.Slider_play_label.setText(
                f'{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}')
            if self.isFullScreen():
                self.Slider_play_label.move(
                    position+self.Slider_Play.x(), self.height()-65)
            else:
                self.Slider_play_label.move(
                    position+self.Slider_Play.x(), self.height()-80)
            self.Slider_play_label.setVisible(True)

    def slider_volume_pos(self, position):
        if self.player.isAudioAvailable() or self.player.isVideoAvailable():
            # Convert Width of Slider to volume
            volume = int(100*position/self.Slider_Volume.width())
            self.Slider_Volume_label.setText(f'{volume}%')
            if self.isFullScreen():
                self.Slider_Volume_label.move(
                    position + self.Slider_Volume.x()-5, self.height()-37)
            else:
                self.Slider_Volume_label.move(
                    position + self.Slider_Volume.x()-5, self.height()-48)
            self.Slider_Volume_label.setVisible(True)

    def Set_volume(self, volume):
        if self.player.isAudioAvailable() or self.player.isVideoAvailable():
            # Volume must be between 0 , 100
            if 100 <= volume:
                volume = 100
            elif volume <= 0:
                volume = 0

            if not volume:
                self.player.setMuted(True)
                self.pushButton_volume.setIcon(QIcon('./Icons/mute.png'))
                self.pushButton_volume.setToolTip("UnMute (Ctrl+M)")

            else:
                self.player.setMuted(False)
                self.pushButton_volume.setIcon(QIcon('./Icons/unmute.png'))
                self.pushButton_volume.setToolTip("Mute (Ctrl+M)")

            self.Slider_Volume.setValue(volume)
            self.player.setVolume(volume)

    def volumeOnOff(self):
        """Mute and unmute"""
        if self.player.isAudioAvailable() or self.player.isVideoAvailable():
            if self.player.isMuted():
                self.player.setMuted(False)
                self.pushButton_volume.setIcon(QIcon('./Icons/unmute.png'))
                self.pushButton_volume.setToolTip("Mute (Ctrl+M)")
            else:
                self.player.setMuted(True)
                self.pushButton_volume.setIcon(QIcon('./Icons/mute.png'))
                self.pushButton_volume.setToolTip("UnMute (Ctrl+M)")

    # save bookmarks and updatae tag list widget
    def save_Bookmarks(self):
        try:
            # use add bookmark function to add bookmarks in tag part
            add_Bookmark(
                self.lineEdit_Bookmark.text() + "#" + tc.millis_to_format(self.player.position()),
                ".".join(self.windowTitle()[16:].split(".")[:-1]), self.tag_Path)
            # there isn't any tags for movie we want to add bookmark it
            if not ".".join(self.windowTitle()[16:].split(".")[:-1]) in self.allTag:
                self.allTag.update({".".join(self.windowTitle()[16:].split(".")[:-1]): {}})
            self.allTag[".".join(self.windowTitle()[16:].split(".")[:-1])].update(
                {self.lineEdit_Bookmark.text(): tc.millis_to_format(self.player.position())})
            self.set_TagonListwidget(self.windowTitle()[16:].split(".")[
                                     0])  # update tag listwidget
            # update combo box of edit and Main window
            index = self.ComboBox_Tags_of_file.findText(self.windowTitle()[16:])
            self.ComboBox_Tags_of_file.setCurrentIndex(index)
            index = self.Setting.comboBox_Tag.findText(self.windowTitle()[16:])
            self.Setting.comboBox_Tag.setCurrentIndex(index)
            # ****
            

        except:
            pass

        self.lineEdit_Bookmark.clear()
        self.lineEdit_Bookmark.setVisible(False)

    def sch_icon_Event(self):
        # Show search lineEdit to search
        self.search_lineEdit.setFixedWidth(0)

        # Start Animation of search lineEdit
        self.SearchAnimation = Search_Animation(self)
        self.SearchAnimation.update_Animation.connect(
            self.Update_Search_Animation)
        self.pushButton_Search.setEnabled(False)
        self.SearchAnimation.start()

        self.search_lineEdit.setVisible(True)
        self.search_lineEdit.setFocus(True)

    def Update_Search_Animation(self, size):
        if size == -1:  # Animation is finished
            self.pushButton_Search.setEnabled(True)
        else:  # Animation is running
            self.search_lineEdit.setFixedWidth(size)

    def add_BookMarks(self):
        # Show Bookmark lineEdit to search

        if self.player.isVideoAvailable() or self.player.isAudioAvailable():
            self.lineEdit_Bookmark.setFixedWidth(0)

            # Start Animation of search lineEdit
            self.BookMarkAnimation = BookMark_Animation(self)
            self.BookMarkAnimation.update_Animation.connect(
                self.Update_BookMark_Animation)

            self.pushButton_BookMark.setEnabled(False)
            self.BookMarkAnimation.start()

            self.lineEdit_Bookmark.setVisible(True)
            self.lineEdit_Bookmark.setFocus(True)

    def Update_BookMark_Animation(self, size):
        if size == -1:  # Animation is finished
            self.pushButton_BookMark.setEnabled(True)
        else:  # Animation is running
            self.lineEdit_Bookmark.setFixedWidth(size)

    def MainWindow_Event(self, type):
        # Click on MainWindow
        self.search_lineEdit.setText("")
        self.search_lineEdit.setVisible(False)

        self.lineEdit_Bookmark.setText("")
        self.lineEdit_Bookmark.setVisible(False)

        self.sch_listWidget.setVisible(False)
        self.sch_listWidget.clear()

    # handle main size change to set correct size to
    # search and bookmark line edits and searchlistwidgetd
    def main_size_Change(self, val):
        self.lineEdit_Bookmark.setFixedWidth(int(self.size().width()/4))
        self.search_lineEdit.setFixedWidth(int(self.size().width()/4))

        self.sch_listWidget.resize(  # Handle size of search listwidget
            int(self.size().width()/4), int((200 / 600) * self.size().height()))
        self.sch_listWidget.move(  # Move search listwidget
            self.size().width()-self.pushButton_Search.geometry().width()-self.search_lineEdit.geometry().width()-15, self.search_lineEdit.geometry().height()+self.search_lineEdit.pos().y() + self.menubar.geometry().height())

    # Item clicked event in search tag part
    def item_searchlist_Event(self, item):
        session, tag = re.split(" -> ", item.text())
        # get all session to compare that is selected tag in playlist or user select tag wrong
        all_sessions = list(self.PlaylistW.Files.keys())
        # there is bug here if mp3 and mp4 has same name
        all_sessions = [".".join(item.split(".")[:-1]) for item in all_sessions]
        if session in all_sessions:
            if session != ".".join(self.windowTitle()[16:].split(".")[:-1]):
                # Show confirm window to get accept user for change video
                self.confirmWin = confrimWin(self, session=".".join(session.split(".")[:-1]),
                                            tag_Text=tag, Text=f"Are you sure to change video to {session} from search")
                self.confirmWin.show()
            else:
                try:
                    # concert time format to second for using in change position
                    time_second = tc.to_second(self.allTag[session][tag])
                    self.change_Position(time_second)
                except:  # handle unexcepted error!
                    pass
        else:
            Warning_user_wrongTags = confrimWin(self, Title= "Warning", Text= "You has opened wrong tag files, please be care")
            Warning_user_wrongTags.show()

    # Create search listwidget and running thread to starting search

    def search_Tag(self, val):
        # Create QListWidget
        self.sch_listWidget.resize(
            int((200 / 800) * self.size().width()), int((200 / 600) * self.size().height()))
        self.sch_listWidget.move(
            self.search_lineEdit.x(), self.search_lineEdit.geometry().height()+self.search_lineEdit.pos().y() + self.menubar.geometry().height())

        self.sch_listWidget.setVisible(True)
        if val == "":
            self.sch_listWidget.clear()
        # start search thread
        else:
            self.search_Thread = search_thread(self, self.allTag, val)
            self.search_Thread.update_schTag.connect(self.update_searchTags)
            self.search_Thread.start()

    # Update searchtags function to update search widget by searching instantly
    def update_searchTags(self, tagsDict):
        self.sch_listWidget.clear()  # clear search list widget

        for session, Tags in tagsDict.items():  # writing data on search listwidget
            for text in Tags:
                self.sch_listWidget.addItem(session + " -> " + text)

    def Logout(self):
        os.remove("LoginPart/User.csv")
        self.close()
        self.player.stop()
        subprocess.call(['python', 'MediaPlayer.py'])  # Start again

    def Play_list(self):
        # Open playlist
        # To show current Row for every time it is opened
        if self.PlaylistW.listWidget_Playlist.count():
            self.PlaylistW.listWidget_Playlist.setCurrentRow(
                list(self.PlaylistW.Files.keys()).index(self.windowTitle()[16:]))

        self.PlaylistW.show()
        # setPosition of playlist when it is opened
        self.PlaylistW.move(QtGui.QCursor().pos().x(),
                            QtGui.QCursor().pos().y()-self.PlaylistW.size().height()-25)

    def Show_Tags_of_file(self):
        # To show Tags of file in DockWidget
        self.DockWidget_Tags_of_file.setVisible(
            not self.DockWidget_Tags_of_file.isVisible())
        index = self.ComboBox_Tags_of_file.findText(self.windowTitle()[16:])
        self.ComboBox_Tags_of_file.setCurrentIndex(index)
        # To Change features of the Dockwidget according Fullscreen
        if self.isFullScreen():
            self.DockWidget_Tags_of_file.setFeatures(
                QDockWidget.DockWidgetClosable)
            Full_screen.Set_visible(self, False)

        else:  # To Change features of the Dockwidget according Normalscreen
            self.DockWidget_Tags_of_file.setFeatures(
                QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)

    def ListWidget_Tag(self, index):
        """Tag combo box item clicked function"""
        videoName = ".".join(list(self.PlaylistW.Files.keys())[index].split(".")[:-1])
        self.set_TagonListwidget(videoName, Setting_Tags=False)

    def openTags(self):
        """OpenTag in csv, pptx, docx format and start tag thread for reading data"""

        self.tag_Path, _ = QFileDialog.getOpenFileName(
            self, "Open Tag", directory=os.path.join(os.getcwd(), 'Tags'), filter='*.csv *.pptx *.docx')
        # if tagpath is correct we starting tag_thread to read tags from path
        if self.tag_Path:
            self.Tagname = self.tag_Path.split("/")[-1]
            fileFormat = self.Tagname.split(".")[-1]
            self.tag_thread = read_Tag(self, self.tag_Path, fileFormat)
            self.tag_thread.Tag_Ready.connect(self.getTag)
            self.tag_thread.start()

    # Tag is ready to use
    # if tags ready we shoud save them in self.allTag variable to use them properly

    def getTag(self, tags):
        self.allTag = tags
        index = self.ComboBox_Tags_of_file.findText(self.windowTitle()[16:])
        self.ComboBox_Tags_of_file.setCurrentIndex(index)
        self.set_TagonListwidget(".".join(self.windowTitle()[16:].split(".")[:-1]))

    # set tags on tag listwidget using vedio name
    # update tags

    def set_TagonListwidget(self, videoName, Setting_Tags=True, Media_Tags=True):
        if Media_Tags:
            self.ListWidget_Tags_of_file.clear()
        if Setting_Tags:
            self.Setting.Edit_tag_Listwidget.clear()
        try:
            if videoName in self.allTag:
                sessionTag = self.allTag[videoName]
                # sorted tags by time
                sessionTag = {text: time for text, time in sorted(
                    sessionTag.items(), key=lambda item: tc.to_second(item[1]))}
                for text in sessionTag:
                    # setting part tags by qtreewidget
                    if Setting_Tags:
                        item = QTreeWidgetItem(
                            self.Setting.Edit_tag_Listwidget, [text, sessionTag[text]])
                    # media part tags by qlistwidget
                    if Media_Tags:
                        self.ListWidget_Tags_of_file.addItem(
                            f'{self.ListWidget_Tags_of_file.count()+1} . {text}')

        except:
            pass
    # item clicked event to go to time correlate clicked tag in video

    # change time when clicking on tags in search part and main listwidget if tags

    def GoToTagtime(self, item):
        spliter = len(str(self.ListWidget_Tags_of_file.currentRow()+1)) + 3
        tag_Text = item.text()[spliter:]
        # change time if clicked on tags that belong to playing session
        if self.windowTitle()[16:] == self.ComboBox_Tags_of_file.currentText():
            session = ".".join(self.windowTitle()[16:].split(".")[:-1])
            try:
                # convert time to seconds using tc mudole(write by own)
                time_second = tc.to_second(self.allTag[session][tag_Text])
                # using change position function to handle sliders and time
                self.change_Position(time_second)
            except:
                pass
        else:
            session = ".".join(self.ComboBox_Tags_of_file.currentText().split(".")[:-1])
            self.confirmWin = confrimWin(self, session=session,
                                         tag_Text=tag_Text, Text=f"Are you sure to change video to {session}")
            self.confirmWin.show()

    def change_Position(self, time_second):
        # change slider position using item time
        self.Slider_Play.setValue(int(time_second)*1000)
        # change video position using item time
        self.player.setPosition(int(time_second)*1000)

    # change video function to change video when clicked on
    # tags that there is not in current movie's tags

    def change_Video(self, session):
        for key in self.PlaylistW.Files:
            if re.search(session, key):
                self.player.setMedia(
                    QMediaContent(QUrl.fromLocalFile(self.PlaylistW.Files[key])))  # set video
                self.start()
                self.setWindowTitle(
                    f" Media Player - {key}")  # change title
                # update combo box of session in MediaPlayer
                index = self.ComboBox_Tags_of_file.findText(key)
                self.ComboBox_Tags_of_file.setCurrentIndex(
                    index)  # update combo box
                # update tags on setting and MediaPlayer window
                self.set_TagonListwidget(".".join(key.split(".")[:-1]))

                return True
        return False

    # close Event to stop runnig thread and preventing error
    def Close(self, val):
        if self.tag_thread:
            self.tag_thread.stop()
        if self.search_Thread:
            self.search_Thread.stop()
        if self.SearchAnimation:
            self.SearchAnimation.stop()
        if self.BookMarkAnimation:
            self.BookMarkAnimation.stop()

    # dragEnterEvent to hanle drag and drop option

    def dragEnterEvent(self, event):
        # pass
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    # dragMoveEvent to hanle drag and drop option
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    # dropEvent to hanle drag and drop option
    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            # get droppen file path
            file_path = event.mimeData().urls()[0].toLocalFile()
            file_format = (file_path.split("/")[-1]).split(".")[-1]
            desired_format = ['mp4', 'mkv', 'mp3']  # desired path to open
            if file_format in desired_format:  # check file format
                self.Load_video(filepath=file_path)


# custome slider for handling some event
# like mouse press and drag and mouse move event
class Slider(QSlider):
    setUP_Slider = QtCore.pyqtSignal(int)
    moveMent_Position = QtCore.pyqtSignal(int)

    def __init__(self, MediaPlayer):  # init function
        QSlider.__init__(self, parent=MediaPlayer)
        self.setMouseTracking(True)
        self.MediaPlayer = MediaPlayer

    def mousePressEvent(self, position):  # mouse pressed event
        self.setUP_Slider.emit(position.pos().x())

    def mouseMoveEvent(self, position):
        # simple movement event
        if position.buttons() == QtCore.Qt.NoButton:
            self.moveMent_Position.emit(position.x())

        # Drag slider event
        elif position.buttons() == QtCore.Qt.LeftButton:
            self.setUP_Slider.emit(position.x())

        # To Close label of slider
        if position.y() > self.height()-5 or position.y() < 5 or position.x() > self.width()-5 or position.x() < 5:
            self.MediaPlayer.Slider_play_label.setVisible(False)
            self.MediaPlayer.Slider_Volume_label.setVisible(False)


# thread for read data from csv or pptx or docx file
class read_Tag(QtCore.QThread):
    Tag_Ready = QtCore.pyqtSignal(dict)

    def __init__(self, window, filepath, fileFormat=csv):
        self.filepath = filepath
        self.fileFormat = fileFormat
        QtCore.QThread.__init__(self, parent=window)

    def run(self):
        # get data function using readTag mudole
        func = getattr(readTag, "read_" + str(self.fileFormat))
        tags = func(self.filepath)
        self.Tag_Ready.emit(tags)

    def stop(self):  # force thread to stop
        self.terminate()
        self.wait()


# Thread for searching in tags
class search_thread(QtCore.QThread):
    update_schTag = QtCore.pyqtSignal(dict)

    def __init__(self, window, Tags, word):
        self.word = word
        self.allTags = Tags
        QtCore.QThread.__init__(self, parent=window)

    def run(self):
        result = {}
        for key in self.allTags:
            result.update({key: STag.find_Closest_to(
                self.allTags[key], self.word)})
        self.update_schTag.emit(result)

    def stop(self):  # force thread to stop
        self.terminate()
        self.wait()


class Search_Animation(QtCore.QThread):
    update_Animation = QtCore.pyqtSignal(int)

    def __init__(self, window):
        QtCore.QThread.__init__(self, parent=window)

    def run(self):
        for i in range(int(Mainw.size().width()/8)):
            self.update_Animation.emit(2*i)
            sleep(0.001)
        # -1 is emitted when animation is finished
        self.update_Animation.emit(-1)

    def stop(self):  # force thread to stop
        self.terminate()
        self.wait()


class BookMark_Animation(QtCore.QThread):
    update_Animation = QtCore.pyqtSignal(int)

    def __init__(self, window):
        QtCore.QThread.__init__(self, parent=window)

    def run(self):
        for i in range(int(Mainw.size().width()/8)):
            self.update_Animation.emit(2*i)
            sleep(0.001)
        # -1 is emitted when animation is finished
        self.update_Animation.emit(-1)

    def stop(self):  # force thread to stop
        self.terminate()
        self.wait()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    if os.path.exists("LoginPart/User.csv"):
        Mainw = MediaPlayer()
        Mainw.show()
        app.exec_()
    else:
        Loginw = Login.LoginWindow()
        Loginw.show()
        app.exec_()
        if Loginw.LoginAccept():
            Mainw = MediaPlayer()
            Mainw.show()
            app.exec_()
