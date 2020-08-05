from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QMainWindow, QLabel, QFrame
from PyQt5 import QtCore


def MousePosition(MediaPlayer, position):
    if position.y() > QApplication.desktop().screenGeometry().height()-50 or position.y() < 50:  # The cursor is up or down
        Set_visible(MediaPlayer, True)
    else:  # The cursor is in the middle
        Set_visible(MediaPlayer, False)


def fullscreen(MediaPlayer):
    if MediaPlayer.firstTime_fullscreen:#For first time must be craete some labels to fill gaps and frame
        MediaPlayer.Label_temp1 = QLabel("", MediaPlayer)
        MediaPlayer.Label_temp2 = QLabel("", MediaPlayer)
        MediaPlayer.Label_temp3 = QLabel("", MediaPlayer)
        MediaPlayer.Label_temp4 = QLabel("", parent=MediaPlayer)
        MediaPlayer.Label_temp5 = QLabel("", parent=MediaPlayer)
        MediaPlayer.Label_temp7 = QLabel("", parent=MediaPlayer)
        MediaPlayer.frame = QFrame(parent=MediaPlayer)
        MediaPlayer.lay = QHBoxLayout()
        MediaPlayer.frame.setLayout(MediaPlayer.lay)

        MediaPlayer.firstTime_fullscreen = False

    Set_visible(MediaPlayer, MediaPlayer.isFullScreen())
    MediaPlayer.menubar.setVisible(MediaPlayer.isFullScreen())
    if not MediaPlayer.isFullScreen():
        Remove_from_layout(MediaPlayer)
        MediaPlayer.showFullScreen()

    else:
        Add_to_layout(MediaPlayer)
        MediaPlayer.showNormal()


def Remove_from_layout(MediaPlayer):
    ###To remove everything from their layout
    screenWidth = QApplication.desktop().screenGeometry().width()
    screenHeight = QApplication.desktop().screenGeometry().height()
    # Remove widget of video from its layout and resize , move it
    MediaPlayer.verticalLayout.removeWidget(MediaPlayer.videowidget)
    MediaPlayer.videowidget.resize(screenWidth, screenHeight)
    MediaPlayer.videowidget.move(0, 0)

    # Remove Slider and Time_Label and Duration_label from their layout and resize , move it
    MediaPlayer.horizontalLayout_4.removeWidget(MediaPlayer.label_Duration)
    MediaPlayer.horizontalLayout_4.removeWidget(MediaPlayer.Slider_Play)
    MediaPlayer.horizontalLayout_4.removeWidget(MediaPlayer.label_Time)

    MediaPlayer.Label_temp4.move(0, screenHeight-50)
    MediaPlayer.Label_temp4.resize(15, 20)

    MediaPlayer.label_Time.move(15, screenHeight-50)
    MediaPlayer.label_Time.resize(70, 20)

    MediaPlayer.Slider_Play.move(85, screenHeight-50)
    MediaPlayer.Slider_Play.resize(screenWidth-170, 20)
    MediaPlayer.Label_temp5.move(screenWidth-85, screenHeight-50)
    MediaPlayer.Label_temp5.resize(15, 20)

    MediaPlayer.label_Duration.move(screenWidth-70, screenHeight-50)
    MediaPlayer.label_Duration.resize(70, 20)

    # Remove some pushButton from their layout and resize , move it
    MediaPlayer.horizontalLayout.removeWidget(MediaPlayer.pushButton_Start)
    MediaPlayer.horizontalLayout.removeWidget(MediaPlayer.pushButton_stop)
    MediaPlayer.horizontalLayout.removeWidget(MediaPlayer.pushButton_next)
    MediaPlayer.horizontalLayout.removeWidget(MediaPlayer.pushButton_previous)
    MediaPlayer.horizontalLayout.removeWidget(MediaPlayer.pushButton_open)

    MediaPlayer.pushButton_Start.move(screenWidth/2-15, screenHeight-30)
    MediaPlayer.pushButton_stop.move(screenWidth/2+45, screenHeight-30)
    MediaPlayer.pushButton_next.move(screenWidth/2+15, screenHeight-30)
    MediaPlayer.pushButton_previous.move(screenWidth/2-45, screenHeight-30)
    MediaPlayer.pushButton_open.move(screenWidth/2-75, screenHeight-30)

    # Remove some pushButton and volume_Slider from their layout and resize , move it
    MediaPlayer.horizontalLayout_5.removeWidget(MediaPlayer.pushButton_Setting)
    MediaPlayer.horizontalLayout_5.removeWidget(
        MediaPlayer.pushButton_Playlist)
    MediaPlayer.horizontalLayout_5.removeWidget(
        MediaPlayer.pushButton_Tag_of_file)
    MediaPlayer.horizontalLayout_3.removeWidget(MediaPlayer.pushButton_volume)
    MediaPlayer.horizontalLayout_3.removeWidget(MediaPlayer.Slider_Volume)

    MediaPlayer.pushButton_Setting.move(0, screenHeight-30)
    MediaPlayer.pushButton_Playlist.move(30, screenHeight-30)
    MediaPlayer.pushButton_Tag_of_file.move(screenWidth-158, screenHeight-30)
    MediaPlayer.pushButton_volume.move(screenWidth-129, screenHeight-30)
    MediaPlayer.Slider_Volume.move(screenWidth-100, screenHeight-30)
    MediaPlayer.Slider_Volume.resize(85, 30)
    MediaPlayer.Label_temp7.move(screenWidth-15, screenHeight-30)
    MediaPlayer.Label_temp7.resize(15, 30)

    # Move and resize temporary Label to fill gaps
    MediaPlayer.Label_temp1.move(60, screenHeight-30)
    MediaPlayer.Label_temp1.resize(screenWidth/2-75-60, 30)

    MediaPlayer.Label_temp2.move(screenWidth/2+75, screenHeight-30)
    MediaPlayer.Label_temp2.resize(screenWidth-158-screenWidth/2-75, 30)
    # Remove search and Bookmark pushButton from their layout 
    MediaPlayer.horizontalLayout_6.removeWidget(MediaPlayer.pushButton_Search)
    MediaPlayer.horizontalLayout_6.removeWidget(MediaPlayer.search_lineEdit)
    MediaPlayer.horizontalLayout_2.removeWidget(
        MediaPlayer.pushButton_BookMark)
    MediaPlayer.horizontalLayout_2.removeWidget(MediaPlayer.lineEdit_Bookmark)

    # Add search and Bookmark pushButton to the layout and add this layout to frame
    MediaPlayer.lay.addWidget(MediaPlayer.pushButton_BookMark, 0)
    MediaPlayer.lay.addWidget(MediaPlayer.lineEdit_Bookmark, 1)
    MediaPlayer.lay.addWidget(MediaPlayer.Label_temp3, 1)

    MediaPlayer.lay.addWidget(MediaPlayer.search_lineEdit, 2)
    MediaPlayer.lay.addWidget(MediaPlayer.pushButton_Search, 3)
    MediaPlayer.frame.resize(screenWidth, 35)

    MediaPlayer.frame.move(0, 0)


def Add_to_layout(MediaPlayer):
    ###To Add everything To their layout
    MediaPlayer.horizontalLayout_5.removeItem(MediaPlayer.horizontalLayout)
    MediaPlayer.horizontalLayout_5.removeItem(MediaPlayer.horizontalLayout_3)
    MediaPlayer.verticalLayout.addWidget(MediaPlayer.videowidget)
    MediaPlayer.verticalLayout.removeItem(MediaPlayer.horizontalLayout_4)
    MediaPlayer.verticalLayout.addLayout(MediaPlayer.horizontalLayout_4)
    MediaPlayer.horizontalLayout_4.addWidget(MediaPlayer.label_Time)
    MediaPlayer.horizontalLayout_4.addWidget(MediaPlayer.Slider_Play)
    MediaPlayer.horizontalLayout_4.addWidget(MediaPlayer.label_Duration)
    MediaPlayer.horizontalLayout_5.addWidget(MediaPlayer.pushButton_Setting)
    MediaPlayer.horizontalLayout_5.addWidget(
        MediaPlayer.pushButton_Playlist, 12, alignment=QtCore.Qt.AlignLeft)

    MediaPlayer.horizontalLayout.addWidget(MediaPlayer.pushButton_open)
    MediaPlayer.horizontalLayout.addWidget(MediaPlayer.pushButton_previous)
    MediaPlayer.horizontalLayout.addWidget(MediaPlayer.pushButton_Start)
    MediaPlayer.horizontalLayout.addWidget(MediaPlayer.pushButton_next)
    MediaPlayer.horizontalLayout.addWidget(MediaPlayer.pushButton_stop)

    MediaPlayer.horizontalLayout_5.addLayout(MediaPlayer.horizontalLayout)

    MediaPlayer.horizontalLayout_5.addWidget(
        MediaPlayer.pushButton_Tag_of_file, 15, QtCore.Qt.AlignRight)
    MediaPlayer.horizontalLayout_3.addWidget(MediaPlayer.pushButton_volume)
    MediaPlayer.horizontalLayout_3.addWidget(MediaPlayer.Slider_Volume)
    MediaPlayer.horizontalLayout_5.addLayout(MediaPlayer.horizontalLayout_3)

    MediaPlayer.lay.removeWidget(MediaPlayer.pushButton_Search)
    MediaPlayer.lay.removeWidget(MediaPlayer.pushButton_BookMark)
    MediaPlayer.lay.removeWidget(MediaPlayer.lineEdit_Bookmark)
    MediaPlayer.lay.removeWidget(MediaPlayer.search_lineEdit)

    MediaPlayer.horizontalLayout_2.addWidget(MediaPlayer.pushButton_BookMark)
    MediaPlayer.horizontalLayout_2.addWidget(MediaPlayer.lineEdit_Bookmark)

    MediaPlayer.horizontalLayout_6.addWidget(MediaPlayer.search_lineEdit)
    MediaPlayer.horizontalLayout_6.addWidget(MediaPlayer.pushButton_Search)
    #Temporary label and frame must be hide when mainwindow is in Normal screen
    MediaPlayer.frame.setVisible(False)
    MediaPlayer.Label_temp1.setVisible(False)
    MediaPlayer.Label_temp2.setVisible(False)
    MediaPlayer.Label_temp4.setVisible(False)
    MediaPlayer.Label_temp5.setVisible(False)
    MediaPlayer.Label_temp7.setVisible(False)


def Set_visible(MediaPlayer, Bool):
    # To SetVisible all widget True or False
    MediaPlayer.Label_temp1.setVisible(Bool)
    MediaPlayer.Label_temp2.setVisible(Bool)
    MediaPlayer.Label_temp4.setVisible(Bool)
    MediaPlayer.Label_temp5.setVisible(Bool)
    MediaPlayer.Label_temp7.setVisible(Bool)
    MediaPlayer.Slider_Play.setVisible(Bool)
    MediaPlayer.label_Time.setVisible(Bool)
    MediaPlayer.label_Duration.setVisible(Bool)
    MediaPlayer.pushButton_stop.setVisible(Bool)
    MediaPlayer.pushButton_previous.setVisible(Bool)
    MediaPlayer.pushButton_open.setVisible(Bool)
    MediaPlayer.pushButton_next.setVisible(Bool)
    MediaPlayer.pushButton_Setting.setVisible(Bool)
    MediaPlayer.pushButton_volume.setVisible(Bool)
    MediaPlayer.Slider_Volume.setVisible(Bool)
    MediaPlayer.pushButton_Playlist.setVisible(Bool)
    MediaPlayer.pushButton_Tag_of_file.setVisible(Bool)
    MediaPlayer.pushButton_Search.setVisible(Bool)
    MediaPlayer.pushButton_BookMark.setVisible(Bool)
    MediaPlayer.frame.setVisible(Bool)
    MediaPlayer.pushButton_Start.setVisible(Bool)#For focuse Start button must be last
