from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic, QtCore, QtGui
import os
import csv
import SettingPart.Theme as Theme_module
import SettingPart.PlayBack as PlayBack
import SettingPart.Account as Account
from editPart.edit import edit_Tags
from userWinPart.confirm import confrimWin
from userWinPart.updatedatabaseWin import updatedatabaseWin as UDWin
from userWinPart.tagEditWin import tagEditWin
from PyQt5.QtWidgets import QTreeWidgetItem
import re


Form = uic.loadUiType(os.path.join(os.getcwd(), 'SettingPart/Setting.ui'))[0]


class SettingWindow(QMainWindow, Form):
    def __init__(self, Mediaplayer):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)
        self.MediaPlayer = Mediaplayer
        self.Account_changing = False

        # Theme Part
        self.palette = QtGui.QPalette()
        self.pushButton_Cancel.clicked.connect(self.Exit)
        self.pushButton_OK.clicked.connect(self.OK)
        self.comboBox_Theme.activated.connect(self._Theme)

        # To Connect Signals of custom Theme
        self.checkBox_Theme.stateChanged.connect(Theme_module.Classic_Theme)
        self.comboBox_Background.activated.connect(self.background_Theme)
        self.comboBox_Base.activated.connect(self.Base_Theme)
        self.comboBox_WindowsText.activated.connect(self.WindowsText_Theme)
        self.comboBox_Text.activated.connect(self.Text_Theme)
        self.comboBox_Button.activated.connect(
            self.Button_Theme)
        self.comboBox_ButtonText.activated.connect(
            self.ButtonText_Theme)
        self.comboBox_Slider.activated.connect(
            self.SliderTheme)
        self.scrollArea_Theme.setVisible(False)

        # Play Back Part
        self.horizontalSlider_Speed.setRange(0, 300)
        self.horizontalSlider_Speed.setValue(100)
        self.lineEdit_Speed.setText("1.00")
        self.label_Error_Range.setVisible(False)
        self.label_Error_Number.setVisible(False)

        self.horizontalSlider_Speed.valueChanged.connect(self.Play_Back_Slider)
        self.lineEdit_Speed.textChanged.connect(self.Play_Back_LineEdit)

        # Text Part
        self.comboBox_Font.activated.connect(self.Font_Change)

        # Account part
        self.label_NotMatch.setVisible(False)
        self.label_PassLong.setVisible(False)
        self.label_OldPass.setVisible(False)
        self.label_Wait.setVisible(False)
        self.label_finish.setVisible(False)
        self.lineEdit_CurrentPass.textChanged.connect(self.CurrentPass)
        self.lineEdit_ReNewpass.editingFinished.connect(self.ReNewpass)
        self.lineEdit_NewPass.editingFinished.connect(self.NewPass)
        self.lineEdit_ReNewpass.textChanged.connect(
            lambda: self.label_NotMatch.setVisible(False))

        self.pushButton_Delete_Acc.clicked.connect(self.DelAcc)

        
        # Edit tag part
        self.comboBox_Tag.activated.connect(self.ListWidget_Tag_Edit)
        self.Edit_tag_Listwidget.setHeaderLabels(['Tag', 'Time'])
        self.pushButton_Edit.clicked.connect(self.edit_Tag) 
        self.pushButton_Delete.clicked.connect(self.del_Tag)
        self.pushButton_Add.clicked.connect(self.add_Tag)
        self.pushButton_Upload.clicked.connect(self.uploadTags)
        self.pushButton_Download.clicked.connect(self.downloadTags)
        self.prev_text = None
        self.tagEditWin = None
        self.UDWin = UDWin(self.MediaPlayer)
        self.confirmWin = None


        # close event
        self.closeEvent = self.Close
        self.connection_part = None



    # Connect signals to Theme module in Theme.py
    def _Theme(self, index):
        Theme_module._Theme(self, index)

    def background_Theme(self, index):
        Theme_module.background_Theme(self, index)

    def Base_Theme(self, index):
        Theme_module.Base_Theme(self, index)

    def WindowsText_Theme(self, index):
        Theme_module.WindowsText_Theme(self, index)

    def Text_Theme(self, index):
        Theme_module.Text_Theme(self, index)

    def Button_Theme(self, index):
        Theme_module.Button_Theme(self, index)

    def ButtonText_Theme(self, index):
        Theme_module.ButtonText_Theme(self, index)

    def SliderTheme(self, index):
        Theme_module.SliderTheme(self, index)
    # Connect signals to Account module in Account.py

    def CurrentPass(self, val):
        Account.CurrentPass(self, val)

    def ReNewpass(self):
        Account.ReNewpass(self)

    def NewPass(self):
        Account.NewPass(self)


    def pass_change_result(self,val):
        ###To show password has been changed or not 
        if val:
            self.label_finish.setVisible(True)
        else:
            self.label_Error.setVisible(True)

    def DelAcc(self):
        Account.DeleteAcc(self,self.MediaPlayer)
    

    # Edit tag part
    # *************************
    
    # updata tags part of settingpart's tag listwidget
    def ListWidget_Tag_Edit(self, index):
        videoName = (list(self.MediaPlayer.PlaylistW.Files.keys())[index].split("."))[0] # get videoname
        self.MediaPlayer.set_TagonListwidget( # update listwidgets
            videoName, Setting_Tags= True, Media_Tags= False)



    # edit tag part
    def edit_Tag(self):
        self.pushButton_Edit.setEnabled(False)
        self.pushButton_Add.setEnabled(False)
        try:
            self.prev_text = [self.Edit_tag_Listwidget.currentItem().text(0), self.Edit_tag_Listwidget.currentItem().text(1)]
            self.tagEditWin = tagEditWin( # show open tag win to apply our change
                self.MediaPlayer, Text= self.prev_text[0], Time= self.prev_text[1])
            self.tagEditWin.show()
        except Exception as e:
            print(e)
    

    # delete part for deleting selected item in tree widget
    def del_Tag(self):
        try: # handle error of not selected item
            item = [self.Edit_tag_Listwidget.currentItem().text(0), self.Edit_tag_Listwidget.currentItem().text(1)]
            session = self.comboBox_Tag.currentText().split(".")[0]
            if session in self.MediaPlayer.allTag:
                # show window to get accept from user
                self.confirmWin = confrimWin(self.MediaPlayer, session= session 
                    , Text= f"are you sure to delete ({item[0]}) tag", tagPartText= item, Title= "delete tag")
                self.confirmWin.show()
            else:
                print("error in finding session -> delete")
        except Exception as e:
            print(e)

    
    # add tag 
    def add_Tag(self):
        self.pushButton_Edit.setEnabled(False)
        self.pushButton_Add.setEnabled(False)
        self.tagEditWin = tagEditWin( # show add tag win that user enter tag information
            self.MediaPlayer, Title= "Add tag")
        self.tagEditWin.show()


    # upload tag to online database
    def uploadTags(self):
        if not self.UDWin.isVisible():
            self.UDWin = UDWin(self.MediaPlayer) # window of upload tag
            self.UDWin.user_Msg(
                text= "Please wait to update list of your tag", stylesheet= "color:rgb(0, 170, 0);")
            self.UDWin.show()


    # download tag from online database
    def downloadTags(self):
        if not self.UDWin.isVisible():
            self.UDWin = UDWin(self.MediaPlayer, "Download Database") # window of download tag
            self.UDWin.user_Msg(
                text= "Please wait to update list of your tag", stylesheet= "color:rgb(0, 170, 0);")
            self.UDWin.show()

            
    # Edit part ended 
    # **********

    # close event to close child win and stop runnig thread
    def Close(self, val):
        self.UDWin.close()
        if self.tagEditWin:
            self.tagEditWin.close()
        if self.confirmWin:
            self.confirmWin.close()
        if self.connection_part:
            self.connection_part.stop()

        



    def Font_Change(self, val):
        print(val)
        # if int(val)==0:
        #     print(self.font())
        #     self.setFont(QtGui.QFont('Arial',2))
        #     self.MediaPlayer.setFont(QtGui.QFont('Arial',2))
        #     self.Tab.setFont(QtGui.QFont('Arial',2))
        #     self.MediaPlayer.actionFullScreen.setFont(QtGui.QFont('Arial',2))

    def Play_Back_LineEdit(self, val):
        PlayBack.Play_Back_LineEdit(self, val)

    def Play_Back_Slider(self, val):
        self.lineEdit_Speed.setText(str(val/100))

    def OK(self):
        Theme_module.saveANDexit(self)
        if self.Account_changing:
            self.label_finish.setVisible(False)


            if not self.label_NotMatch.isVisible():
                if not self.label_PassLong.isVisible():
                    if Account.read_Pass('Pass') == self.lineEdit_CurrentPass.text():
                        self.label_OldPass.setVisible(False)
                        self.label_Error.setVisible(False)
                        self.pushButton_OK.setEnabled(False)
                        self.pushButton_Cancel.setEnabled(False)
                        self.label_Wait.setVisible(True)
                        self.connection_part =Account.Apply_Thread(self)
                        self.connection_part.start()
                        self.connection_part.pass_changed.connect(self.pass_change_result)
                        self.label_Wait.setVisible(False)           
                        self.pushButton_OK.setEnabled(True)
                        self.pushButton_Cancel.setEnabled(True)
                    else:
                        self.Tab.setCurrentIndex(3)
                        self.label_OldPass.setVisible(True)
        else:
            self.close()



    def Exit(self):
        #Reset to factory!!
        Theme_module.Theme_apply(self)
        self.label_finish.setVisible(False)
        self.label_NotMatch.setVisible(False)
        self.label_PassLong.setVisible(False)
        self.label_OldPass.setVisible(False)
        self.label_Wait.setVisible(False)
        self.label_Error.setVisible(False)
        self.lineEdit_CurrentPass.clear()
        self.lineEdit_NewPass.clear()
        self.lineEdit_ReNewpass.clear()
        self.close()
