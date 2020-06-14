from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog
from PyQt5 import uic
import os
import sys
import csv


class LoginDatabase():
    def __init__(self):
        self.dic = {}
        with open("LoginPart/Login.csv") as iFile:
            file_reader = csv.reader(iFile, delimiter=',')
            self.dic = {rows[0]: rows[1] for rows in file_reader}

    def check(self, user):
        for item in self.dic.keys():
            if item.lower() == user[0].lower():
                if self.dic[item] == user[1]:
                    return True
        return False

Form = uic.loadUiType(os.path.join(os.getcwd(), 'LoginPart/Login.ui'))[0]


class LoginWindow(QDialog, Form):
    def __init__(self):
        Form.__init__(self)
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Login")
        self.StudentID =str('')
        self.Email=str('')
        # Event

        self.LoginButton.clicked.connect(self.Login)
        self.LoginButton.setEnabled(False)
        self.clearButton.clicked.connect(self.clear)
        self.clearButton.setEnabled(False)
        self.lineEdit_StudentID.textChanged.connect(self.StudentID_update)
        self.lineEdit_Email.textChanged.connect(self.Email_update)

    def StudentID_update(self, val):
        self.StudentID = val
        self.label_Error.clear()
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
        self.label_Error.clear()
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
        Database = LoginDatabase()
        if Database.check((str(self.Email), str(self.StudentID))):
            self.close()
            return True
        else:
            self.label_Error.setText("Please try again")
            self.lineEdit_StudentID.setStyleSheet("background:#ff967c")
            self.lineEdit_Email.setStyleSheet("background:#ff967c")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = LoginWindow()
    w.show()
    sys.exit(app.exec_())
