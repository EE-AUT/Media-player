from PyQt5.QtWidgets import QLineEdit


# our custome line dit with special css format and handle size
class LineEdit(QLineEdit):
    def __init__(self, parent):
        QLineEdit.__init__(self, parent=parent)
        styleSheet_LineEdits = ("""
            QLineEdit{ 
                background-color: #b5e2ff;
                border: 2px solid gray;
                border-radius: 4px;
                padding: 0 8px;
                selection-background-color: darkgray;
                font-size: 14px;
            }
        """)
        self.setStyleSheet(styleSheet_LineEdits)
        self.resize(250, 30)
        self.move(parent.size().width() / 2 - 125,
                  parent.size().height()/2 - 15)
