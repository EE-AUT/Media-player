from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic, QtCore, QtGui
import os
import csv

Form = uic.loadUiType(os.path.join(os.getcwd(), 'SettingPart/Setting.ui'))[0]


class SettingWindow(QMainWindow, Form, QtCore.QThread):
    def __init__(self, Mediaplayer):
        QMainWindow.__init__(self)
        Form.__init__(self)
        QtCore.QThread.__init__(self, parent=Mediaplayer)
        self.setupUi(self)
        self.MediaPlayer = Mediaplayer

        # Theme Part
        self.palette = QtGui.QPalette()
        self.pushButton_Cancel.clicked.connect(self.Exit)
        self.pushButton_OK.clicked.connect(self.saveANDexit)
        self.comboBox_Theme.activated.connect(self._Theme)
        self.scrollArea_Theme.setVisible(False)

        # Play Back Part
        self.horizontalSlider_Speed.setRange(0, 300)
        self.horizontalSlider_Speed.setValue(100)
        self.lineEdit_Speed.setText("1.00")
        self.label_Error_Range.setVisible(False)
        self.label_Error_Number.setVisible(False)

        self.horizontalSlider_Speed.valueChanged.connect(self.Play_Back_Slider)
        self.lineEdit_Speed.textChanged.connect(self.Play_Back_LineEdit)

        # Text Part
        self.comboBox_Font.activated.connect(self.Font_Change)


    def Font_Change(self, val):
        print(val)
        # if int(val)==0:
        #     print(self.font())
        #     self.setFont(QtGui.QFont('Arial',2))
        #     self.MediaPlayer.setFont(QtGui.QFont('Arial',2))
        #     self.Tab.setFont(QtGui.QFont('Arial',2))
        #     self.MediaPlayer.actionFullScreen.setFont(QtGui.QFont('Arial',2))

    def Play_Back_LineEdit(self, val):
        try:
            if val:
                if float(val):
                    self.label_Error_Number.setVisible(False)

                    if float(val) >= 0 and float(val) <= 3:
                        self.label_Error_Range.setVisible(False)
                        self.horizontalSlider_Speed.setValue(float(val)*100)
                        if self.MediaPlayer.player.isAvailable():
                            self.MediaPlayer.player.setPlaybackRate(float(val))
                    else:
                        self.label_Error_Range.setVisible(True)

        except:
            self.label_Error_Number.setVisible(True)

    def Play_Back_Slider(self, val):
        self.lineEdit_Speed.setText(str(val/100))

    def Exit(self):
        self.Theme_apply()
        self.close()

    def saveANDexit(self):
        # To Write everything about Setting in Sitting.csv
        with open('SettingPart/Setting.csv', mode='w', newline='') as file:
            Setting_writer = csv.writer(file)
            Setting_writer.writerow(
                ['Theme'] + [self.comboBox_Theme.currentIndex()])
            Setting_writer.writerow(
                ['Classic'] + [int(self.checkBox_Theme.isChecked())])
            Setting_writer.writerow(
                ['Background'] + [self.comboBox_Background.currentIndex()])
            Setting_writer.writerow(
                ['Base'] + [self.comboBox_Base.currentIndex()])
            Setting_writer.writerow(
                ['WindowText'] + [self.comboBox_WindowsText.currentIndex()])
            Setting_writer.writerow(
                ['Text'] + [self.comboBox_Text.currentIndex()])
            Setting_writer.writerow(
                ['Button'] + [self.comboBox_Button.currentIndex()])
            Setting_writer.writerow(
                ['ButtonText'] + [self.comboBox_ButtonText.currentIndex()])
            Setting_writer.writerow(
                ['Slider Color'] + [self.comboBox_Slider.currentIndex()])
            # Setting_writer.writerow(
            #     ['Slider Size'] + [self.spinBox_Slider.value()])

        self.Theme_apply()
        self.close()

    def _Theme(self, index):
        if index == 0:
            self.Classic_Theme(False)
            self.checkBox_Theme.setChecked(False)

            self.background_Theme(1)
            self.comboBox_Background.setCurrentIndex(1)

            self.Base_Theme(0)
            self.comboBox_Base.setCurrentIndex(0)

            self.WindowsText_Theme(2)
            self.comboBox_WindowsText.setCurrentIndex(2)

            self.Text_Theme(2)
            self.comboBox_Text.setCurrentIndex(2)

            self.Button_Theme(0)
            self.comboBox_Button.setCurrentIndex(0)

            self.ButtonText_Theme(2)
            self.comboBox_ButtonText.setCurrentIndex(2)

            self.SliderTheme(3)
            self.comboBox_Slider.setCurrentIndex(3)

            # self.Slider_Size_Changed(int(Dict['Slider Size']))
            # self.spinBox_Slider.setValue(int(Dict['Slider Size']))

            self.palette.setColor(QtGui.QPalette.Highlight,
                                  QtGui.QColor('#2c88f7'))
            self.palette.setColor(
                QtGui.QPalette.HighlightedText, QtCore.Qt.black)
            QApplication.setPalette(self.palette)
            self.scrollArea_Theme.setVisible(False)

        if index == 1:
            self.Classic_Theme(False)
            self.checkBox_Theme.setChecked(False)

            self.background_Theme(11)
            self.comboBox_Background.setCurrentIndex(11)

            self.Base_Theme(2)
            self.comboBox_Base.setCurrentIndex(2)

            self.WindowsText_Theme(0)
            self.comboBox_WindowsText.setCurrentIndex(0)

            self.Text_Theme(0)
            self.comboBox_Text.setCurrentIndex(0)

            self.Button_Theme(11)
            self.comboBox_Button.setCurrentIndex(11)

            self.ButtonText_Theme(0)
            self.comboBox_ButtonText.setCurrentIndex(0)

            self.SliderTheme(5)
            self.comboBox_Slider.setCurrentIndex(5)

            # self.Slider_Size_Changed(int(Dict['Slider Size']))
            # self.spinBox_Slider.setValue(int(Dict['Slider Size']))
            self.palette.setColor(QtGui.QPalette.Highlight,
                                  QtGui.QColor('#cb90ff'))
            self.palette.setColor(
                QtGui.QPalette.HighlightedText, QtCore.Qt.black)
            QApplication.setPalette(self.palette)
            self.scrollArea_Theme.setVisible(False)
        if index == 2:
            self._Theme(1)
            self.Classic_Theme(True)
            self.checkBox_Theme.setChecked(True)
            self.SliderTheme(5)

        if index == 3:
            self._Theme(0)
            self.Classic_Theme(True)
            self.checkBox_Theme.setChecked(True)
            self.SliderTheme(3)

        if index == 4:

            self.scrollArea_Theme.setVisible(True)

            # To Connect Signals of custom Theme
            self.checkBox_Theme.stateChanged.connect(self.Classic_Theme)
            self.comboBox_Background.activated.connect(self.background_Theme)
            self.comboBox_Base.activated.connect(self.Base_Theme)
            self.comboBox_WindowsText.activated.connect(self.WindowsText_Theme)
            self.comboBox_Text.activated.connect(self.Text_Theme)
            self.comboBox_Button.activated.connect(self.Button_Theme)
            self.comboBox_ButtonText.activated.connect(self.ButtonText_Theme)
            self.comboBox_Slider.activated.connect(self.SliderTheme)

            # self.spinBox_Slider.setRange(0, 10)
            # self.spinBox_Slider.valueChanged.connect(self.Slider_Size_Changed)

    def Classic_Theme(self, classic):
        if classic:
            QApplication.setStyle("Windows")
        else:
            QApplication.setStyle("Fusion")

    def background_Theme(self, index):
        if index == 0:
            self.palette.setColor(QtGui.QPalette.Window,
                                  QtGui.QColor('#ffffff'))
            QApplication.setPalette(self.palette)
        if index == 1:
            self.palette.setColor(QtGui.QPalette.Window,
                                  QtGui.QColor('#ebebeb'))
            QApplication.setPalette(self.palette)
        if index == 2:
            self.palette.setColor(QtGui.QPalette.Window,
                                  QtGui.QColor(53, 53, 53))
            QApplication.setPalette(self.palette)
        if index == 3:
            self.palette.setColor(QtGui.QPalette.Window,
                                  QtGui.QColor('#35b9ff'))
            QApplication.setPalette(self.palette)
        if index == 4:
            self.palette.setColor(QtGui.QPalette.Window,
                                  QtGui.QColor('#163393'))
            QApplication.setPalette(self.palette)
        if index == 5:
            self.palette.setColor(QtGui.QPalette.Window,
                                  QtGui.QColor('#ee8bff'))
            QApplication.setPalette(self.palette)
        if index == 6:
            self.palette.setColor(QtGui.QPalette.Window,
                                  QtGui.QColor('#9538bd'))
            QApplication.setPalette(self.palette)
        if index == 7:
            self.palette.setColor(QtGui.QPalette.Window,
                                  QtGui.QColor('#55aa00'))
            QApplication.setPalette(self.palette)
        if index == 8:
            self.palette.setColor(QtGui.QPalette.Window,
                                  QtGui.QColor('#ffff7f'))
            QApplication.setPalette(self.palette)
        if index == 9:
            self.palette.setColor(QtGui.QPalette.Window,
                                  QtGui.QColor('#ff0000'))
            QApplication.setPalette(self.palette)
        if index == 10:
            self.palette.setColor(QtGui.QPalette.Window,
                                  QtGui.QColor('#ffaa00'))
        if index == 11:
            self.palette.setColor(QtGui.QPalette.Window,
                                  QtGui.QColor('#353535'))
        QApplication.setPalette(self.palette)

    ##########################
    def Base_Theme(self, index):
        if index == 0:
            self.palette.setColor(QtGui.QPalette.Base,
                                  QtGui.QColor('#ffffff'))
            QApplication.setPalette(self.palette)
        if index == 1:
            self.palette.setColor(QtGui.QPalette.Base,
                                  QtGui.QColor('#ebebeb'))
            QApplication.setPalette(self.palette)
        if index == 2:
            self.palette.setColor(QtGui.QPalette.Base,
                                  QtGui.QColor(53, 53, 53))
            QApplication.setPalette(self.palette)
        if index == 3:
            self.palette.setColor(QtGui.QPalette.Base,
                                  QtGui.QColor('#35b9ff'))
            QApplication.setPalette(self.palette)
        if index == 4:
            self.palette.setColor(QtGui.QPalette.Base,
                                  QtGui.QColor('#163393'))
            QApplication.setPalette(self.palette)
        if index == 5:
            self.palette.setColor(QtGui.QPalette.Base,
                                  QtGui.QColor('#ee8bff'))
            QApplication.setPalette(self.palette)
        if index == 6:
            self.palette.setColor(QtGui.QPalette.Base,
                                  QtGui.QColor('#9538bd'))
            QApplication.setPalette(self.palette)
        if index == 7:
            self.palette.setColor(QtGui.QPalette.Base,
                                  QtGui.QColor('#55aa00'))
            QApplication.setPalette(self.palette)
        if index == 8:
            self.palette.setColor(QtGui.QPalette.Base,
                                  QtGui.QColor('#ffff7f'))
            QApplication.setPalette(self.palette)
        if index == 9:
            self.palette.setColor(QtGui.QPalette.Base,
                                  QtGui.QColor('#ff0000'))
            QApplication.setPalette(self.palette)
        if index == 10:
            self.palette.setColor(QtGui.QPalette.Base,
                                  QtGui.QColor('#ffaa00'))
        if index == 11:
            self.palette.setColor(QtGui.QPalette.Base,
                                  QtGui.QColor('#353535'))
        QApplication.setPalette(self.palette)

    ###################
    def WindowsText_Theme(self, index):
        if index == 0:
            self.palette.setColor(QtGui.QPalette.WindowText,
                                  QtGui.QColor('#ffffff'))
            QApplication.setPalette(self.palette)
        if index == 1:
            self.palette.setColor(QtGui.QPalette.WindowText,
                                  QtGui.QColor('#ebebeb'))
            QApplication.setPalette(self.palette)
        if index == 2:
            self.palette.setColor(QtGui.QPalette.WindowText,
                                  QtGui.QColor(53, 53, 53))
            QApplication.setPalette(self.palette)
        if index == 3:
            self.palette.setColor(QtGui.QPalette.WindowText,
                                  QtGui.QColor('#35b9ff'))
            QApplication.setPalette(self.palette)
        if index == 4:
            self.palette.setColor(QtGui.QPalette.WindowText,
                                  QtGui.QColor('#163393'))
            QApplication.setPalette(self.palette)
        if index == 5:
            self.palette.setColor(QtGui.QPalette.WindowText,
                                  QtGui.QColor('#ee8bff'))
            QApplication.setPalette(self.palette)
        if index == 6:
            self.palette.setColor(QtGui.QPalette.WindowText,
                                  QtGui.QColor('#9538bd'))
            QApplication.setPalette(self.palette)
        if index == 7:
            self.palette.setColor(QtGui.QPalette.WindowText,
                                  QtGui.QColor('#55aa00'))
            QApplication.setPalette(self.palette)
        if index == 8:
            self.palette.setColor(QtGui.QPalette.WindowText,
                                  QtGui.QColor('#ffff7f'))
            QApplication.setPalette(self.palette)
        if index == 9:
            self.palette.setColor(QtGui.QPalette.WindowText,
                                  QtGui.QColor('#ff0000'))
            QApplication.setPalette(self.palette)
        if index == 10:
            self.palette.setColor(QtGui.QPalette.WindowText,
                                  QtGui.QColor('#ffaa00'))
        if index == 11:
            self.palette.setColor(QtGui.QPalette.WindowText,
                                  QtGui.QColor('#353535'))
        QApplication.setPalette(self.palette)

    #############################

    def Text_Theme(self, index):
        if index == 0:
            self.palette.setColor(QtGui.QPalette.Text,
                                  QtGui.QColor('#ffffff'))
            QApplication.setPalette(self.palette)
        if index == 1:
            self.palette.setColor(QtGui.QPalette.Text,
                                  QtGui.QColor('#ebebeb'))
            QApplication.setPalette(self.palette)
        if index == 2:
            self.palette.setColor(QtGui.QPalette.Text,
                                  QtGui.QColor(53, 53, 53))
            QApplication.setPalette(self.palette)
        if index == 3:
            self.palette.setColor(QtGui.QPalette.Text,
                                  QtGui.QColor('#35b9ff'))
            QApplication.setPalette(self.palette)
        if index == 4:
            self.palette.setColor(QtGui.QPalette.Text,
                                  QtGui.QColor('#163393'))
            QApplication.setPalette(self.palette)
        if index == 5:
            self.palette.setColor(QtGui.QPalette.Text,
                                  QtGui.QColor('#ee8bff'))
            QApplication.setPalette(self.palette)
        if index == 6:
            self.palette.setColor(QtGui.QPalette.Text,
                                  QtGui.QColor('#9538bd'))
            QApplication.setPalette(self.palette)
        if index == 7:
            self.palette.setColor(QtGui.QPalette.Text,
                                  QtGui.QColor('#55aa00'))
            QApplication.setPalette(self.palette)
        if index == 8:
            self.palette.setColor(QtGui.QPalette.Text,
                                  QtGui.QColor('#ffff7f'))
            QApplication.setPalette(self.palette)
        if index == 9:
            self.palette.setColor(QtGui.QPalette.Text,
                                  QtGui.QColor('#ff0000'))
            QApplication.setPalette(self.palette)
        if index == 10:
            self.palette.setColor(QtGui.QPalette.Text,
                                  QtGui.QColor('#ffaa00'))
        if index == 11:
            self.palette.setColor(QtGui.QPalette.Text,
                                  QtGui.QColor('#353535'))
        QApplication.setPalette(self.palette)

    ###############################
    def Button_Theme(self, index):
        if index == 0:
            self.palette.setColor(QtGui.QPalette.Button,
                                  QtGui.QColor('#ffffff'))
            QApplication.setPalette(self.palette)
        if index == 1:
            self.palette.setColor(QtGui.QPalette.Button,
                                  QtGui.QColor('#ebebeb'))
            QApplication.setPalette(self.palette)
        if index == 2:
            self.palette.setColor(QtGui.QPalette.Button,
                                  QtGui.QColor(53, 53, 53))
            QApplication.setPalette(self.palette)
        if index == 3:
            self.palette.setColor(QtGui.QPalette.Button,
                                  QtGui.QColor('#35b9ff'))
            QApplication.setPalette(self.palette)
        if index == 4:
            self.palette.setColor(QtGui.QPalette.Button,
                                  QtGui.QColor('#163393'))
            QApplication.setPalette(self.palette)
        if index == 5:
            self.palette.setColor(QtGui.QPalette.Button,
                                  QtGui.QColor('#ee8bff'))
            QApplication.setPalette(self.palette)
        if index == 6:
            self.palette.setColor(QtGui.QPalette.Button,
                                  QtGui.QColor('#9538bd'))
            QApplication.setPalette(self.palette)
        if index == 7:
            self.palette.setColor(QtGui.QPalette.Button,
                                  QtGui.QColor('#55aa00'))
            QApplication.setPalette(self.palette)
        if index == 8:
            self.palette.setColor(QtGui.QPalette.Button,
                                  QtGui.QColor('#ffff7f'))
            QApplication.setPalette(self.palette)
        if index == 9:
            self.palette.setColor(QtGui.QPalette.Button,
                                  QtGui.QColor('#ff0000'))
            QApplication.setPalette(self.palette)
        if index == 10:
            self.palette.setColor(QtGui.QPalette.Button,
                                  QtGui.QColor('#ffaa00'))
        if index == 11:
            self.palette.setColor(QtGui.QPalette.Button,
                                  QtGui.QColor('#353535'))
        QApplication.setPalette(self.palette)

    ###############################
    def ButtonText_Theme(self, index):
        if index == 0:
            self.palette.setColor(QtGui.QPalette.ButtonText,
                                  QtGui.QColor('#ffffff'))
            QApplication.setPalette(self.palette)
        if index == 1:
            self.palette.setColor(QtGui.QPalette.ButtonText,
                                  QtGui.QColor('#ebebeb'))
            QApplication.setPalette(self.palette)
        if index == 2:
            self.palette.setColor(QtGui.QPalette.ButtonText,
                                  QtGui.QColor(53, 53, 53))
            QApplication.setPalette(self.palette)
        if index == 3:
            self.palette.setColor(QtGui.QPalette.ButtonText,
                                  QtGui.QColor('#35b9ff'))
            QApplication.setPalette(self.palette)
        if index == 4:
            self.palette.setColor(QtGui.QPalette.ButtonText,
                                  QtGui.QColor('#163393'))
            QApplication.setPalette(self.palette)
        if index == 5:
            self.palette.setColor(QtGui.QPalette.ButtonText,
                                  QtGui.QColor('#ee8bff'))
            QApplication.setPalette(self.palette)
        if index == 6:
            self.palette.setColor(QtGui.QPalette.ButtonText,
                                  QtGui.QColor('#9538bd'))
            QApplication.setPalette(self.palette)
        if index == 7:
            self.palette.setColor(QtGui.QPalette.ButtonText,
                                  QtGui.QColor('#55aa00'))
            QApplication.setPalette(self.palette)
        if index == 8:
            self.palette.setColor(QtGui.QPalette.ButtonText,
                                  QtGui.QColor('#ffff7f'))
            QApplication.setPalette(self.palette)
        if index == 9:
            self.palette.setColor(QtGui.QPalette.ButtonText,
                                  QtGui.QColor('#ff0000'))
            QApplication.setPalette(self.palette)
        if index == 10:
            self.palette.setColor(QtGui.QPalette.ButtonText,
                                  QtGui.QColor('#ffaa00'))
        if index == 11:
            self.palette.setColor(QtGui.QPalette.BrightText,
                                  QtGui.QColor('#353535'))
        QApplication.setPalette(self.palette)

    def SliderTheme(self, index):
        # Color of Slider in comboBox
        color = ["#ffffff", "#ebebeb", "#353535", "#35b9ff", "#163393",
                 "#ee8bff", "#9538bd", "#55aa00", "#ffff7f", "#ff0000", "#ffaa00"]
        if self.checkBox_Theme.isChecked():
            # Set stylesheet for Sliders Classic

            StyleSheet_Slider = ("")
        else:
            # Set stylesheet for Sliders Fusion
            StyleSheet_Slider = ("""
                QSlider::groove:horizontal {
                    border: 1px solid white;
                    background: white;
                    height: 1px;
                    border-radius: 4px;
                }""" +

                                 "QSlider::sub-page:horizontal {" +
                                 f"background: {color[index]};" +
                                 """border: 1px solid #777;
                    height: 10px;
                    border-radius: 4px;
                }""" +

                                 """QSlider::add-page:horizontal {
                    background: #fff;
                    border: 1px solid Gray;
                    height: 10px;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {""" +
                                 f"background-color: {color[index]};" +
                                 """border: 1px solid;
                    height: 10px;
                    width: 10px;
                    margin: -5px 0px;
                    border-radius: 4px;
                }
            """)
        self.MediaPlayer.Slider_Volume.setStyleSheet(StyleSheet_Slider)
        self.MediaPlayer.Slider_Play.setStyleSheet(StyleSheet_Slider)

    def Theme_apply(self):
        with open('SettingPart/Setting.csv') as file:

            Setting_reader = csv.reader(file)
            Dict = {rows[0]: rows[1] for rows in Setting_reader}
            self.comboBox_Theme.setCurrentIndex(int(Dict['Theme']))
            self._Theme(int(Dict['Theme']))
            self.Classic_Theme(int(Dict['Classic']))
            self.checkBox_Theme.setChecked(int(Dict['Classic']))

            self.background_Theme(int(Dict['Background']))
            self.comboBox_Background.setCurrentIndex(
                int(Dict['Background']))

            self.Base_Theme(int(Dict['Base']))
            self.comboBox_Base.setCurrentIndex(int(Dict['Base']))

            self.WindowsText_Theme(int(Dict['WindowText']))
            self.comboBox_WindowsText.setCurrentIndex(
                int(Dict['WindowText']))

            self.Text_Theme(int(Dict['Text']))
            self.comboBox_Text.setCurrentIndex(int(Dict['Text']))

            self.Button_Theme(int(Dict['Button']))
            self.comboBox_Button.setCurrentIndex(int(Dict['Button']))

            self.ButtonText_Theme(int(Dict['ButtonText']))
            self.comboBox_ButtonText.setCurrentIndex(
                int(Dict['ButtonText']))

            self.SliderTheme(int(Dict['Slider Color']))
            self.comboBox_Slider.setCurrentIndex(int(Dict['Slider Color']))

            # self.Slider_Size_Changed(int(Dict['Slider Size']))
            # self.spinBox_Slider.setValue(int(Dict['Slider Size']))

            if int(Dict['Theme']) != 4:
                self.scrollArea_Theme.setVisible(False)
            elif int(Dict['Theme']) == 4:
                self.scrollArea_Theme.setVisible(True)
