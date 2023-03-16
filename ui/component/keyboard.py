from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton

import ui


class KeyBoardButton(QPushButton):
    BTN_STYLE = \
        """
        QPushButton{{
            color: {color};
            font: {font_weight} {font_size}px 微軟正黑體;
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
    clicked_signal = pyqtSignal(dict)

    def __init__(self, text, size, command, data, **kwargs):
        super(KeyBoardButton, self).__init__()

        self.command = command
        self.data = data
        self.setText(text)
        self.setStyleSheet(self.BTN_STYLE.format(
            color=kwargs.get('color', ui.COLOR.BLACK),
            font_weight=kwargs.get('font_weight', 'normal'),
            font_size=kwargs.get('font_weight', '36'),
        ))
        self.setMinimumSize(*size)
        self.clicked.connect(self.btn_handler)

    def btn_handler(self):
        self.clicked_signal.emit({
            'cmd': self.command,
            'data': self.data
        })


class KeyBoard(QWidget):
    output_signal = pyqtSignal(str)
    save_signal = pyqtSignal()

    COMMANDS_NUM = 0
    COMMANDS_DOT = 1
    COMMANDS_DEL = 2
    COMMANDS_SAVE = 3

    def __init__(self, parent):
        super(KeyBoard, self).__init__()
        self.setParent(parent)
        self.__output = ''

        # layout
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(30)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        # buttons
        self.btn_nums = []
        for i in range(10):
            self.btn_nums.append(KeyBoardButton(str(i), (120, 120), self.COMMANDS_NUM, data=i))
            self.btn_nums[i].clicked_signal.connect(self.command_handler)

            if i == 0:
                self.grid_layout.addWidget(self.btn_nums[i], 3, 0, 1, 1)
            else:
                self.grid_layout.addWidget(self.btn_nums[i], (i - 1) // 3, (i - 1) % 3, 1, 1)

        self.btn_dot = KeyBoardButton('.', (120, 120), self.COMMANDS_DOT, data=None)
        self.btn_dot.clicked_signal.connect(self.command_handler)
        self.grid_layout.addWidget(self.btn_dot, 3, 1, 1, 1)

        self.btn_del = KeyBoardButton('Del', (120, 120), self.COMMANDS_DEL, data=None)
        self.btn_del.clicked_signal.connect(self.command_handler)
        self.grid_layout.addWidget(self.btn_del, 3, 2, 1, 1)

        self.btn_save = KeyBoardButton('儲存', (420, 120), self.COMMANDS_SAVE, data=None)
        self.btn_save.clicked_signal.connect(self.command_handler)
        self.grid_layout.addWidget(self.btn_save, 4, 0, 3, 1)

    def command_handler(self, obj):
        if obj['cmd'] == self.COMMANDS_NUM:
            if len(self.__output) == 1 and self.__output[-1] == '0':
                self.__output = str(obj['data'])
            else:
                self.__output += str(obj['data'])
        elif obj['cmd'] == self.COMMANDS_DOT:
            if self.__output.find('.') == -1:
                self.__output += '.'
        elif obj['cmd'] == self.COMMANDS_DEL:
            if len(self.__output) > 0:
                self.__output = self.__output[:-1]
        elif obj['cmd'] == self.COMMANDS_SAVE:
            self.save_signal.emit()

        self.output_signal.emit(self.__output)

    def set_output(self, value):
        self.__output = value

    def set_enable(self, enable):
        self.btn_dot.setEnabled(enable)
        self.btn_del.setEnabled(enable)
        self.btn_save.setEnabled(enable)

        for btn in self.btn_nums:
            btn.setEnabled(enable)
