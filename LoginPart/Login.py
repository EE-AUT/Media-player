from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog, QLabel
import os
import sys
import csv
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import Qt
from time import sleep
from signupPart.signUp import signUpWindow
import Database.Database as get_Database
import SettingPart.Setting as Setting


Form = uic.loadUiType(os.path.join(os.getcwd(), 'LoginPart/Login.ui'))[0]


class LoginWindow(QDialog, Form):
    def __init__(self, parent=None):
        Form.__init__(self)
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Login")
        self.StudentID = str('')
        self.Email = str('')

        # Event
        self.LoginButton.clicked.connect(self.Login)
        self.LoginButton.setEnabled(False)
        self.signButton.clicked.connect(self.signUp)
        self.clearButton.clicked.connect(self.clear)
        self.clearButton.setEnabled(False)
        self.lineEdit_StudentID.textChanged.connect(self.StudentID_update)
        self.lineEdit_Email.textChanged.connect(self.Email_update)
        self.label_Forget.mousePressEvent = self.forget_Pass

        # Message Label
        self.Label_Msg = QLabel(self)
        self.Label_Msg.setVisible(False)
        self.Label_Msg.resize(240, 40)
        self.Label_Msg.move(self.size().width()/2 - 120,
                            self.size().height()/2 - 90)
        self.Label_Msg.setAlignment(Qt.AlignCenter)

        # Threads
        self.GetData = GetData_Thread(self)
        self.GetData.data_isReady.connect(self.checkData)
        self.wait = wait_Toclear_thread(self)
        self.wait.isFinished.connect(self.clear_msg)

        self.closeEvent = self.closeThreads  # stop all thread
        self.AcceptKey = False

    def StudentID_update(self, val):
        self.StudentID = val
        self.lineEdit_StudentID.setStyleSheet("")
        if self.StudentID:
            self.clearButton.setEnabled(True)
            if self.lineEdit_Email.text():
                self.LoginButton.setEnabled(True)
        else:
            if not self.lineEdit_Email.text():
                self.clearButton.setEnabled(False)
            self.LoginButton.setEnabled(False)

    def Email_update(self, email):
        self.Email = email.lower()
        self.lineEdit_Email.setStyleSheet("")
        if self.Email:
            self.clearButton.setEnabled(True)
            if self.lineEdit_StudentID.text():
                self.LoginButton.setEnabled(True)
        else:
            if not self.lineEdit_StudentID.text():
                self.clearButton.setEnabled(False)
            self.LoginButton.setEnabled(False)

    def clear(self):
        self.lineEdit_StudentID.clear()
        self.lineEdit_Email.clear()

    def Login(self):
        if self.GetData:
            self.user_Message("please wait ...", "rgb(0, 170, 0)", wait=False)
            self.LoginButton.setEnabled(False)
            self.GetData.start()

    def checkData(self, Data):
        self.check = checkData_Thread(
            self, Data=Data, Email=self.Email, StNo=self.StudentID)
        self.check.check_Key.connect(self.isAccept)
        self.check.start()

    def isAccept(self, key):
        if key:
            open("LoginPart/User.csv", "w")
            self.GetData = None
            self.check = None
            self.wait = None
            self.close()
            self.AcceptKey = True
        else:
            self.AcceptKey = False
            self.user_Message("Email or Password wrong!", "rgb(255, 0, 0)", 10)
            self.LoginButton.setEnabled(True)
            self.lineEdit_StudentID.setStyleSheet("background:#ff967c")
            self.lineEdit_Email.setStyleSheet("background:#ff967c")

    def LoginAccept(self):
        return self.AcceptKey

    def signUp(self):
        self.signUpwin = signUpWindow(self)
        self.signUpwin.show()
        self.setVisible(False)
        self.signUpwin.closeEvent = self.close_Sign

    def close_Sign(self, val):
        self.setVisible(True)

    def closeThreads(self, val):
        self.GetData = None
        self.check = None
        self.wait = None

    def clear_msg(self, check):
        if check:
            self.Label_Msg.setVisible(False)

    def forget_Pass(self, val):
        print("forget pass")

    def clear_msg(self, check):
        if check:
            self.Label_Msg.setVisible(False)

    def user_Message(self, msg, color, font=12, wait=True):
        self.Label_Msg.setVisible(True)
        self.Label_Msg.setText(msg)

        stylesheet1 = ("""
            QLabel{
                color: """ + color + ";"
                       )
        stylesheet2 = ("""
                font: """ + str(font) + "pt;}"
                       )
        self.Label_Msg.setStyleSheet(stylesheet1 + stylesheet2)
        if self.wait:
            if wait:
                self.wait.start()


class GetData_Thread(QtCore.QThread):
    data_isReady = QtCore.pyqtSignal(list)

    def __init__(self, window):
        QtCore.QThread.__init__(self, parent=window)

    def run(self):
        data = get_Database.get_Database()
        if not data:
            self.data_isReady.emit([])
        else:
            self.data_isReady.emit(data)


class checkData_Thread(QtCore.QThread):
    check_Key = QtCore.pyqtSignal(bool)

    def __init__(self, window, Data, Email, StNo):
        self.Data = Data
        self.Email = Email
        self.StNo = StNo
        QtCore.QThread.__init__(self, parent=window)

    def run(self):
        for user in self.Data:
            if str(user["Email"]) == str(self.Email):
                if str(user["sudentNO"]) == str(self.StNo):
                    self.check_Key.emit(True)
                    break
            self.check_Key.emit(False)


class wait_Toclear_thread(QtCore.QThread):
    isFinished = QtCore.pyqtSignal(bool)

    def __init__(self, window):
        QtCore.QThread.__init__(self, parent=window)

    def run(self):
        sleep(2.5)
        self.isFinished.emit(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = LoginWindow()
    w.show()
    sys.exit(app.exec_())
