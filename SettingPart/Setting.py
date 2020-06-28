from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic, QtCore, QtGui
import os

Form = uic.loadUiType(os.path.join(os.getcwd(), 'SettingPart/Setting.ui'))[0]


class SettingWindow(QMainWindow, Form, QtCore.QThread):
    def __init__(self, Mediaplayer):
        QMainWindow.__init__(self)
        Form.__init__(self)
        QtCore.QThread.__init__(self, parent=Mediaplayer)
        self.setupUi(self)
        self.MediaPlayer = Mediaplayer

        self.pushButton_Cancel.clicked.connect(lambda: self.close())
        self.pushButton_OK.clicked.connect(self.saveANDexit)
        self.comboBox_Theme.activated.connect(self._Theme)
        self.scrollArea_Theme.setVisible(False)


    def saveANDexit(self):
        pass

    def _Theme(self, index):
        if index == 0:
            QApplication.setStyle("Fusion")
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#ebebeb'))
            palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.black)
            palette.setColor(QtGui.QPalette.Base, QtGui.QColor('#ffffff'))
            # palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor("#c5c5c5"))
            # palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.black)
            # palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.black)
            palette.setColor(QtGui.QPalette.Text, QtGui.QColor('#000000'))
            palette.setColor(QtGui.QPalette.Button, QtGui.QColor('#ffffff'))
            palette.setColor(QtGui.QPalette.ButtonText,
                             QtGui.QColor('#000000'))
            # palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.black)
            palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor('#2c88f7'))
            palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
            QApplication.setPalette(palette)
            self.scrollArea_Theme.setVisible(False)
            # Set styleSheet for Search and Bookmarks LineEdit
            styleSheet_LineEdits = ("""
                QLineEdit{ 
                    background-color: #b5e2ff;
                    border: 2px solid gray;
                    border-radius: 4px;
                    padding: 0 8px;
                    selection-background-color: darkgray;
                    font-size: 14px;
                }
            """)
            self.MediaPlayer.search_lineEdit.setStyleSheet(
                styleSheet_LineEdits)
            self.MediaPlayer.write_Bookmark.setStyleSheet(styleSheet_LineEdits)

            # Set styleSheet for Search listWidget
            self.MediaPlayer.sch_listWidget.setStyleSheet("""
                QListWidget{ 
                    background-color:#b5e2ff;
                    border: 2px solid gray;
                    border-radius: 4px;
                    padding: 0 8px;
                    selection-background-color: darkgray;
                    font-size: 14px;
                }
            """)
            # Set stylesheet for Sliders
            StyleSheet_Slider = ("""
                QSlider::groove:horizontal {
                    border: 1px solid white;
                    background: white;
                    height: 1px;
                    border-radius: 4px;
                }

                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1, stop: 0 #5566ff, stop: 1 #8bd3ff);
                    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, stop: 0 #8bd3ff, stop: 1 #5566ff);
                    border: 1px solid #777;
                    height: 10px;
                    border-radius: 4px;
                }
                    
                QSlider::add-page:horizontal {
                    background: #fff;
                    border: 1px solid white;
                    height: 10px;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background-color: #2c88f7;
                    border: 1px solid;
                    height: 10px;
                    width: 10px;
                    margin: -5px 0px;
                    border-radius: 4px;
                }
            """)
            self.MediaPlayer.Slider_Volume.setStyleSheet(StyleSheet_Slider)
            self.MediaPlayer.Slider_Play.setStyleSheet(StyleSheet_Slider)

        if index == 1:
            QApplication.setStyle("Fusion")
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
            palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
            palette.setColor(QtGui.QPalette.AlternateBase,
                             QtGui.QColor(53, 53, 53))
            palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
            palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
            palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor('#cb90ff'))
            palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
            QApplication.setPalette(palette)
            self.scrollArea_Theme.setVisible(False)
            # Set styleSheet for Search and Bookmarks LineEdit
            styleSheet_LineEdits = ("""
                QLineEdit{ 
                    background-color: #dcb4ff;
                    border: 2px solid gray;
                    border-radius: 4px;
                    padding: 0 8px;
                    selection-background-color: darkgray;
                    font-size: 14px;
                }
            """)
            self.MediaPlayer.search_lineEdit.setStyleSheet(
                styleSheet_LineEdits)
            self.MediaPlayer.write_Bookmark.setStyleSheet(styleSheet_LineEdits)
            pal = self.MediaPlayer.search_lineEdit.palette()
            pal.setColor(QtGui.QPalette.PlaceholderText, QtGui.QColor("Gray"))
            pal.setColor(QtGui.QPalette.Text, QtGui.QColor("Black"))
            self.MediaPlayer.search_lineEdit.setPalette(pal)
            pal = self.MediaPlayer.write_Bookmark.palette()
            pal.setColor(QtGui.QPalette.PlaceholderText, QtGui.QColor("Gray"))
            pal.setColor(QtGui.QPalette.Text, QtGui.QColor("Black"))
            self.MediaPlayer.write_Bookmark.setPalette(pal)

            # Set styleSheet for Search listWidget
            self.MediaPlayer.sch_listWidget.setStyleSheet("""
                QListWidget{ 
                    background-color:#dcb4ff;
                    border: 2px solid gray;
                    border-radius: 4px;
                    padding: 0 8px;
                    selection-background-color: darkgray;
                    font-size: 14px;
                }
            """)
            # Set stylesheet for Sliders
            StyleSheet_Slider = ("""
                QSlider::groove:horizontal {
                    border: 1px solid white;
                    background: white;
                    height: 1px;
                    border-radius: 4px;
                }

                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1, stop: 0 #762d8a, stop: 1 #dcb4ff);
                    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, stop: 0 #dcb4ff, stop: 1 #762d8a);
                    border: 1px solid #777;
                    height: 10px;
                    border-radius: 4px;
                }
                    
                QSlider::add-page:horizontal {
                    background: #fff;
                    border: 1px solid Gray;
                    height: 10px;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background-color: #aa6ec3;
                    border: 1px solid;
                    height: 10px;
                    width: 10px;
                    margin: -5px 0px;
                    border-radius: 4px;
                }
            """)
            self.MediaPlayer.Slider_Volume.setStyleSheet(StyleSheet_Slider)
            self.MediaPlayer.Slider_Play.setStyleSheet(StyleSheet_Slider)

        if index == 2:
            QApplication.setStyle("Windows")
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
            palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
            palette.setColor(QtGui.QPalette.AlternateBase,
                             QtGui.QColor(53, 53, 53))
            palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
            palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
            palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor('#cb90ff'))
            palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
            QApplication.setPalette(palette)
            self.scrollArea_Theme.setVisible(False)

            # Set styleSheet for Search and Bookmarks LineEdit
            styleSheet_LineEdits = ("""
                QLineEdit{ 
                    background-color: #dcb4ff;
                    border: 2px solid gray;
                    border-radius: 4px;
                    padding: 0 8px;
                    selection-background-color: darkgray;
                    font-size: 14px;
                }
            """)
            self.MediaPlayer.search_lineEdit.setStyleSheet(
                styleSheet_LineEdits)
            self.MediaPlayer.write_Bookmark.setStyleSheet(styleSheet_LineEdits)
            pal = self.MediaPlayer.search_lineEdit.palette()
            pal.setColor(QtGui.QPalette.PlaceholderText, QtGui.QColor("Gray"))
            pal.setColor(QtGui.QPalette.Text, QtGui.QColor("Black"))
            self.MediaPlayer.search_lineEdit.setPalette(pal)
            pal = self.MediaPlayer.write_Bookmark.palette()
            pal.setColor(QtGui.QPalette.PlaceholderText, QtGui.QColor("Gray"))
            pal.setColor(QtGui.QPalette.Text, QtGui.QColor("Black"))
            self.MediaPlayer.write_Bookmark.setPalette(pal)

            # Set styleSheet for Search listWidget
            self.MediaPlayer.sch_listWidget.setStyleSheet("""
                QListWidget{ 
                    background-color:#dcb4ff;
                    border: 2px solid gray;
                    border-radius: 4px;
                    padding: 0 8px;
                    selection-background-color: darkgray;
                    font-size: 14px;
                }
            """)
            # Set stylesheet for Sliders
            StyleSheet_Slider = ("""
                QSlider::groove:horizontal {
                    border: 1px solid white;
                    background: white;
                    height: 1px;
                    border-radius: 4px;
                }

                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1, stop: 0 #762d8a, stop: 1 #dcb4ff);
                    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, stop: 0 #dcb4ff, stop: 1 #762d8a);
                    border: 1px solid #777;
                    height: 10px;
                    border-radius: 4px;
                }
                    
                QSlider::add-page:horizontal {
                    background: #fff;
                    border: 1px solid Gray;
                    height: 10px;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background-color: #aa6ec3;
                    border: 1px solid;
                    height: 10px;
                    width: 10px;
                    margin: -5px 0px;
                    border-radius: 4px;
                }
            """)
            self.MediaPlayer.Slider_Volume.setStyleSheet(StyleSheet_Slider)
            self.MediaPlayer.Slider_Play.setStyleSheet(StyleSheet_Slider)

        if index == 3:
            QApplication.setStyle("windows")
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#ebebeb'))
            palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.black)
            palette.setColor(QtGui.QPalette.Base, QtGui.QColor('#ffffff'))
            # palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor("#c5c5c5"))
            # palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.black)
            # palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.black)
            palette.setColor(QtGui.QPalette.Text, QtGui.QColor('#000000'))
            palette.setColor(QtGui.QPalette.Button, QtGui.QColor('#ffffff'))
            palette.setColor(QtGui.QPalette.ButtonText,
                             QtGui.QColor('#000000'))
            # palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.black)
            palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor('#0057da'))
            palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
            QApplication.setPalette(palette)
            self.scrollArea_Theme.setVisible(False)

            # Set styleSheet for Search and Bookmarks LineEdit
            styleSheet_LineEdits = ("""
                QLineEdit{ 
                    background-color: #b5e2ff;
                    border: 2px solid gray;
                    border-radius: 4px;
                    padding: 0 8px;
                    selection-background-color: darkgray;
                    font-size: 14px;
                }
            """)
            self.MediaPlayer.search_lineEdit.setStyleSheet(
                styleSheet_LineEdits)
            self.MediaPlayer.write_Bookmark.setStyleSheet(styleSheet_LineEdits)
            # Set styleSheet for Search listWidget
            self.MediaPlayer.sch_listWidget.setStyleSheet("""
                QListWidget{ 
                    background-color:#b5e2ff;
                    border: 2px solid gray;
                    border-radius: 4px;
                    padding: 0 8px;
                    selection-background-color: darkgray;
                    font-size: 14px;
                }
            """)
            # Set stylesheet for Sliders
            StyleSheet_Slider = ("""
                QSlider::groove:horizontal {
                    border: 1px solid white;
                    background: white;
                    height: 1px;
                    border-radius: 4px;
                }

                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1, stop: 0 #5566ff, stop: 1 #8bd3ff);
                    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, stop: 0 #8bd3ff, stop: 1 #5566ff);
                    border: 1px solid #777;
                    height: 10px;
                    border-radius: 4px;
                }
                    
                QSlider::add-page:horizontal {
                    background: #fff;
                    border: 1px solid white;
                    height: 10px;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background-color: #2c88f7;
                    border: 1px solid;
                    height: 10px;
                    width: 10px;
                    margin: -5px 0px;
                    border-radius: 4px;
                }
            """)
            self.MediaPlayer.Slider_Volume.setStyleSheet(StyleSheet_Slider)
            self.MediaPlayer.Slider_Play.setStyleSheet(StyleSheet_Slider)

        if index == 4:
            self.palette = QtGui.QPalette()
            self.scrollArea_Theme.setVisible(True)
            self.checkBox_Theme.stateChanged.connect(self.Classic_Theme)
            self.comboBox_Background.activated.connect(self.background_Theme)
            self.comboBox_Base.activated.connect(self.Base_Theme)
            self.comboBox_WindowsText.activated.connect(self.WindowsText_Theme)
            self.comboBox_Text.activated.connect(self.Text_Theme)
            self.comboBox_Button.activated.connect(self.Button_Theme)
            self.comboBox_ButtonText.activated.connect(self.ButtonText_Theme)
            self.comboBox_Slider.activated.connect(self.SliderTheme)

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
        QApplication.setPalette(self.palette)

    def SliderTheme(self, index, size=3):
        color = ["#ffffff", "#ebebeb", "#353535", "#35b9ff", "#163393",
                 "#ee8bff", "#9538bd", "#55aa00", "#ffff7f", "#ff0000", "#ffaa00"]
        # Set stylesheet for Sliders
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

