from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import uic, QtCore, QtGui
import os
from editPart import timeconvert as tc
from editPart.edit import edit_Tags
import Database.updateDatabase as UD







Form = uic.loadUiType(os.path.join(os.getcwd(), 'userWinPart/updatedatabaseWin.ui'))[0]

class updatedatabaseWin(QMainWindow, Form):
    def __init__(self, parent= None, Title= "Upload Database"):
        Form.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Title = Title
        self.setWindowTitle(Title)
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.MediaPlayer = parent

        # threads
        self.getWsheets = getWsheets(self) # get worksheets of user
        self.getWsheets.Wsheets_Ready.connect(self.wsh_isReady)
        self.getWsheets.start()
        self.UD_Thread = None
        self.DD_Thread = None

        # ********

        # initial condition Upload part
        if self.Title == "Upload Database":
            self.LineEdit.setEnabled(False)
            self.Browse_Button.setVisible(False)
            self.wsheets =None
            self.new_Button.clicked.connect(self.new_Wsh)
            self.wsh_Combo_Global.setVisible(False)
            self.label_Global.setVisible(False)
            self.Ok_Button.clicked.connect(self.OkClicked_Upload)

        # initial condition Download part
        if self.Title == "Download Database":
            self.Browse_Button.setVisible(True)
            self.new_Button.setVisible(False)
            self.Browse_Button.clicked.connect(self.select_Csv)
            self.Ok_Button.clicked.connect(self.OkClicked_Download)
            self.save_tag_Path = None

        # event
        self.Ok_Button.setEnabled(False)
        self.closeEvent = self.Close
        self.Cancel_Button.clicked.connect(self.Cancel)


    # worksheets and they result ready
    def wsh_isReady(self, wsheets, accept, Gworksheets, gAccept):
        self.wsheets = wsheets
        self.Ok_Button.setEnabled(True)
        self.label_Msg.setVisible(False)
        if accept:
            self.wsh_Combo.addItems(wsheets) # update worksheets in combo box
        else:
            self.user_Msg( # connection failed
                "Connection Failed or Failed in user Tag", "color:rgb(255, 0, 0)")

        if self.Title == "Download Database":
            if gAccept:
                self.wsh_Combo_Global.addItems(Gworksheets) #show global worksheets in download part
            else:
                self.user_Msg(
                    "Connection Failed", "color:rgb(255, 0, 0)") # connection failed

    def new_Wsh(self): # enter new worksheet name to create new one
        if self.new_Button.isChecked():
            self.LineEdit.setEnabled(True)
            self.LineEdit.setPlaceholderText("Enter tag file name")
            self.wsh_Combo.setEnabled(False)
        else:
            self.LineEdit.setPlaceholderText("Enter Tag file path")
            self.LineEdit.setEnabled(False)
            self.LineEdit.setPlaceholderText("")
            self.LineEdit.clear()
            self.wsh_Combo.setEnabled(True)

    # ok clicked and hancle updateand download part
    def OkClicked_Upload(self):
        self.label_Msg.setVisible(False)
        user = open("LoginPart/User.csv").read().split(",")[0]
        if self.new_Button.isChecked():
            tagname = self.LineEdit.text()
            if not tagname == "":
                if not tagname in self.wsheets:
                    self.Ok_Button.setEnabled(False)
                    self.upload(user, tagname, self.MediaPlayer.tag_Path)
                else:
                    self.user_Msg(
                        "there is tag with this name", "color:rgb(255, 0, 0)")
            else:
                self.user_Msg(
                    "please fill tag name", "color:rgb(255, 0, 0)")
        else:
            if self.wsh_Combo.currentIndex():
                self.Ok_Button.setEnabled(False)
                self.upload(user, self.wsh_Combo.currentText(), self.MediaPlayer.tag_Path)
            else:
                self.user_Msg(
                    "select one of tags or create new one", "color:rgb(255, 0, 0)")
                

    # running thread for upload data to database
    def upload(self, user, wsheetname, filepath):
        if filepath:
            file_format = (filepath.split("/")[-1]).split(".")[-1]
            if file_format == "csv":
                # creating and running thread
                self.UD_Thread = uploadDatabse(self, user, wsheetname, filepath)
                self.UD_Thread.upload_Result.connect(self.upload_Result)
                self.UD_Thread.start()
                self.user_Msg("please wait ...", "color:rgb(0, 170, 0)")
            else:
                # handle user incorrect work
                self.user_Msg("you can only upload csv file not other format", "color:rgb(255, 0, 0)")
            
        else:
            # handle user incorrect work
            self.user_Msg(
                "first select a tag in media and try this again", "color:rgb(255, 0, 0)")

    # upload result
    def upload_Result(self, key, Wsh):
        self.Ok_Button.setEnabled(True)
        self.label_Msg.setVisible(False)
        if key:
            # upload completed
            self.user_Msg("It's Done", "color:rgb(0, 170, 0)")
            self.wsh_Combo.addItem(Wsh)
        else:
            # connetion failed
            self.user_Msg("Connection Failed", "color:rgb(255, 0, 0)")

    # select csv file to write downloaded database there
    def select_Csv(self):
        save_tag_Path, _ = QFileDialog.getOpenFileName(
            self, "Select Tag to save tags Tag", directory=os.path.join(os.getcwd(), 'Tags'), filter='*.csv')
        if save_tag_Path:
            self.LineEdit.setText(save_tag_Path)

    # handle download 
    def OkClicked_Download(self):
        self.label_Msg.setVisible(False)
        tagpath = self.LineEdit.text()
        try:
            if os.path.exists(tagpath):
                # handle user incorrect work
                if self.wsh_Combo.currentIndex() and self.wsh_Combo_Global.currentIndex():
                    self.user_Msg(
                        "you cant choose two tags instantly", "color:rgb(255, 0, 0)")
                elif self.wsh_Combo.currentIndex() and (not self.wsh_Combo_Global.currentIndex()):
                    self.Ok_Button.setEnabled(False)
                    self.download() 
                elif (not self.wsh_Combo.currentIndex()) and self.wsh_Combo_Global.currentIndex():
                    self.Ok_Button.setEnabled(False)
                    self.download(Global = True)
                else:
                    # handle user incorrect work
                    self.user_Msg(
                        "please select one of tags to download", "color:rgb(255, 0, 0)")
            else:
                # handle user incorrect work
                self.user_Msg(
                    "please select currect file", "color:rgb(255, 0, 0)")
        except Exception as e:
            print(e)


    # download data using thread
    def download(self, Global = False):
        if not Global: # download from gloals or not
            user = user = open("LoginPart/User.csv").read().split(",")[0]
            wsheets = self.wsh_Combo.currentText()
        else:
            user = "ap.mediaplayer@gmail.com"
            wsheets = self.wsh_Combo_Global.currentText()
        self.user_Msg("please wait ...", "color:rgb(0, 170, 0)")
        # running thread
        self.DD_Thread = downloadDatabse(self, user, wsheets, self.LineEdit.text())
        self.DD_Thread.download_Result.connect(self.Download_Result)
        self.DD_Thread.start()

    # download result 
    def Download_Result(self, key):
        self.Ok_Button.setEnabled(True)
        if key:
            # Done
            self.user_Msg("It's Done", "color:rgb(0, 170, 0)")
        else:
            # Connection Failed
            self.user_Msg("Connection Failed", "color:rgb(255, 0, 0)")


    # cancel button and close self window
    def Cancel(self):
        self.close()

    # stop thread while runnig
    def Close(self, val):
        self.getWsheets.stop()
        if self.UD_Thread:
            self.UD_Thread.stop()
        if self.DD_Thread:
            self.DD_Thread.stop()


    # user message label situation
    def user_Msg(self, text, stylesheet):
        self.label_Msg.setVisible(True)
        self.label_Msg.setText(text)
        self.label_Msg.setStyleSheet(stylesheet)
        







# thread of get worksheets
class getWsheets(QtCore.QThread):
    Wsheets_Ready = QtCore.pyqtSignal(list, bool, list, bool)

    def __init__(self, window):
        QtCore.QThread.__init__(self, parent=window)

    def run(self):
        result = []
        worksheets = []
        Globalworksheet = []
        user = open("LoginPart/User.csv").read().split(",")[0]
        result = UD.get_allworksheet(user)
        for item in result[0]:
            worksheets.append(item.title) # user worksheets
        for item in result[2]:
            Globalworksheet.append(item.title) # global worksheets
        if len(worksheets):
            worksheets.pop(0) 
        if len(Globalworksheet):
            Globalworksheet.pop(0)
        self.Wsheets_Ready.emit(worksheets, result[1], Globalworksheet, result[3])

    def stop(self): # stop thread
        self.terminate()
        self.wait()



# thread for upload database using UpdateDatabase mudole
class uploadDatabse(QtCore.QThread):
    upload_Result = QtCore.pyqtSignal(bool, str)

    def __init__(self, window, user= None, wsheetname= None, filepath= None):
        QtCore.QThread.__init__(self, parent=window)
        self.user = user
        self.wsheetname = wsheetname
        self.filepath = filepath

    def run(self):
        result = UD.upload_Database(self.user, self.wsheetname, self.filepath)
        self.upload_Result.emit(result, self.wsheetname)


    def stop(self):
        self.terminate()
        self.wait()

# thread for download database using UpdateDatabase mudole
class downloadDatabse(QtCore.QThread):
    download_Result = QtCore.pyqtSignal(bool)

    def __init__(self, window, user= None, wsheetname= None, filepath= None):
        QtCore.QThread.__init__(self, parent=window)
        self.user = user
        self.wsheetname = wsheetname
        self.filepath = filepath

    def run(self):
        result = UD.download_Database(self.user, self.wsheetname, self.filepath)
        self.download_Result.emit(result)


    def stop(self):
        self.terminate()
        self.wait()