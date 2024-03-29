from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

import ui


class MessagePage(QWidget):
    close_signal = pyqtSignal()
    FONT_STYLE = """QLabel{{
        color: {color};
        font: {font_size}px 微軟正黑體;
    }}"""

    def __init__(self, text=None, image_path=None, wait_time=2000, **kwargs):
        super(MessagePage, self).__init__()

        # set layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)

        # create image
        if image_path is not None:
            self.image_view = QLabel('', self)
            self.image_view.setMinimumSize(200, 200)
            self.image_view.setPixmap(QPixmap.fromImage(QImage(image_path)))
            self.layout.addWidget(self.image_view)

            if text is not None:
                self.image_view.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
            else:
                self.image_view.setAlignment(QtCore.Qt.AlignCenter)

        # create message
        if text is not None:
            self.message = QLabel(text, self)
            self.message.setStyleSheet(self.FONT_STYLE.format(color=kwargs.get('color', ui.COLOR.MAIN), font_size=kwargs.get('font_size', '48')))
            self.layout.addWidget(self.message)

            if image_path is not None:
                self.message.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
            else:
                self.message.setAlignment(QtCore.Qt.AlignCenter)

        # close timer
        self.timer = QTimer()
        self.timer.setInterval(wait_time)
        self.timer.timeout.connect(self.close_handler)

    def start_timer(self):
        self.timer.start()

    def close_handler(self):
        self.close_signal.emit()
        self.timer.stop()

    def set_message(self, text):
        self.message.setText(text)
