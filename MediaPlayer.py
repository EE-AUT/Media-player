import sys
import os
import LoginPart.Login as Login
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QFileDialog
from PyQt5 import uic, QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaMetaData
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

        self.setWindowTitle("Media Player")

        # PushButtton
        self.pushButton_Start.setEnabled(False)
        self.pushButton_Start.clicked.connect(self.start)
        self.pushButton_volume.clicked.connect(self.volumeOnOff)

        # Slider Play
        self.Slider_Play.setRange(0, 0)
        self.player.positionChanged.connect(self.Position_changed)
        self.player.durationChanged.connect(self.Duration_changed)
        self.Slider_Play.sliderMoved.connect(self.Set_Position)

        # Slider Volume
        self.Slider_Volume.setRange(0, 0)
        # self.player.volumeChanged.connect(self.Volume_changed)
        self.Slider_Volume.sliderMoved.connect(self.Set_volume)

        # Label
        self.label_Name.setText("Welcome Dear")
        self.label_Name.setStyleSheet("background:#00aaff")

        # Tool Bar
        self.actionOpen.triggered.connect(self.Load_video)

    def start(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.pushButton_Start.setEnabled(True)
            self.pushButton_Start.setIcon(QIcon('./Icons/pause.png'))
        else:
            self.player.play()
            self.pushButton_Start.setEnabled(True)
            self.pushButton_Start.setIcon(QIcon('./Icons/play.png'))

    def Load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open video", directory=os.path.join(os.getcwd(), 'Video'))
        if file_path:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.start()
            self.Slider_Volume.setRange(0, self.player.volume())
            self.Slider_Volume.setValue(100)


    def Position_changed(self, position):
        self.Slider_Play.setValue(position)

    def Duration_changed(self, duration):
        self.Slider_Play.setRange(0, duration)

    def Set_Position(self, position):
        self.player.setPosition(position)

    # def Volume_changed(self, volume):
    #     self.Slider_Volume.setValue(volume)

    def Set_volume(self, volume):
        if not volume:
            self.player.setMuted(True)
            self.pushButton_volume.setIcon(QIcon('./Icons/sound off.png'))
        else:
            self.player.setMuted(False)
            self.pushButton_volume.setIcon(QIcon('./Icons/sound on.png'))
        self.player.setVolume(volume)
    
    def volumeOnOff(self):
        if self.player.isMuted():
            self.player.setMuted(False)
            self.pushButton_volume.setIcon(QIcon('./Icons/sound on.png'))
        else:
            self.player.setMuted(True)
            self.pushButton_volume.setIcon(QIcon('./Icons/sound off.png'))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    Loginw = Login.LoginWindow()
    Loginw.show()
    app.exec_()
    if Loginw.Login():
        # app=QApplication(sys.argv)
        Mainw = MediaPlayer()
        Mainw.show()
        sys.exit(app.exec_())
