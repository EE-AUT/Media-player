
def Play_Back_LineEdit(SettingWindow,val):
    try:
        if val:
            if float(val):
                SettingWindow.label_Error_Number.setVisible(False)

                if float(val) >= 0 and float(val) <= 3:
                    SettingWindow.label_Error_Range.setVisible(False)
                    SettingWindow.horizontalSlider_Speed.setValue(float(val)*100)
                    if SettingWindow.MediaPlayer.player.isAvailable():
                        SettingWindow.MediaPlayer.player.setPlaybackRate(float(val))
                else:
                    SettingWindow.label_Error_Range.setVisible(True)

    except:
        SettingWindow.label_Error_Number.setVisible(True)