import sys
import os
import LoginPart.Login as Login
import SearchPart.tag as Tag
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QFileDialog, QLineEdit, QListWidget, QSlider
from PyQt5 import uic, QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon


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
        self.sch_listWidget = QListWidget(self)
        self.search_lineEdit = QLineEdit(self)
        self.sch_listWidget.setVisible(False)
        self.search_lineEdit.setVisible(False)
        self.mouseReleaseEvent = self.MainWindow_Event
        self.resizeEvent = self.main_size_Change
        self.search_Thread = None

        # Create Tags
        self.TagDB = None


        # create Slider
        self.Slider_Play = Slider(self)
        self.Slider_Play.setOrientation(Qt.Horizontal)
        self.Slider_Play.resize(644, 22)
        self.horizontalLayout_4.addWidget(self.Slider_Play, 1)
        self.horizontalLayout_4.addWidget(self.label_Time, 0)
        self.Duration = 0
        # StyleSheet for Slider_Play
        self.Slider_Play.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: white;
                height: 10px;
                border-radius: 4px;
            }

            QSlider::sub-page:horizontal {
                background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1, stop: 0 #66e, stop: 1 #bbf);
                background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, stop: 0 #bbf, stop: 1 #55f);
                border: 1px solid #777;
                height: 10px;
                border-radius: 4px;
            }
            
            QSlider::add-page:horizontal {
                background: #fff;
                border: 1px solid #777;
                height: 10px;
                border-radius: 4px;
            }
        """)

        # PushButtton
        self.pushButton_Start.setEnabled(False)
        self.pushButton_Start.mouseReleaseEvent
        self.pushButton_Start.clicked.connect(self.start)

        self.pushButton_volume.setEnabled(False)
        self.pushButton_volume.clicked.connect(self.volumeOnOff)

        self.pushButton_stop.setEnabled(False)
        self.pushButton_stop.clicked.connect(self.stop)

        self.pushButton_next.setEnabled(False)
        self.pushButton_next.clicked.connect(self.next)

        self.pushButton_previous.setEnabled(False)
        self.pushButton_previous.clicked.connect(self.previous)

        self.pushButton_open.clicked.connect(self.Load_video)

        self.pushButton_Search.clicked.connect(self.sch_icon_Event)

        # Slider Play
        self.Slider_Play.setRange(0, 0)
        self.player.positionChanged.connect(self.Position_changed)
        self.player.durationChanged.connect(self.Duration_changed)
        self.Slider_Play.setUP_Slider.connect(self.Set_Position)

        # Slider Volume
        self.Slider_Volume.setRange(0, 0)
        self.Slider_Volume.sliderMoved.connect(self.Set_volume)

        # label_Time

        # Tool Bar
        self.actionOpen.triggered.connect(self.Load_video)

        # Search
        self.sch_listWidget.itemDoubleClicked.connect(self.item_Event)
        self.search_lineEdit.textChanged.connect(self.search_Tag)

        # self.lineEdit_GoTo.textChanged.connect(self.GoTO)

    def start(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.pushButton_Start.setEnabled(True)
            self.pushButton_Start.setIcon(QIcon('./Icons/pause.png'))
        else:
            self.player.play()
            self.pushButton_Start.setEnabled(True)
            self.pushButton_Start.setIcon(QIcon('./Icons/play.png'))

    def stop(self):
        self.player.stop()
        self.pushButton_next.setEnabled(False)
        self.pushButton_previous.setEnabled(False)
        self.pushButton_volume.setEnabled(False)
        self.pushButton_Start.setEnabled(False)
        self.pushButton_stop.setEnabled(False)

    def next(self):
        self.FileName = self.Files[self.Files.index(self.FileName)+1]
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(
            os.path.join(self.File_Path, self.FileName))))
        self.setWindowTitle(f" Media Player - {self.FileName}")
        self.start()
        if self.FileName == self.Files[-1]:
            self.pushButton_next.setEnabled(False)
        else:
            self.pushButton_previous.setEnabled(True)

    def previous(self):
        self.FileName = self.Files[self.Files.index(self.FileName)-1]
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(
            os.path.join(self.File_Path, self.FileName))))
        self.setWindowTitle(f" Media Player - {self.FileName}")
        self.start()
        if self.FileName == self.Files[0]:
            self.pushButton_previous.setEnabled(False)
        else:
            self.pushButton_next.setEnabled(True)

    def Load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open video", directory=os.path.join(os.getcwd(), 'Video'))
        path_Element = file_path.split("/")
        movie_Name = path_Element.pop()
        Tag_path = "/".join(path_Element) + "/Tags/" + movie_Name.split(".")[0]
        self.Create_Tags(Tag_path)

        if file_path:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.start()
            self.pushButton_volume.setEnabled(True)
            self.pushButton_volume.setIcon(QIcon('./Icons/unmute.png'))

            self.pushButton_stop.setEnabled(True)
            self.Slider_Volume.setRange(0, self.player.volume())
            self.Slider_Volume.setValue(80)
            self.FileName = file_path.split("/")[-1]
            # self.player.setObjectName(self.FileName)
            self.setWindowTitle(f" Media Player - {self.FileName}")
            self.File_Path = file_path.replace(f"/{self.FileName}", "")
            self.Files = os.listdir(self.File_Path)
            if not self.FileName == self.Files[0]:
                self.pushButton_previous.setEnabled(True)
            if not self.FileName == self.Files[-1]:
                self.pushButton_next.setEnabled(True)

    def Position_changed(self, position):
        hour = position//(1000*3600)
        minute = (position % (1000*3600))//(60*1000)
        second = ((position % (1000*3600)) % (60*1000))//1000

        self.label_Time.setText(f'{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}')
        self.Slider_Play.setValue(position)

    def Duration_changed(self, duration):
        self.Duration = duration
        self.Slider_Play.setRange(0, duration)

    def Set_Position(self, position):

        if not (position < 0 and position > self.Slider_Play.width()):
            position = int(self.Duration * (position / self.Slider_Play.width()))
            self.Slider_Play.setValue(position)

        self.player.setPosition(position)

    # def Volume_changed(self, volume):
    #     self.Slider_Volume.setValue(volume)

    def Set_volume(self, volume):
        if not volume:
            self.player.setMuted(True)
            self.pushButton_volume.setIcon(QIcon('./Icons/mute.png'))
        else:
            self.player.setMuted(False)
            self.pushButton_volume.setIcon(QIcon('./Icons/unmute.png'))
        self.player.setVolume(volume)

    def volumeOnOff(self):
        if self.player.isMuted():
            self.player.setMuted(False)
            self.pushButton_volume.setIcon(QIcon('./Icons/unmute.png'))
        else:
            self.player.setMuted(True)
            self.pushButton_volume.setIcon(QIcon('./Icons/mute.png'))

    def sch_icon_Event(self, type):

        # create QLineEdit
        self.search_lineEdit.resize(
            int((200 / 800) * self.size().width()), self.pushButton_Search.geometry().height()-2)
        self.search_lineEdit.move(
            int(self.pushButton_Search.x() - (200 / 800) * self.size().width()), 31)
        self.search_lineEdit.setVisible(True)

    def MainWindow_Event(self, type):

        self.search_lineEdit.setText("")
        self.search_lineEdit.setVisible(False)

        self.sch_listWidget.setVisible(False)
        self.sch_listWidget.clear()

    def main_size_Change(self, val):

        self.sch_listWidget.resize(
            int((200 / 800) * self.size().width()), int((200 / 600) * self.size().height()))
        self.sch_listWidget.move(
            int(self.pushButton_Search.x() - (200 / 800) * self.size().width()), 52)

        self.search_lineEdit.resize(
            int((200 / 800) * self.size().width()), self.pushButton_Search.geometry().height()-2)
        self.search_lineEdit.move(
            int(self.pushButton_Search.x() - (200 / 800) * self.size().width()), 31)

    def item_Event(self, item):
        print(item.text())

    def search_Tag(self, val):

        # create QListWidget
        self.sch_listWidget.resize(
            int((200 / 800) * self.size().width()), int((200 / 600) * self.size().height()))
        self.sch_listWidget.move(
            int(self.pushButton_Search.x() - (200 / 800) * self.size().width()), 52)
        self.sch_listWidget.setVisible(True)

        # start search thread
        self.search_Thread = search_thread(self, val)
        self.search_Thread.update_schTag.connect(self.update_Tags)
        self.search_Thread.start()

    def update_Tags(self, tagsList):
        self.sch_listWidget.clear()

        for key in tagsList:
            self.sch_listWidget.addItem(key)

        self.search_Thread = None

    def GoTO(self, time):
        self.Slider_Play.setValue(int(time)*1000)
        self.player.setPosition(int(time)*1000)

    def Create_Tags(self, directory):
        self.TagDB = Tag.tag("SearchPart/1")

        




# Custome play slider
class Slider(QSlider):
    setUP_Slider = QtCore.pyqtSignal(int)
    def __init__(self, MediaPlayer):
        QSlider.__init__(self, parent= MediaPlayer)

    def mousePressEvent(self, position):
        self.setUP_Slider.emit(position.pos().x())

    def mouseMoveEvent(self, position):
        self.setUP_Slider.emit(position.x())




# thread for searching in tags
class search_thread(QtCore.QThread):
    update_schTag = QtCore.pyqtSignal(list)

    def __init__(self, window, val):
        self.val = val
        self.Parent = window
        QtCore.QThread.__init__(self, parent=window)

    def run(self):
        if self.Parent.TagDB:
            sch_Tags = self.Parent.TagDB.find_Closest_to(self.val)
            self.update_schTag.emit(sch_Tags)
        else :
            self.update_schTag.emit([])



if __name__ == '__main__':
    app = QApplication(sys.argv)
    Loginw = Login.LoginWindow()
    Loginw.show()
    app.exec_()
    if Loginw.Login():
        # app=QApplication(sys.argv)
        # self.TagDB = Tag.tag("SearchPart/1")
        Mainw = MediaPlayer()
        Mainw.show()
        sys.exit(app.exec_())
