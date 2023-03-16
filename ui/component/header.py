from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

import ui


class Header(QWidget):
    FONT_STYLE = \
        """QLabel{{
            color: {color};
            font: bold {font_size}px 微軟正黑體;
        }}"""
    BTN_SIZE = (80, 80)

    button_exit_signal = pyqtSignal()

    def __init__(self, parent, title_text, **kwargs):
        super(Header, self).__init__()
        self.setParent(parent)
        self.setGeometry(0, 0, ui.APP_WIDTH, 150)
        self.setStyleSheet(f"background-color: {kwargs.get('background_color', ui.COLOR.MAIN)}")

        # layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # title
        self.title = QLabel(title_text, self)
        self.title.setStyleSheet(self.FONT_STYLE.format(
            color=kwargs.get('background_color', ui.COLOR.WHITE),
            font_size=kwargs.get('font_size', '64'), )
        )
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # exit btn
        self.exit_button = QPushButton('', self)
        self.exit_button.resize(*self.BTN_SIZE)
        self.exit_button.setStyleSheet("""
                    QPushButton{{
                        background-color: transparent; 
                        border: none; 
                        image: url(resource/{button_type}.png)
                    }}
                    QPushButton:pressed {{
                        background-color: transparent; 
                        border: none; 
                        image: url(resource/{button_type}_pressed.png)
                    }}
                """.format(button_type='logout'))
        self.exit_button.setGeometry(
            QtCore.QRect(
                ui.APP_WIDTH - self.BTN_SIZE[0] - 30,
                (150 - self.BTN_SIZE[1]) // 2,
                *self.BTN_SIZE
            ))

        self.exit_button.clicked.connect(self.button_exit_signal)
        # self.exit_button.hide()
