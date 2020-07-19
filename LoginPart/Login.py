from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog, QLabel
import os
import sys
import csv
import signupPart.signUp as signup
from PyQt5 import uic, QtCore, QtGui
from time import sleep
from signupPart.CustomLineEdit import LineEdit as CustomLineEdit


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
        self.StudentID = str('')
        self.Email = str('')
        # Event

        self.LoginButton.clicked.connect(self.Login)
        self.LoginButton.setEnabled(False)
        self.signButton.setEnabled(False)
        self.signButton.clicked.connect(self.signUp)
        self.clearButton.clicked.connect(self.clear)
        self.clearButton.setEnabled(False)
        self.lineEdit_StudentID.textChanged.connect(self.StudentID_update)
        self.lineEdit_Email.textChanged.connect(self.Email_update)
        self.label_Forget.mousePressEvent = self.forget_Pass
        self.Label_Msg = QLabel(self)
        self.Label_Msg.setVisible(False)
        self.Label_Msg.resize(240, 40)
        self.Label_Msg.move(self.size().width()/2 - 120, self.size().height()/2 - 90)
        self.confirm_LineEdit = CustomLineEdit(self)
        self.confirm_LineEdit.returnPressed.connect(self.check_rightKey)
        self.confirm_LineEdit.setVisible(False)
        self.confirm_LineEdit.setPlaceholderText("Enter Key here: 30' remain")
        self.Confirm_key = None

        # threads
        self.send_Email_Thread = None
        self.wait = wait_Toclear_thread(self)
        self.wait.isFinished.connect(self.clear_msg)
        self.wait_Toconfirm = wait_Toconfirm(self)
        self.wait_Toconfirm.Finished_1s.connect(self.Update_Time)
        self.wait_Toconfirm.Finished_Time.connect(self.Time_Ended)


    def StudentID_update(self, val):
        self.StudentID = val
        self.lineEdit_StudentID.setStyleSheet("")
        if self.StudentID:
            self.clearButton.setEnabled(True)
            if self.lineEdit_Email.text():
                self.LoginButton.setEnabled(True)
                self.signButton.setEnabled(True)
        else:
            if not self.lineEdit_Email.text():
                self.clearButton.setEnabled(False)
            self.LoginButton.setEnabled(False)
            self.signButton.setEnabled(False)

    def Email_update(self, email):
        self.Email = email.lower()
        self.lineEdit_Email.setStyleSheet("")
        if self.Email:
            self.clearButton.setEnabled(True)
            if self.lineEdit_StudentID.text():
                self.LoginButton.setEnabled(True)
                self.signButton.setEnabled(True)
        else:
            if not self.lineEdit_StudentID.text():
                self.clearButton.setEnabled(False)
            self.LoginButton.setEnabled(False)
            self.signButton.setEnabled(False)

    def clear(self):
        self.lineEdit_StudentID.clear()
        self.lineEdit_Email.clear()

    def Login(self):
        Database = LoginDatabase()
        if Database.check((str(self.StudentID), str(self.Email))):
            open("LoginPart/User.csv", "w")
            self.close()
            return True
        else:
            self.lineEdit_StudentID.setStyleSheet("background:#ff967c")
            self.lineEdit_Email.setStyleSheet("background:#ff967c")

    def signUp(self):
        # self.setEnabled(False)
        self.signButton.setEnabled(False)
        print("sign")
        if self.check_valid_Email(self.Email):
            self.send_Email_Thread = send_Email(self, receiver= self.Email)
            self.send_Email_Thread.Finished.connect(self.check_verify)
            self.send_Email_Thread.start()
        else:
            self.signButton.setEnabled(True)
            self.user_Message("Invalid Email", "rgb(255, 0, 0)")



    def check_valid_Email(self, address):
        if address.find("@") != -1:
            return True
        return False
        

    def check_verify(self, key):
        if key:
            self.Confirm_key = key
            self.signButton.setEnabled(True)
            print("Finished: ", key)
            self.confirm_LineEdit.setVisible(True)
            self.groupBox.setVisible(False) # invisible MailWindow
            self.wait_Toconfirm.start()
            self.user_Message("message sent", "rgb(0, 170, 0)")
            
        else:
            self.signButton.setEnabled(True)
            self.user_Message("Connection Faild, or invalid Email addres", "rgb(255, 0, 0)", font=8)


            

    def Update_Time(self, val):
        self.confirm_LineEdit.setPlaceholderText(f"Enter Key here: {val}' remain")

    def Time_Ended(self, key):
        if key:
            self.confirm_LineEdit.setVisible(False)
            self.groupBox.setVisible(True) # visible MailWindow
            

    def check_rightKey(self):
        try:
            if int(self.confirm_LineEdit.text()) == self.Confirm_key:
                print("correct key")
                self.confirm_LineEdit.setVisible(False)
                self.groupBox.setVisible(True) # visible MailWindow
            else:
                self.user_Message("Invalid Key", "rgb(255, 0, 0)")
        except:
            self.user_Message("Just Number Please", "rgb(255, 0, 0)", font= 10)




    def user_Message(self, msg, color, font = 12):
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
        self.wait.start()


    def clear_msg(self, check):
        if check:
            self.Label_Msg.setVisible(False)


    def forget_Pass(self, val):
        print("forget pass")



class send_Email(QtCore.QThread):
    Finished = QtCore.pyqtSignal(int)
    def __init__(self, window, receiver):
        self.receiver = receiver
        QtCore.QThread.__init__(self, parent= window)
    def run(self):
        confirm_key = signup.Send_Email(self.receiver)
        self.Finished.emit(confirm_key)


class wait_Toclear_thread(QtCore.QThread):
    isFinished = QtCore.pyqtSignal(bool)
    def __init__(self, window):
        QtCore.QThread.__init__(self, parent= window)
    def run(self):
        sleep(2.5)
        self.isFinished.emit(True)


class wait_Toconfirm(QtCore.QThread):
    Finished_1s = QtCore.pyqtSignal(int)
    Finished_Time = QtCore.pyqtSignal(bool)
    def __init__(self, window):
        QtCore.QThread.__init__(self, parent= window)
    
    def run(self):
        for i in range(30):
            sleep(1)
            self.Finished_1s.emit(30 - (i + 1))
        self.Finished_Time.emit(True)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = LoginWindow()
    w.show()
    sys.exit(app.exec_())
