from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel

import ui


class Pointer(QWidget):
    FONT_STYLE = \
        """QLabel{{
            color: {color};
            font: bold 28px 微軟正黑體;
            background-color: {background_color};
            border: 1px solid {background_color};
            border-radius: 30px;
        }}
        QPushButton:pressed {{
            background-color: #D9D9D9;
            border-style: solid;
        }}
        """
    SIZE = (60, 60)

    button_exit_signal = pyqtSignal()

    def __init__(self, parent, label, start, **kwargs):
        super(Pointer, self).__init__()
        self.setParent(parent)

        # label
        self.label = QLabel(label, self)
        self.label.setStyleSheet(self.FONT_STYLE.format(
            color=ui.COLOR.WHITE,
            background_color=ui.COLOR.MAIN
        ))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setGeometry(*start, *self.SIZE)

