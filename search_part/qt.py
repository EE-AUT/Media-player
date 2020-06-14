from PyQt5.QtWidgets import QApplication, QMainWindow
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

        # initial condition
        self.search_lineEdit.setVisible(False)
        self.sch_listWidget.setVisible(False)
        self.search_Thread = None


        # Events
        self.search_icon.mouseReleaseEvent = self.sch_icon_Event
        QMainWindow.mouseReleaseEvent = self.MainWindow_Event
        self.search_lineEdit.mouseReleaseEvent = self.line_edit_Event
        self.search_lineEdit.textChanged.connect(self.search_Tag)
        self.sch_listWidget.itemDoubleClicked.connect(self.item_Event)


    # Search icon events
    def sch_icon_Event(self, type):
        self.search_lineEdit.setVisible(True)
        self.search_icon.setVisible(False)

    def item_Event(self, item):
        print(item.text())
        

    def MainWindow_Event(self, type):
        self.search_lineEdit.setVisible(False)
        self.sch_listWidget.setVisible(False)
        self.search_icon.setVisible(True)
        

    def line_edit_Event(self, type):
        self.sch_listWidget.setVisible(True)

    def search_Tag(self, val):
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

