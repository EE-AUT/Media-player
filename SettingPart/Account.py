import Database.Database as get_Database
from oauth2client.service_account import ServiceAccountCredentials
from PyQt5 import QtCore
import csv


def CurrentPass(SettingWindow, val):
    if val:
        SettingWindow.Account_changing = True

    else:
        SettingWindow.Account_changing = False
    SettingWindow.label_OldPass.setVisible(False)


def ReNewpass(SettingWindow):
    if SettingWindow.lineEdit_NewPass.text() != SettingWindow.lineEdit_ReNewpass.text():
        SettingWindow.label_NotMatch.setVisible(True)
    else:
        SettingWindow.label_NotMatch.setVisible(False)


def NewPass(SettingWindow):
    if len(SettingWindow.lineEdit_NewPass.text()) < 8:
        SettingWindow.label_PassLong.setVisible(True)
    else:
        SettingWindow.label_PassLong.setVisible(False)
    SettingWindow.label_NotMatch.setVisible(False)


def read_Pass(mode):
    with open("LoginPart/User.csv") as file:
        file_reader = file.read()
        if mode == 'Pass':
            return file_reader.split(',')[1]
        if mode == 'Email':
            return file_reader.split(',')[0]


class Apply_Thread(QtCore.QThread):
    pass_changed = QtCore.pyqtSignal(bool)

    def __init__(self, window):
        QtCore.QThread.__init__(self, parent=window)
        self.window = window

    def run(self):
        if read_Pass('Pass') == self.window.lineEdit_CurrentPass.text():
            if len(self.window.lineEdit_NewPass.text()) > 7:
                if self.window.lineEdit_NewPass.text() == self.window.lineEdit_ReNewpass.text():
                    result = get_Database.Change_password(
                            read_Pass('Pass'), self.window.lineEdit_NewPass.text())
                    self.pass_changed.emit(result)
