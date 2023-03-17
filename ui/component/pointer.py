from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton

import ui


class Pointer(QPushButton):
    FONT_STYLE = \
        """
        QPushButton {{
            color: {color};
            font: bold 28px 微軟正黑體;
            background-color: {background_color};
            border: 1px solid {background_color};
            border-radius: 30px;
        }}
        QPushButton:pressed {{
            background-color: {background_pressed_color};
            border: 1px solid {background_pressed_color};
        }}
        """
    SIZE = (60, 60)

    clicked_signal = pyqtSignal(int)

    def __init__(self, parent, label, start, **kwargs):
        super(Pointer, self).__init__(label, parent)
        self.kwargs = kwargs

        self.setStyleSheet(self.FONT_STYLE.format(
            color=ui.COLOR.WHITE,
            background_color=ui.COLOR.MAIN,
            background_pressed_color=ui.COLOR.MAIN_SUB
        ))

        self.setGeometry(*start, *self.SIZE)

        self.clicked.connect(lambda: self.clicked_signal.emit(self.kwargs.get('index', 0)))
