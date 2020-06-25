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

        self.pushButton_close.clicked.connect(lambda: self.close())
        self.comboBox_Theme.activated.connect(self._Theme)
        self.scrollArea_Theme.setVisible(False)

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
            self.MediaPlayer.Slider_Play.setStyleSheet("""
                QSlider::groove:horizontal {
                    border: 1px solid #bbb;
                    background: white;
                    height: 3px;
                    border-radius: 4px;
                }

                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1, stop: 0 #aa55ff, stop: 1 #DDA0DD);
                    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, stop: 0 #DDA0DD, stop: 1 #aa55ff);
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
            self.MediaPlayer.Slider_Volume.setStyleSheet("""
                QSlider::groove:horizontal {
                    border: 1px solid #bbb;
                    background: white;
                    height: 3px;
                    border-radius: 4px;
                }

                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1, stop: 0 #aa55ff, stop: 1 #DDA0DD);
                    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, stop: 0 #DDA0DD, stop: 1 #aa55ff);
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

        if index == 4:
            self.scrollArea_Theme.setVisible(True)
            self.checkBox_Theme.stateChanged.connect(self.Classic_Theme)
            self.comboBox_Background.activated.connect(self.background_Theme)

    def Classic_Theme(self, classic):
        if classic:
            QApplication.setStyle("Windows")
        else:
            QApplication.setStyle("Fusion")

    def background_Theme(self, index):
        self.palette = QtGui.QPalette()
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
        if index==3:
            self.palette.setColor(QtGui.QPalette.Window,QtGui.QColor('#35b9ff'))
            QApplication.setPalette(self.palette)
        if index==4:
            self.palette.setColor(QtGui.QPalette.Window,QtGui.QColor('#163393'))
            QApplication.setPalette(self.palette)
        if index==5:
            self.palette.setColor(QtGui.QPalette.Window,QtGui.QColor('#ee8bff'))
            QApplication.setPalette(self.palette)
        if index==6:
            self.palette.setColor(QtGui.QPalette.Window,QtGui.QColor('#9538bd'))
            QApplication.setPalette(self.palette)
        if index==7:
            self.palette.setColor(QtGui.QPalette.Window,QtGui.QColor('#55aa00'))
            QApplication.setPalette(self.palette)
        if index==8:
            self.palette.setColor(QtGui.QPalette.Window,QtGui.QColor('#ffff7f'))
            QApplication.setPalette(self.palette)
        if index==9:
            self.palette.setColor(QtGui.QPalette.Window,QtGui.QColor('#ff0000'))
            QApplication.setPalette(self.palette)
        if index==10:
            self.palette.setColor(QtGui.QPalette.Window,QtGui.QColor('#ffaa00'))
            QApplication.setPalette(self.palette)
