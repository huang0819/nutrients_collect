from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton

import ui


class MessageWidget(QWidget):
    FONT_STYLE = \
        """QLabel{{
            color: {color};
            font: normal 32px 微軟正黑體;
        }}"""

    BTN_STYLE = \
        """
        QPushButton{{
            color: {color};
            font: normal 28px 微軟正黑體;
            border-radius: 15px;
            border-style: solid;
            border-width: 2px;
            border-color: #D9D9D9;
            background-color: #F3F3F3;
        }}
        QPushButton:pressed {{
            background-color: #D9D9D9;
            border-style: solid;
        }}
        """

    close_signal = pyqtSignal()

    def __init__(self, parent, **kwargs):
        super().__init__()
        self.setParent(parent)
        self.resize(ui.MESSAGE_WIDTH, ui.MESSAGE_HEIGHT)
        self.setGeometry(
            (ui.APP_WIDTH - ui.MESSAGE_WIDTH) // 2,
            (ui.APP_HEIGHT - ui.MESSAGE_HEIGHT - 150) // 2,
            ui.MESSAGE_WIDTH, ui.MESSAGE_HEIGHT
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.background = QLabel('', self)
        self.background.setGeometry(0, 0, ui.MESSAGE_WIDTH, ui.MESSAGE_HEIGHT)
        self.background.setStyleSheet(f"background-color: {ui.COLOR.WHITE}")

        # Head
        self.head = QLabel('', self)
        self.head.setGeometry(0, 0, ui.MESSAGE_WIDTH, 50)
        self.head.setStyleSheet(f"background-color: {ui.COLOR.MAIN}")

        # Message
        self.message = QLabel('', self)
        self.message.setGeometry(0, 81 + 50, ui.MESSAGE_WIDTH, 39)
        self.message.setStyleSheet(self.FONT_STYLE.format(color=kwargs.get('color', ui.COLOR.BLACK), ))
        self.message.setAlignment(QtCore.Qt.AlignCenter)

        # Button
        self.button = QPushButton('返回', self)
        self.button.setGeometry((ui.MESSAGE_WIDTH - 100) // 2, 81 + 50 + 39 + 48, 100, 50)
        self.button.setStyleSheet(self.BTN_STYLE.format(color=ui.COLOR.BLACK))
        self.button.clicked.connect(self.close_handler)

        self.hide()

    def set_message(self, text, **kwargs):
        self.message.setText(text)
        self.message.setStyleSheet(self.FONT_STYLE.format(color=kwargs.get('color', ui.COLOR.BLACK), ))
        self.head.setStyleSheet(f"background-color: {kwargs.get('color', ui.COLOR.MAIN)}")

    def close_handler(self):
        self.hide()
        self.close_signal.emit()
