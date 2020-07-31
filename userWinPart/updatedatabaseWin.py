from PyQt5.QtWidgets import QApplication, QMainWindow
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
        self.MediaPlayer = parent
        self.getWsheets = getWsheets(self)
        self.getWsheets.Wsheets_Ready.connect(self.wsh_isReady)
        self.getWsheets.start()


    def wsh_isReady(self, wsheets, accept):
        if accept:
            print("yes")
            print(wsheets[0].title)
            # self.wsh_Combo.addItems(wsheets)
        else:
            print("error occured")








class getWsheets(QtCore.QThread):
    Wsheets_Ready = QtCore.pyqtSignal(list, bool)

    def __init__(self, window):
        QtCore.QThread.__init__(self, parent=window)

    def run(self):
        result = []
        user = open("LoginPart/User.csv").read().split(",")[0]
        result = UD.get_allworksheet("test")
        self.Wsheets_Ready.emit(result[0], result[1])

    def stop(self):
        self.terminate()
        self.wait()