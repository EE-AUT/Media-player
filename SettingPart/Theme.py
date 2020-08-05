import csv
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui


def saveANDexit(SettingWindow):
    # To Write everything about Setting in Sitting.csv
    with open('SettingPart/Setting.csv', mode='w', newline='') as file:
        Setting_writer = csv.writer(file)
        Setting_writer.writerow(
            ['Theme'] + [SettingWindow.comboBox_Theme.currentIndex()])
        Setting_writer.writerow(
            ['Classic'] + [int(SettingWindow.checkBox_Theme.isChecked())])
        Setting_writer.writerow(
            ['Background'] + [SettingWindow.comboBox_Background.currentIndex()])
        Setting_writer.writerow(
            ['Base'] + [SettingWindow.comboBox_Base.currentIndex()])
        Setting_writer.writerow(
            ['WindowText'] + [SettingWindow.comboBox_WindowsText.currentIndex()])
        Setting_writer.writerow(
            ['Text'] + [SettingWindow.comboBox_Text.currentIndex()])
        Setting_writer.writerow(
            ['Button'] + [SettingWindow.comboBox_Button.currentIndex()])
        Setting_writer.writerow(
            ['ButtonText'] + [SettingWindow.comboBox_ButtonText.currentIndex()])
        Setting_writer.writerow(
            ['Slider Color'] + [SettingWindow.comboBox_Slider.currentIndex()])


def Theme_apply(SettingWindow):
    # To Read everything about Setting from Sitting.csv
    with open('SettingPart/Setting.csv') as file:
        Setting_reader = csv.reader(file)
        Dict = {rows[0]: rows[1] for rows in Setting_reader}

        SettingWindow.comboBox_Theme.setCurrentIndex(int(Dict['Theme']))
        _Theme(SettingWindow, int(Dict['Theme']))

        Classic_Theme(int(Dict['Classic']))
        SettingWindow.checkBox_Theme.setChecked(int(Dict['Classic']))

        background_Theme(SettingWindow, int(Dict['Background']))
        SettingWindow.comboBox_Background.setCurrentIndex(
            int(Dict['Background']))

        Base_Theme(SettingWindow, int(Dict['Base']))
        SettingWindow.comboBox_Base.setCurrentIndex(int(Dict['Base']))

        WindowsText_Theme(SettingWindow, int(Dict['WindowText']))
        SettingWindow.comboBox_WindowsText.setCurrentIndex(
            int(Dict['WindowText']))

        Text_Theme(SettingWindow, int(Dict['Text']))
        SettingWindow.comboBox_Text.setCurrentIndex(int(Dict['Text']))

        Button_Theme(SettingWindow, int(Dict['Button']))
        SettingWindow.comboBox_Button.setCurrentIndex(int(Dict['Button']))

        ButtonText_Theme(SettingWindow, int(Dict['ButtonText']))
        SettingWindow.comboBox_ButtonText.setCurrentIndex(
            int(Dict['ButtonText']))

        SliderTheme(SettingWindow, int(Dict['Slider Color']))
        SettingWindow.comboBox_Slider.setCurrentIndex(
            int(Dict['Slider Color']))

        if int(Dict['Theme']) != 4:
            SettingWindow.scrollArea_Theme.setVisible(False)
        elif int(Dict['Theme']) == 4:
            SettingWindow.scrollArea_Theme.setVisible(True)


def _Theme(SettingWindow, index):
    # To select Theme
    if index == 0:
        # Light Theme
        Classic_Theme(False)
        SettingWindow.checkBox_Theme.setChecked(False)

        background_Theme(SettingWindow, 1)
        SettingWindow.comboBox_Background.setCurrentIndex(1)

        Base_Theme(SettingWindow, 0)
        SettingWindow.comboBox_Base.setCurrentIndex(0)

        WindowsText_Theme(SettingWindow, 2)
        SettingWindow.comboBox_WindowsText.setCurrentIndex(2)

        Text_Theme(SettingWindow, 2)
        SettingWindow.comboBox_Text.setCurrentIndex(2)

        Button_Theme(SettingWindow, 0)
        SettingWindow.comboBox_Button.setCurrentIndex(0)

        ButtonText_Theme(SettingWindow, 2)
        SettingWindow.comboBox_ButtonText.setCurrentIndex(2)

        SliderTheme(SettingWindow, 3)
        SettingWindow.comboBox_Slider.setCurrentIndex(3)

        SettingWindow.palette.setColor(QtGui.QPalette.Highlight,
                                       QtGui.QColor('#2c88f7'))
        SettingWindow.palette.setColor(
            QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        QApplication.setPalette(SettingWindow.palette)
        SettingWindow.scrollArea_Theme.setVisible(False)

    if index == 1:
        # Dark Theme
        Classic_Theme(False)
        SettingWindow.checkBox_Theme.setChecked(False)

        background_Theme(SettingWindow, 11)
        SettingWindow.comboBox_Background.setCurrentIndex(11)

        Base_Theme(SettingWindow, 2)
        SettingWindow.comboBox_Base.setCurrentIndex(2)

        WindowsText_Theme(SettingWindow, 0)
        SettingWindow.comboBox_WindowsText.setCurrentIndex(0)

        Text_Theme(SettingWindow, 0)
        SettingWindow.comboBox_Text.setCurrentIndex(0)

        Button_Theme(SettingWindow, 11)
        SettingWindow.comboBox_Button.setCurrentIndex(11)

        ButtonText_Theme(SettingWindow, 0)
        SettingWindow.comboBox_ButtonText.setCurrentIndex(0)

        SliderTheme(SettingWindow, 5)
        SettingWindow.comboBox_Slider.setCurrentIndex(5)

        SettingWindow.palette.setColor(QtGui.QPalette.Highlight,
                                       QtGui.QColor('#cb90ff'))
        SettingWindow.palette.setColor(
            QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        QApplication.setPalette(SettingWindow.palette)
        SettingWindow.scrollArea_Theme.setVisible(False)

    if index == 2:
        # Classic Dark Theme
        _Theme(SettingWindow, 1)
        Classic_Theme(True)
        SettingWindow.checkBox_Theme.setChecked(True)
        SliderTheme(SettingWindow, 5)

    if index == 3:
        # Classic Light Theme
        _Theme(SettingWindow, 0)
        Classic_Theme(True)
        SettingWindow.checkBox_Theme.setChecked(True)
        SliderTheme(SettingWindow, 3)

    if index == 4:

        SettingWindow.scrollArea_Theme.setVisible(True)


def Classic_Theme(classic):
    # To Set windows or Fusion style according to Classic
    if classic:
        QApplication.setStyle("Windows")
    else:
        QApplication.setStyle("Fusion")


def background_Theme(SettingWindow, index):
    # To set Background according index(Color)
    if index == 0:
        SettingWindow.palette.setColor(QtGui.QPalette.Window,
                                       QtGui.QColor('#ffffff'))  # White
        QApplication.setPalette(SettingWindow.palette)
    if index == 1:
        SettingWindow.palette.setColor(QtGui.QPalette.Window,
                                       QtGui.QColor('#ebebeb'))  # Silver
        QApplication.setPalette(SettingWindow.palette)
    if index == 2:
        SettingWindow.palette.setColor(QtGui.QPalette.Window,
                                       QtGui.QColor(53, 53, 53))  # Black
        QApplication.setPalette(SettingWindow.palette)
    if index == 3:
        SettingWindow.palette.setColor(QtGui.QPalette.Window,
                                       QtGui.QColor('#35b9ff'))  # Bright Blue
        QApplication.setPalette(SettingWindow.palette)
    if index == 4:
        SettingWindow.palette.setColor(QtGui.QPalette.Window,
                                       QtGui.QColor('#163393'))  # Dark Blue
        QApplication.setPalette(SettingWindow.palette)
    if index == 5:
        SettingWindow.palette.setColor(QtGui.QPalette.Window,
                                       QtGui.QColor('#ee8bff'))  # Bright purple
        QApplication.setPalette(SettingWindow.palette)
    if index == 6:
        SettingWindow.palette.setColor(QtGui.QPalette.Window,
                                       QtGui.QColor('#9538bd'))  # Dark purple
        QApplication.setPalette(SettingWindow.palette)
    if index == 7:
        SettingWindow.palette.setColor(QtGui.QPalette.Window,
                                       QtGui.QColor('#55aa00'))  # Green
        QApplication.setPalette(SettingWindow.palette)
    if index == 8:
        SettingWindow.palette.setColor(QtGui.QPalette.Window,
                                       QtGui.QColor('#ffff7f'))  # Yellow
        QApplication.setPalette(SettingWindow.palette)
    if index == 9:
        SettingWindow.palette.setColor(QtGui.QPalette.Window,
                                       QtGui.QColor('#ff0000'))  # Red
        QApplication.setPalette(SettingWindow.palette)
    if index == 10:
        SettingWindow.palette.setColor(QtGui.QPalette.Window,
                                       QtGui.QColor('#ffaa00'))  # Orange
    if index == 11:
        SettingWindow.palette.setColor(QtGui.QPalette.Window,
                                       QtGui.QColor('#353535'))  # Gray
    QApplication.setPalette(SettingWindow.palette)

##########################


def Base_Theme(SettingWindow, index):
    # To set Base color according index(Color)
    if index == 0:
        SettingWindow.palette.setColor(QtGui.QPalette.Base,
                                       QtGui.QColor('#ffffff'))
    if index == 1:
        SettingWindow.palette.setColor(QtGui.QPalette.Base,
                                       QtGui.QColor('#ebebeb'))
    if index == 2:
        SettingWindow.palette.setColor(QtGui.QPalette.Base,
                                       QtGui.QColor(53, 53, 53))
    if index == 3:
        SettingWindow.palette.setColor(QtGui.QPalette.Base,
                                       QtGui.QColor('#35b9ff'))
    if index == 4:
        SettingWindow.palette.setColor(QtGui.QPalette.Base,
                                       QtGui.QColor('#163393'))
    if index == 5:
        SettingWindow.palette.setColor(QtGui.QPalette.Base,
                                       QtGui.QColor('#ee8bff'))
    if index == 6:
        SettingWindow.palette.setColor(QtGui.QPalette.Base,
                                       QtGui.QColor('#9538bd'))
    if index == 7:
        SettingWindow.palette.setColor(QtGui.QPalette.Base,
                                       QtGui.QColor('#55aa00'))
    if index == 8:
        SettingWindow.palette.setColor(QtGui.QPalette.Base,
                                       QtGui.QColor('#ffff7f'))
    if index == 9:
        SettingWindow.palette.setColor(QtGui.QPalette.Base,
                                       QtGui.QColor('#ff0000'))
    if index == 10:
        SettingWindow.palette.setColor(QtGui.QPalette.Base,
                                       QtGui.QColor('#ffaa00'))
    if index == 11:
        SettingWindow.palette.setColor(QtGui.QPalette.Base,
                                       QtGui.QColor('#353535'))
    QApplication.setPalette(SettingWindow.palette)

###################


def WindowsText_Theme(SettingWindow, index):
    # To set WindowsText color according index(Color)
    if index == 0:
        SettingWindow.palette.setColor(QtGui.QPalette.WindowText,
                                       QtGui.QColor('#ffffff'))
    if index == 1:
        SettingWindow.palette.setColor(QtGui.QPalette.WindowText,
                                       QtGui.QColor('#ebebeb'))
        QApplication.setPalette(SettingWindow.palette)
    if index == 2:
        SettingWindow.palette.setColor(QtGui.QPalette.WindowText,
                                       QtGui.QColor(53, 53, 53))
    if index == 3:
        SettingWindow.palette.setColor(QtGui.QPalette.WindowText,
                                       QtGui.QColor('#35b9ff'))
    if index == 4:
        SettingWindow.palette.setColor(QtGui.QPalette.WindowText,
                                       QtGui.QColor('#163393'))
    if index == 5:
        SettingWindow.palette.setColor(QtGui.QPalette.WindowText,
                                       QtGui.QColor('#ee8bff'))
    if index == 6:
        SettingWindow.palette.setColor(QtGui.QPalette.WindowText,
                                       QtGui.QColor('#9538bd'))
    if index == 7:
        SettingWindow.palette.setColor(QtGui.QPalette.WindowText,
                                       QtGui.QColor('#55aa00'))
    if index == 8:
        SettingWindow.palette.setColor(QtGui.QPalette.WindowText,
                                       QtGui.QColor('#ffff7f'))
    if index == 9:
        SettingWindow.palette.setColor(QtGui.QPalette.WindowText,
                                       QtGui.QColor('#ff0000'))
    if index == 10:
        SettingWindow.palette.setColor(QtGui.QPalette.WindowText,
                                       QtGui.QColor('#ffaa00'))
    if index == 11:
        SettingWindow.palette.setColor(QtGui.QPalette.WindowText,
                                       QtGui.QColor('#353535'))
    QApplication.setPalette(SettingWindow.palette)

#############################


def Text_Theme(SettingWindow, index):
    # To set Text color according index(Color)
    if index == 0:
        SettingWindow.palette.setColor(QtGui.QPalette.Text,
                                       QtGui.QColor('#ffffff'))
    if index == 1:
        SettingWindow.palette.setColor(QtGui.QPalette.Text,
                                       QtGui.QColor('#ebebeb'))
    if index == 2:
        SettingWindow.palette.setColor(QtGui.QPalette.Text,
                                       QtGui.QColor(53, 53, 53))
    if index == 3:
        SettingWindow.palette.setColor(QtGui.QPalette.Text,
                                       QtGui.QColor('#35b9ff'))
    if index == 4:
        SettingWindow.palette.setColor(QtGui.QPalette.Text,
                                       QtGui.QColor('#163393'))
    if index == 5:
        SettingWindow.palette.setColor(QtGui.QPalette.Text,
                                       QtGui.QColor('#ee8bff'))
    if index == 6:
        SettingWindow.palette.setColor(QtGui.QPalette.Text,
                                       QtGui.QColor('#9538bd'))
    if index == 7:
        SettingWindow.palette.setColor(QtGui.QPalette.Text,
                                       QtGui.QColor('#55aa00'))
    if index == 8:
        SettingWindow.palette.setColor(QtGui.QPalette.Text,
                                       QtGui.QColor('#ffff7f'))
    if index == 9:
        SettingWindow.palette.setColor(QtGui.QPalette.Text,
                                       QtGui.QColor('#ff0000'))
    if index == 10:
        SettingWindow.palette.setColor(QtGui.QPalette.Text,
                                       QtGui.QColor('#ffaa00'))
    if index == 11:
        SettingWindow.palette.setColor(QtGui.QPalette.Text,
                                       QtGui.QColor('#353535'))
    QApplication.setPalette(SettingWindow.palette)

###############################


def Button_Theme(SettingWindow, index):
    # To set Button color according index(Color)
    if index == 0:
        SettingWindow.palette.setColor(QtGui.QPalette.Button,
                                       QtGui.QColor('#ffffff'))
    if index == 1:
        SettingWindow.palette.setColor(QtGui.QPalette.Button,
                                       QtGui.QColor('#ebebeb'))
    if index == 2:
        SettingWindow.palette.setColor(QtGui.QPalette.Button,
                                       QtGui.QColor(53, 53, 53))
    if index == 3:
        SettingWindow.palette.setColor(QtGui.QPalette.Button,
                                       QtGui.QColor('#35b9ff'))
    if index == 4:
        SettingWindow.palette.setColor(QtGui.QPalette.Button,
                                       QtGui.QColor('#163393'))
    if index == 5:
        SettingWindow.palette.setColor(QtGui.QPalette.Button,
                                       QtGui.QColor('#ee8bff'))
    if index == 6:
        SettingWindow.palette.setColor(QtGui.QPalette.Button,
                                       QtGui.QColor('#9538bd'))
    if index == 7:
        SettingWindow.palette.setColor(QtGui.QPalette.Button,
                                       QtGui.QColor('#55aa00'))
    if index == 8:
        SettingWindow.palette.setColor(QtGui.QPalette.Button,
                                       QtGui.QColor('#ffff7f'))
    if index == 9:
        SettingWindow.palette.setColor(QtGui.QPalette.Button,
                                       QtGui.QColor('#ff0000'))
    if index == 10:
        SettingWindow.palette.setColor(QtGui.QPalette.Button,
                                       QtGui.QColor('#ffaa00'))
    if index == 11:
        SettingWindow.palette.setColor(QtGui.QPalette.Button,
                                       QtGui.QColor('#353535'))
    QApplication.setPalette(SettingWindow.palette)

###############################


def ButtonText_Theme(SettingWindow, index):
    # To set ButtonText color according index(Color)
    if index == 0:
        SettingWindow.palette.setColor(QtGui.QPalette.ButtonText,
                                       QtGui.QColor('#ffffff'))
    if index == 1:
        SettingWindow.palette.setColor(QtGui.QPalette.ButtonText,
                                       QtGui.QColor('#ebebeb'))
    if index == 2:
        SettingWindow.palette.setColor(QtGui.QPalette.ButtonText,
                                       QtGui.QColor(53, 53, 53))
    if index == 3:
        SettingWindow.palette.setColor(QtGui.QPalette.ButtonText,
                                       QtGui.QColor('#35b9ff'))
    if index == 4:
        SettingWindow.palette.setColor(QtGui.QPalette.ButtonText,
                                       QtGui.QColor('#163393'))
    if index == 5:
        SettingWindow.palette.setColor(QtGui.QPalette.ButtonText,
                                       QtGui.QColor('#ee8bff'))
    if index == 6:
        SettingWindow.palette.setColor(QtGui.QPalette.ButtonText,
                                       QtGui.QColor('#9538bd'))
    if index == 7:
        SettingWindow.palette.setColor(QtGui.QPalette.ButtonText,
                                       QtGui.QColor('#55aa00'))
        QApplication.setPalette(SettingWindow.palette)
    if index == 8:
        SettingWindow.palette.setColor(QtGui.QPalette.ButtonText,
                                       QtGui.QColor('#ffff7f'))
    if index == 9:
        SettingWindow.palette.setColor(QtGui.QPalette.ButtonText,
                                       QtGui.QColor('#ff0000'))
    if index == 10:
        SettingWindow.palette.setColor(QtGui.QPalette.ButtonText,
                                       QtGui.QColor('#ffaa00'))
    if index == 11:
        SettingWindow.palette.setColor(QtGui.QPalette.BrightText,
                                       QtGui.QColor('#353535'))
    QApplication.setPalette(SettingWindow.palette)


def SliderTheme(SettingWindow, index):
    # Create list of Color of Slider in comboBox
    color = ["#ffffff", "#ebebeb", "#353535", "#35b9ff", "#163393",
             "#ee8bff", "#9538bd", "#55aa00", "#ffff7f", "#ff0000", "#ffaa00"]
    if SettingWindow.checkBox_Theme.isChecked():
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
    SettingWindow.MediaPlayer.Slider_Volume.setStyleSheet(StyleSheet_Slider)
    SettingWindow.MediaPlayer.Slider_Play.setStyleSheet(StyleSheet_Slider)
