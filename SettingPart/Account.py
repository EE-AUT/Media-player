import Database.Database as get_Database
from oauth2client.service_account import ServiceAccountCredentials
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
import csv
import os


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


def DeleteAcc(SettingWindow, MediaPlayer):

    key = random.randint(10e5, 10e6)
    DeletAccW = DeleteAccountWindow(SettingWindow, MediaPlayer, key)
    DeletAccW.show()
    Sent_Email_ = Sent_Email_Thread(
        SettingWindow, key, read_Pass("Email"))
    Sent_Email_.sent.connect(DeletAccW.check)
    Sent_Email_.start()


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

    def stop(self):
        self.terminate()
        self.wait()


Form = uic.loadUiType(os.path.join(
    os.getcwd(), 'SettingPart/Delete Account.ui'))[0]


class DeleteAccountWindow(QMainWindow, Form, QtCore.QThread):
    def __init__(self, window,MediaPlayer, key):
        QMainWindow.__init__(self)
        Form.__init__(self)
        QtCore.QThread.__init__(self, window)
        self.setupUi(self)
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.key = key
        self.window = window
        self.MediaPlayer = MediaPlayer

        self.Button_No.clicked.connect(self.No)
        self.Button_Yes.clicked.connect(self.Yes)
        self.lineEdit_Code.textChanged.connect(
            lambda: self.label_Error_code.setVisible(False))
        self.label_Error.setVisible(False)
        self.label_Error_code.setVisible(False)

    def check(self, val):
        if not val:
            self.label_Error.setVisible(True)
            self.Button_No.setEnabled(True)
            self.Button_Yes.setEnabled(False)
        else:
            self.Button_Yes.setEnabled(True)

    def Yes(self):
        if self.key == int(self.lineEdit_Code.text()):
            self.Button_No.setEnabled(False)
            self.Button_Yes.setEnabled(False)
            self.label_Error_code.setVisible(False)
            Delacc = DeleteAcc_Thread(self.window, self.MediaPlayer)
            Delacc.start()
            Delacc.DeleteAccount.connect(self.check)

        else:
            self.label_Error_code.setVisible(True)

    def No(self):
        self.label_Error_code.setVisible(False)
        self.label_Error.setVisible(False)
        self.Button_No.setEnabled(True)
        self.Button_Yes.setEnabled(True)
        self.close()


class Sent_Email_Thread(QtCore.QThread):
    sent = QtCore.pyqtSignal(bool)

    def __init__(self, window, code, receiver_address):
        QtCore.QThread.__init__(self, window)
        self.receiver_address = receiver_address
        self.Text = f'''Hello 
        You recently requested to Delete your Account .
        Your Verification code is :{code}
        If you did not request to Delete Account , Please ignore this email or reply to let us know .
        Thank You
        Media Player'''

    def run(self):
        # The mail addresses and password
        sender_address = 'ap.mediaplayer@gmail.com'
        sender_pass = 'AP_MediaPlayer2020'  # secret :)
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = self.receiver_address
        # The subject line
        message['Subject'] = 'AP MediaPlayer Delete Account.'
        # The body and the attachments for the mail
        message.attach(MIMEText(self.Text, 'plain'))
        # Create SMTP session for sending the mail
        try:
            # use gmail with port
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()  # enable security
            # login with mail_id and password
            session.login(sender_address, sender_pass)

            text = message.as_string()
            session.sendmail(sender_address, self.receiver_address, text)
            session.quit()
            self.sent.emit(True)
        except:
            self.sent.emit(False)

    def stop(self):
        self.terminate()
        self.wait()


class DeleteAcc_Thread(QtCore.QThread):
    DeleteAccount = QtCore.pyqtSignal(bool)

    def __init__(self, window, MediaPlayer):
        QtCore.QThread.__init__(self, parent=window)
        self.MediaPlayer = MediaPlayer
        self.window=window

    def run(self):
        result = get_Database.Delete_Account(
            self.MediaPlayer,self.window, read_Pass('Email'))
        self.DeleteAccount.emit(result)

    def stop(self):
        self.terminate()
        self.wait()
