from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton

import ui


class CollectPage(QWidget):
    def __init__(self, **kwargs):
        super(CollectPage, self).__init__()

        top = (ui.APP_HEIGHT - 150 - int(480 * 1.5)) // 2

        # set image area
        self.image_view = QLabel(self)
        self.image_view.setScaledContents(True)
        # self.image_view.setMinimumSize(640, 480)

        self.image_view.setPixmap(QPixmap.fromImage(QImage('resource/photo.png')))

        # self.image_view.setGeometry(QtCore.QRect(0, 130, int(640 * 1.5), int(480 * 1.5)))

        self.image_view.setGeometry(QtCore.QRect(50, top, int(480 * 1.5), int(480 * 1.5)))

        # form area
        self.selected_form_index = None
        self.form_data = [
            {'attr': 'calorie', 'name': '熱量', 'unit': '大卡', 'value': 0},
            {'attr': 'protein', 'name': '蛋白質', 'unit': '公克', 'value': 0},
            {'attr': 'fat', 'name': '脂肪', 'unit': '公克', 'value': 0},
            {'attr': 'carbohydrate', 'name': '碳水化合物', 'unit': '公克', 'value': 0}
        ]

        self.forms = list()
        for i, form in enumerate(self.form_data):
            self.forms.append(FormRow(self, form['name'], form['unit'], i))
            self.forms[-1].setGeometry(QtCore.QRect(100 + int(640 * 1.5), top + (40 + 90) * i, 325, 90))
            self.forms[-1].clicked.connect(self.select_handler)

        # keyboard
        self.key_board = KeyBoard(self)
        self.key_board.setGeometry(QtCore.QRect(150 + int(640 * 1.5) + 325, top, 420, 720))
        self.key_board.output_signal.connect(self.input_handler)
        self.key_board.save_signal.connect(self.save_handler)

    def select_handler(self, index):
        for i, f in enumerate(self.forms):
            f.set_selected(i == index)

        self.selected_form_index = index
        self.key_board.clear_output()

    def input_handler(self, output):
        if self.selected_form_index is not None:
            self.forms[self.selected_form_index].set_value(output)

    def save_handler(self):
        print('save')


class FormRow(QWidget):
    FONT_STYLE = \
        """QLabel{{
            color: {color};
            font: {font_weight} {font_size}px 微軟正黑體;
        }}"""

    INPUT_STYLE = \
        """QLabel{{
            color: {color};
            font: {font_weight} {font_size}px 微軟正黑體;
            border: 1px solid {border_color};
            border-radius: 5px;
        }}"""

    clicked = pyqtSignal(int)

    def __init__(self, parent, label, unit, index, **kwargs):
        super(FormRow, self).__init__()
        self.setParent(parent)
        self.index = index

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Label
        self.label = QLabel(label, self)
        self.label.setStyleSheet(self.FONT_STYLE.format(font_weight='normal', color=ui.COLOR.MAIN, font_size=32))
        self.layout.addWidget(self.label, 0, 0)

        # Input
        self.value = None
        self.selected = False
        self.input = QLabel(f'請輸入{label}', self)
        self.input.setStyleSheet(
            self.INPUT_STYLE.format(font_weight='normal', color=ui.COLOR.GREY, font_size=28,
                                    border_color=ui.COLOR.GREY))
        self.input.setMaximumWidth(250)
        self.input.setMinimumWidth(250)
        self.layout.addWidget(self.input, 1, 0)

        # Unit
        self.unit = QLabel(unit, self)
        self.unit.setStyleSheet(self.FONT_STYLE.format(font_weight='normal', color=ui.COLOR.MAIN, font_size=32))
        self.layout.addWidget(self.unit, 1, 1)

        self.setLayout(self.layout)

    def mousePressEvent(self, ev) -> None:
        self.clicked.emit(self.index)

    def set_selected(self, selected):
        color = ui.COLOR.BLACK if selected else ui.COLOR.GREY
        self.input.setStyleSheet(
            self.INPUT_STYLE.format(font_weight='normal', color=color, font_size=28, border_color=color))
        self.selected = selected

    def set_value(self, value):
        if not value:
            value = '0'

        self.value = value
        self.input.setText(value)


class KeyBoardButton(QPushButton):
    BTN_STYLE = \
        """
        QPushButton{{
            color: {color};
            font: {font_weight} {font_size}px 微軟正黑體;
            border-radius: 5px;
            border-style: outset;
            border-width: 2px;
            border-color: #D9D9D9;
            background-color: #F3F3F3;
        }}
        QPushButton:pressed {{
            background-color: #D9D9D9;
            border-style: inset;
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

        # buttons
        self.btn_nums = []
        for i in range(10):
            self.btn_nums.append(KeyBoardButton(str(i), (120, 120), self.COMMANDS_NUM, data=i))
            self.btn_nums[i].clicked_signal.connect(self.command_handler)

            if i == 0:
                self.grid_layout.addWidget(self.btn_nums[i], 3, 0, 1, 1)
            else:
                self.grid_layout.addWidget(self.btn_nums[i], (i - 1) // 3, (i - 1) % 3, 1, 1)

        self.bnt_dot = KeyBoardButton('.', (120, 120), self.COMMANDS_DOT, data=None)
        self.bnt_dot.clicked_signal.connect(self.command_handler)
        self.grid_layout.addWidget(self.bnt_dot, 3, 1, 1, 1)

        self.bnt_del = KeyBoardButton('Del', (120, 120), self.COMMANDS_DEL, data=None)
        self.bnt_del.clicked_signal.connect(self.command_handler)
        self.grid_layout.addWidget(self.bnt_del, 3, 2, 1, 1)

        self.bnt_calibrate = KeyBoardButton('儲存', (420, 120), self.COMMANDS_SAVE, data=None)
        self.bnt_calibrate.clicked_signal.connect(self.command_handler)
        self.grid_layout.addWidget(self.bnt_calibrate, 4, 0, 3, 1)

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

    def clear_output(self):
        self.__output = ''
