from PyQt5.QtWidgets import QDialog
from PyQt5 import uic, QtCore, QtGui
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import Database.Database as get_Database
import os


Form = uic.loadUiType(os.path.join(os.getcwd(), 'LoginPart/ForgetPass.ui'))[0]


class ForgetPassWindow(QDialog, Form):
    def __init__(self, window):
        QDialog.__init__(self)
        Form.__init__(self)
        self.setupUi(self)

        # To Specialize flags
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.label_sent.setVisible(False)
        self.label_Error_Connection.setVisible(False)
        self.label_Incorrect.setVisible(False)
        self.label_Wait.setVisible(False)
        self.pushButton_sent.setEnabled(False)

        self.lineEdit_Email.textChanged.connect(self.Edit_Email)
        self.lineEdit_StudentID.textChanged.connect(self.Edit_studentID)

        self.pushButton_Back.clicked.connect(self.Back)
        # To get Data from Database in new Thread
        self.Get_Data = Get_Data(self)
        self.Get_Data.Data.connect(self.Sent_Email)
        self.pushButton_sent.clicked.connect(self.start_to_sent)

        # Close Event to stop running thread
        self.closeEvent = self.Close
        # initial for threads
        self.Sent_Email_ = None

    def Edit_Email(self, val):
        self.label_Incorrect.setVisible(False)
        if val and self.lineEdit_StudentID.text():
            self.pushButton_sent.setEnabled(True)
        else:
            self.pushButton_sent.setEnabled(False)

    def Edit_studentID(self, val):
        self.label_Incorrect.setVisible(False)
        if val and self.lineEdit_Email.text():
            self.pushButton_sent.setEnabled(True)
        else:
            self.pushButton_sent.setEnabled(False)

    def start_to_sent(self):
        self.pushButton_sent.setEnabled(False)
        self.label_Wait.setVisible(True)
        self.pushButton_Back.setEnabled(False)
        self.Get_Data.start()

    def Back(self):
        #Reset to factory! and close
        self.label_sent.setVisible(False)
        self.label_Error_Connection.setVisible(False)
        self.lineEdit_Email.clear()
        self.lineEdit_StudentID.clear()
        self.label_Incorrect.setVisible(False)
        self.label_Wait.setVisible(False)
        self.pushButton_sent.setEnabled(False)
        self.close()

    def Sent_Email(self, data):
        if data:
            self.Password = None
            self.label_Error_Connection.setVisible(False)
            self.label_Incorrect.setVisible(False)
            for user in data:
                if str(user["Email"]).lower() == self.lineEdit_Email.text().lower():
                    if str(user["studentNO"]) == self.lineEdit_StudentID.text():
                        self.Password = user["password"][1:]
                        # sent Email in new Thread
                        self.Sent_Email_ = Sent_Email_Thread(
                            self, user['FirstName'], user['LastName'], self.Password, self.lineEdit_Email.text())
                        self.Sent_Email_.sent.connect(self.Check)
                        self.Sent_Email_.start()
            if not self.Password:  # Password is incorrect
                self.label_Incorrect.setVisible(True)
                self.label_Wait.setVisible(False)
                self.pushButton_Back.setEnabled(True)
                self.pushButton_sent.setEnabled(True)
        else:  # connection fail
            self.label_Error_Connection.setVisible(True)
            self.label_Wait.setVisible(False)
            self.pushButton_Back.setEnabled(True)
            self.pushButton_sent.setEnabled(True)

    def Check(self, val):
        if val:  # Everything is ok !
            self.label_sent.setVisible(True)
            self.label_Error_Connection.setVisible(False)

        else:  # Connection fail
            self.label_Error_Connection.setVisible(True)
            self.label_sent.setVisible(False)
        self.label_Wait.setVisible(False)
        self.pushButton_Back.setEnabled(True)
        self.pushButton_sent.setEnabled(True)

    def Close(self, val):
        try:
            self.Get_Data.stop()
            if self.Sent_Email_:
                self.Sent_Email_.stop()
        except:
            pass


class Get_Data(QtCore.QThread):
    Data = QtCore.pyqtSignal(list)

    def __init__(self, window):
        QtCore.QThread.__init__(self, window)

    def run(self):
        try:
            self.Data.emit(get_Database.get_Database())
        except:  # Error in connection
            self.Data.emit([])

    def stop(self):
        self.terminate()
        self.wait()


class Sent_Email_Thread(QtCore.QThread):
    sent = QtCore.pyqtSignal(bool)

    def __init__(self, window, FirstName, LastName, Password, receiver_address):
        QtCore.QThread.__init__(self, window)
        self.receiver_address = receiver_address
        self.Text = f'''Hello {FirstName} {LastName},
        You recently requested to receive your password .
        Your Password is :{Password}
        If you did not request to receive password , Please ignore this email or reply to let us know .
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
        message['Subject'] = 'AP MediaPlayer Password recovery.'
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
