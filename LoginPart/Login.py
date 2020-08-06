from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog, QLabel, QLineEdit
import os
import sys
import csv
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import Qt
from time import sleep
from signupPart.signUp import signUpWindow
import Database.Database as get_Database
import LoginPart.ForgetPass as ForgetPass
import socket


Form = uic.loadUiType(os.path.join(os.getcwd(), 'LoginPart/Login.ui'))[0]


class LoginWindow(QDialog, Form):
    def __init__(self, parent=None):
        Form.__init__(self)
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Login")
        self.Password = str('')
        self.Email = str('')

        # Event
        self.LoginButton.clicked.connect(self.Login)
        self.LoginButton.setEnabled(False)
        self.signButton.clicked.connect(self.signUp)
        self.clearButton.clicked.connect(self.clear)
        self.clearButton.setEnabled(False)
        self.lineEdit_Password.textChanged.connect(self.Password_update)
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
        self.check_net = is_connected(self)
        self.check_net.isConnected.connect(self.check_connection)

        self.closeEvent = self.closeThreads  # stop all thread
        self.signUpwin = None
        self.AcceptKey = False

        # lineEdit pass
        self.lineEdit_Password.setEchoMode(QLineEdit.Password)

        # first definition of threads
        self.check = None

    # update pasword from pass line edit

    def Password_update(self, val):
        self.Password = str(val)
        self.lineEdit_Password.setStyleSheet("")
        # hanle button situation of buttons
        if self.Password:
            self.clearButton.setEnabled(True)
            if self.lineEdit_Email.text():
                self.LoginButton.setEnabled(True)
        else:
            if not self.lineEdit_Email.text():
                self.clearButton.setEnabled(False)
            self.LoginButton.setEnabled(False)

    # update email from pass line edit

    def Email_update(self, email):
        self.Email = email.lower()
        self.lineEdit_Email.setStyleSheet("")
        # hanle button situation of buttons
        if self.Email:
            self.clearButton.setEnabled(True)
            if self.lineEdit_Password.text():
                self.LoginButton.setEnabled(True)
        else:
            if not self.lineEdit_Password.text():
                self.clearButton.setEnabled(False)
            self.LoginButton.setEnabled(False)

    # clear all line edits using clear button

    def clear(self):
        self.lineEdit_Password.clear()
        self.lineEdit_Email.clear()

    # login button
    def Login(self):
        self.check_net.start()

    # chack correctance of input information
    def checkData(self, Data):
        if len(Data) == 0:
            self.user_Message("connection failed", "rgb(255, 0, 0)")
            self.LoginButton.setEnabled(True)
        else:
            # start thread to check verification of information
            self.check = checkData_Thread(
                self, Data=Data, Email=self.Email, Pass="#" + self.Password)
            self.check.check_Key.connect(self.isAccept)
            self.check.start()

    # if input information is correct

    def isAccept(self, key):
        if key:
            open("LoginPart/User.csv",
                 "w").write(f"{self.Email},{self.Password}")
            self.GetData = None
            self.check = None
            self.wait = None
            self.check_net = None
            self.close()
            self.AcceptKey = True
        else:
            self.AcceptKey = False
            self.user_Message("Email or Password wrong!", "rgb(255, 0, 0)", 10)
            self.LoginButton.setEnabled(True)
            self.lineEdit_Password.setStyleSheet("background:#ff967c")
            self.lineEdit_Email.setStyleSheet("background:#ff967c")

    def LoginAccept(self):
        return self.AcceptKey

    # signup button clicked

    def signUp(self):
        # show sign uo window
        self.signUpwin = signUpWindow(self)
        self.signUpwin.show()
        self.setVisible(False)
        self.signUpwin.closeEvent = self.close_Sign

    # stop runnig thread in sign up win
    def close_Sign(self, val):
        self.setVisible(True)
        if self.signUpwin.check_Mail:
            self.signUpwin.check_Mail.terminate()
        if self.signUpwin.send_Email_Thread:
            self.signUpwin.send_Email_Thread.stop()
        if self.signUpwin.wait_Toconfirm:
            self.signUpwin.wait_Toconfirm.stop()
        if self.signUpwin.Confirm_thread:
            self.signUpwin.Confirm_thread.stop()
        if self.signUpwin.wait_To_clearMsg:
            self.signUpwin.wait_To_clearMsg.stop()

    # close login threads

    def closeThreads(self, val):
        if self.GetData:
            self.GetData.stop()
        if self.check:
            self.check.stop()
        if self.wait:
            self.wait.stop()
        if self.check_net:
            self.check_net.stop()

    # clear label massage
    def clear_msg(self, check):
        if check:
            self.Label_Msg.setVisible(False)

    def forget_Pass(self, val):
        ForgetPassW = ForgetPass.ForgetPassWindow(self)
        ForgetPassW.show()

    # check connection and starting thread to login

    def check_connection(self, val):
        if val:
            if self.GetData:
                self.user_Message("please wait ...",
                                  "rgb(0, 255, 127)", wait=False)
                self.LoginButton.setEnabled(False)
                self.GetData.start()
        else:
            self.user_Message("Connection failed", "rgb(255, 0, 0)")

    # user message window to show message with our css format

    def user_Message(self, msg, color, font=12, wait=True):
        self.Label_Msg.setVisible(True)
        self.Label_Msg.setText(msg)

        # css of color
        stylesheet1 = ("""
            QLabel{
                color: """ + color + ";"
                       )
        # css of font size
        stylesheet2 = ("""
                font: """ + str(font) + "pt;}"
                       )
        self.Label_Msg.setStyleSheet(stylesheet1 + stylesheet2)
        if self.wait:
            if wait:
                self.wait.start()


# get data thread to get all user information
# from google sheet using Database mudole's function
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

    def stop(self):  # stop thread
        self.terminate()
        self.wait()


# check information of user
class checkData_Thread(QtCore.QThread):
    check_Key = QtCore.pyqtSignal(bool)

    def __init__(self, window, Data, Email, Pass):
        self.Data = Data
        self.Email = Email
        self.Pass = Pass
        QtCore.QThread.__init__(self, parent=window)

    def run(self):
        for user in self.Data:
            if str(user["Email"]) == str(self.Email):
                if str(user["password"]) == str(self.Pass):
                    self.check_Key.emit(True)
                    break
            self.check_Key.emit(False)

    def stop(self):  # stop thread
        self.terminate()
        self.wait()


# wait thread
# wait for clear label message 2.5 second
class wait_Toclear_thread(QtCore.QThread):
    isFinished = QtCore.pyqtSignal(bool)

    def __init__(self, window):
        QtCore.QThread.__init__(self, parent=window)

    def run(self):
        sleep(2.5)
        self.isFinished.emit(True)

    def stop(self):  # stop thread
        self.terminate()
        self.wait()


# check connectivity of internet using socket library
class is_connected(QtCore.QThread):
    isConnected = QtCore.pyqtSignal(bool)

    def __init__(self, window):
        QtCore.QThread.__init__(self, parent=window)

    def run(self):
        try:
            # connect to 1.1.1.1 if can else coneectiob faild
            socket.create_connection(("1.1.1.1", 53))
            self.isConnected.emit(True)
            return
        except Exception as e:
            pass
        self.isConnected.emit(False)

    def stop(self):  # stop thread
        self.terminate()
        self.wait()

