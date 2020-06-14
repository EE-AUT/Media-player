from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QLineEdit
from PyQt5 import QtGui
import sys
import os
from PyQt5 import uic, QtCore
from tag import *
from time import sleep

a = tag(1)
Form = uic.loadUiType(os.path.join(os.getcwd(), "search_part.ui"))[0]

class IntroWindow(QMainWindow, Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)

        # initial decleration
        self.search_Thread = None
        self.sch_listWidget = QListWidget(self)
        self.search_lineEdit = QLineEdit(self)
        self.width = self.size().width()
        self.height = self.size().height()

        #initial condition
        self.sch_listWidget.setVisible(False)
        self.search_lineEdit.setVisible(False)



        # Events
        self.search_icon.mouseReleaseEvent = self.sch_icon_Event
        QMainWindow.mouseReleaseEvent = self.MainWindow_Event
        self.resizeEvent = self.main_size_Change
        self.sch_listWidget.itemDoubleClicked.connect(self.item_Event)
        self.search_lineEdit.textChanged.connect(self.search_Tag)



    def main_size_Change(self, val):
        self.width = self.size().width()
        self.height = self.size().height()

        self.sch_listWidget.resize(int((200 / 800) * self.width), int((200 / 600) * self.height))
        self.sch_listWidget.move(int(self.width - (200 / 800) * self.width), self.search_lineEdit.size().height())
        
        self.search_lineEdit.resize(int((200 / 800) * self.width), int((20 / 600) * self.height))
        self.search_lineEdit.move(int(self.width - (200 / 800) * self.width), 0)


    # Search icon events
    def sch_icon_Event(self, type):

        self.search_icon.setVisible(False)

        # create QLineEdit
        self.search_lineEdit.resize(int((200 / 800) * self.width), int((20 / 600) * self.height))
        self.search_lineEdit.move(int(self.width - (200 / 800) * self.width), 0)
        self.search_lineEdit.setVisible(True)




    def item_Event(self, item):
        print(item.text())
        

    def MainWindow_Event(self, type):

        self.search_icon.setVisible(True)

        self.search_lineEdit.setText("")
        self.search_lineEdit.setVisible(False)

        self.sch_listWidget.setVisible(False)
        self.sch_listWidget.clear()

        
   


    def search_Tag(self, val):

        # create QListWidget
        self.sch_listWidget.resize(int((200 / 800) * self.width), int((200 / 600) * self.height))
        self.sch_listWidget.move(int(self.width - (200 / 800) * self.width), self.search_lineEdit.size().height())
        self.sch_listWidget.setVisible(True)
        

        # start search thread
        self.search_Thread = search_thread(self, val)
        self.search_Thread.update_schTag.connect(self.update_Tags)
        self.search_Thread.start()



    def update_Tags(self, tagsList):
        self.sch_listWidget.clear()

        for key in tagsList:
            self.sch_listWidget.addItem(key)
            
        self.search_Thread = None


    
# thread for searching in tags
class search_thread(QtCore.QThread):
    update_schTag = QtCore.pyqtSignal(list)
    def __init__(self, window, val):
        self.val = val
        QtCore.QThread.__init__(self, parent= window)

    def run(self):
        sch_Tags = a.find_Closest_to(self.val)
        self.update_schTag.emit(sch_Tags)



if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = IntroWindow()

    w.show()
    app.exec_()

