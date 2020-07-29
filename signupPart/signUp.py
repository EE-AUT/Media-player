from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog, QLabel, QLineEdit
import os
import sys
import signupPart.sendEmail as sendEmail
from PyQt5 import uic, QtCore, QtGui
from time import sleep
from signupPart.CustomLineEdit import LineEdit as CustomLineEdit
import Database.Database as get_Database


Form = uic.loadUiType(os.path.join(os.getcwd(), 'signupPart/signUp.ui'))[0]


class signUpWindow(QMainWindow, Form):
    def __init__(self, parent= None):
        Form.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Login")


        self.FirstName.setPlaceholderText("First Name")
        self.LastName.setPlaceholderText("Last Name")
        self.PassLineEdit.setPlaceholderText("Password")
        self.Pass_repeat.setPlaceholderText("Repeat Password")
        self.Email_LineEdit.setPlaceholderText("Email address")
        self.StudentNo_LineEdit.setPlaceholderText("Student Number")

        self.FName = None
        self.LName = None
        self.UPass = ""
        self.StudentNo = None
        self.Email = None
        self.isEqual_pass = None
        self.error_No = True
        self.Confirm_key = None



        # Thread
        self.wait_To_clearMsg = wait_Toclear_thread(self)
        self.wait_To_clearMsg.isFinished.connect(self.clear_Msg)
        self.send_Email_Thread = None
        self.wait_Toconfirm = wait_Toconfirm(self)
        self.wait_Toconfirm.Finished_1s.connect(self.Update_Time)
        self.wait_Toconfirm.Finished_Time.connect(self.Time_Ended)
        self.check_Mail = None
        self.Confirm_thread = None


        # Visibles
        self.NotEqual_error.setVisible(False)
        self.Label_Msg.setVisible(False)

        # Enabled
        self.submit_Button.setEnabled(False)
        

        # LineEdit
        self.confirm_LineEdit = CustomLineEdit(self)
        self.confirm_LineEdit.returnPressed.connect(self.check_rightKey)
        self.confirm_LineEdit.setVisible(False)
        self.confirm_LineEdit.setPlaceholderText("Enter Key here: 180' remain")



        self.FirstName.editingFinished.connect(self.saveFName)
        self.LastName.editingFinished.connect(self.saveLName)
        self.PassLineEdit.editingFinished.connect(self.saveUpass)
        self.Pass_repeat.editingFinished.connect(self.check_equal)
        self.StudentNo_LineEdit.editingFinished.connect(self.saveSNo)
        self.Email_LineEdit.textChanged.connect(self.saveEmail)



        self.PassLineEdit.setEchoMode(QLineEdit.Password)
        self.Pass_repeat.setEchoMode(QLineEdit.Password)

        self.submit_Button.clicked.connect(self.submit_Email)
        self.clear_Button.clicked.connect(self.clearall)









    def saveFName(self):
        self.FName = self.FirstName.text()

    def saveLName(self):
        self.LName = self.LastName.text()


    def saveUpass(self):
        self.UPass = self.PassLineEdit.text()


    def saveSNo(self):
        try:
            self.StudentNo = int(self.StudentNo_LineEdit.text())
            self.error_No = False

        except:
            self.error_No = True
            self.user_Message("Enter Valid Student number", "rgb(255, 0, 0)", font= 10)


    def saveEmail(self, val):
        try:
            self.Email = val
            if self.Email_LineEdit.text() != "":
                self.submit_Button.setEnabled(True)
            else:
                self.submit_Button.setEnabled(False)

        except:
            self.submit_Button.setEnabled(False)


    def check_equal(self):
        if self.UPass == self.Pass_repeat.text():
            self.NotEqual_error.setVisible(False)
            self.isEqual_pass = True
        else :
            self.isEqual_pass = False
            self.NotEqual_error.setVisible(True)

        


    def clear_Msg(self, ckeck_Key):
        if ckeck_Key:
            self.Label_Msg.setVisible(False)




    def submit_Email(self):
        if self.FName != "" and self.LName != "" and self.UPass != "" and self.Email != "":
            if self.isEqual_pass and self.StudentNo_LineEdit.text() != "" and not self.error_No:
                if len(self.PassLineEdit.text()) >= 8:
                    self.user_Message("please wait ...", "rgb(0, 170, 0)", wait= False)
                    self.submit_Button.setEnabled(False)
                    self._check_Exist()
                else:
                    self.user_Message("Password must be more than 8 character", "rgb(255, 0, 0)", font= 8)    
            else:
                self.user_Message("Please fill all Boxes with true value", "rgb(255, 0, 0)", font= 8)
        else:
            self.user_Message("Please fill all Boxes with true value", "rgb(255, 0, 0)", font= 8)


    

    def _check_Exist(self):
        self.check_Mail = checkEmail_Exist(self, self.Email)
        self.check_Mail.check_Exist.connect(self._check_Exist_Key)
        if self.check_Mail:
            self.check_Mail.start()

    def _check_Exist_Key(self, key):
        if key == 0:
            self.SendMail()
        if key == 1:
            self.submit_Button.setEnabled(True)
            self.user_Message("there is a user with this Email", "rgb(255, 0, 0)", font= 10)
        if key == 2:
            self.submit_Button.setEnabled(True)
            self.user_Message("Connection failed", "rgb(255, 0, 0)") 






    def clearall(self):
        self.FirstName.clear()
        self.LastName.clear()
        self.PassLineEdit.clear()
        self.Pass_repeat.clear()
        self.StudentNo_LineEdit.clear()
        self.Email_LineEdit.clear()


    def SendMail(self):
        try:
            self.send_Email_Thread = send_Email(self, receiver= self.Email)
            self.send_Email_Thread.Finished.connect(self.check_verify)
            if self.send_Email_Thread:
                self.send_Email_Thread.start()
        except:
            self.submit_Button.setEnabled(False)
            self.user_Message("Invalid Email", "rgb(255, 0, 0)")
        


    def check_verify(self, key):
        self.submit_Button.setEnabled(True)
        if key:
            self.Confirm_key = key
            self.user_Message("message sent", "rgb(0, 170, 0)")
            self.setVisibleAll(False)
            if self.wait_Toconfirm:
                self.wait_Toconfirm.start()
            
        else:
            self.user_Message("Connection Faild, or invalid Email address", "rgb(255, 0, 0)", font=8)


    def setVisibleAll(self, key):
        self.confirm_LineEdit.setVisible(not(key))
        self.FirstName.setVisible(key)
        self.LastName.setVisible(key)
        self.PassLineEdit.setVisible(key)
        self.Pass_repeat.setVisible(key)
        self.StudentNo_LineEdit.setVisible(key)
        self.Email_LineEdit.setVisible(key)
        self.submit_Button.setVisible(key)
        self.clear_Button.setVisible(key)


    def Update_Time(self, val):
        self.confirm_LineEdit.setPlaceholderText(f"Enter Key here: {val}' remain")

    def Time_Ended(self, key):
        if key:
            self.confirm_LineEdit.clear()
            self.setVisibleAll(True)

    def check_rightKey(self):
        try:
            if int(self.confirm_LineEdit.text()) == int(self.Confirm_key):
                print("correct key")
                self.user_Message("Please wait ...", "rgb(0, 170, 0)", wait= False)
                self.Confirmation()
            else:
                self.user_Message("Invalid Key", "rgb(255, 0, 0)")
        except Exception as e:
            print(e)
            self.user_Message("Just Number Please", "rgb(255, 0, 0)", font= 10)

        
        
    def Confirmation(self):
        user_Info = [str(self.Email), str(self.StudentNo), "#" + str(self.UPass)
                    , str(self.FName), str(self.LName)]
        self.Confirm_thread = Confimation_Thread(self, user= user_Info)
        self.Confirm_thread.Confirm_Complete.connect(self.signUp_Ended)
        if self.Confirm_thread:
            self.Confirm_thread.start()


    def signUp_Ended(self, key):
        if key:
            self.user_Message("Register has been done", "rgb(0, 170, 0)", font= 10)
            self.setVisibleAll(True)
        else:
            self.user_Message("Connection fails, Register has been faild", "rgb(255, 0, 0)", font= 10)
            self.setVisibleAll(True)





    def user_Message(self, msg, color, font = 12, wait= True):
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
        if wait:
            if self.wait_To_clearMsg:
                self.wait_To_clearMsg.start()



        



    
    
class wait_Toclear_thread(QtCore.QThread):
    isFinished = QtCore.pyqtSignal(bool)
    def __init__(self, window):
        QtCore.QThread.__init__(self, parent= window)
    def run(self):
        sleep(2.5)
        self.isFinished.emit(True)

    def stop(self):
        self.terminate()
        self.wait()

class send_Email(QtCore.QThread):
    Finished = QtCore.pyqtSignal(int)
    def __init__(self, window, receiver):
        self.receiver = receiver
        QtCore.QThread.__init__(self, parent= window)
    def run(self):
        confirm_key = sendEmail.Send_Email(self.receiver)
        self.Finished.emit(confirm_key)

    def stop(self):
        self.terminate()
        self.wait()


class wait_Toconfirm(QtCore.QThread):
    Finished_1s = QtCore.pyqtSignal(int)
    Finished_Time = QtCore.pyqtSignal(bool)
    def __init__(self, window):
        QtCore.QThread.__init__(self, parent= window)
    
    def run(self):
        for i in range(180): # time for clearing confirmation lineEdit
            sleep(1)
            self.Finished_1s.emit(180 - (i + 1))
        self.Finished_Time.emit(True)

    def stop(self):
        self.terminate()
        self.wait()


class checkEmail_Exist(QtCore.QThread):

    check_Exist = QtCore.pyqtSignal(int)

    def __init__(self, window, Email):
        self.Email = Email
        QtCore.QThread.__init__(self, parent= window)


    def run(self):
        check = get_Database.exist_Email(self.Email)
        self.check_Exist.emit(check)

    def stop(self):
        self.terminate()
        self.wait()


class Confimation_Thread(QtCore.QThread):
    Confirm_Complete = QtCore.pyqtSignal(bool)
    def __init__(self, window, user):
        self.user = user
        QtCore.QThread.__init__(self, parent= window)
        
    def run(self):
        check = get_Database.add_User(self.user)
        self.Confirm_Complete.emit(check)

    def stop(self):
        self.terminate()
        self.wait()











if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = signUpWindow()
    w.show()
    sys.exit(app.exec_())
