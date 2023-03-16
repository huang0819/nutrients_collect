from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QComboBox

import ui


class FormRow(QWidget):
    class InputType:
        INPUT = 0
        SELECT = 1

    FONT_STYLE = \
        """QLabel{{
            color: {color};
            font: {font_weight} {font_size}px 微軟正黑體;
        }}"""

    clicked = pyqtSignal(int)

    def __init__(self, parent, label, unit, index, input_type, **kwargs):
        super(FormRow, self).__init__()
        self.setParent(parent)
        self.index = index
        self.input_type = input_type

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Label
        self.label = QLabel(label, self)
        self.label.setStyleSheet(self.FONT_STYLE.format(font_weight='normal', color=ui.COLOR.MAIN, font_size=32))
        self.layout.addWidget(self.label, 0, 0)

        # Input
        self.selected = False

        if input_type == self.InputType.INPUT:
            self.input = Input(self, label)
            self.value = ''
        elif input_type == self.InputType.SELECT:
            self.input = Select(self, label, kwargs.get('options'))
            self.input.data_signal.connect(self.set_value)
            self.value = self.input.currentIndex()

        self.layout.addWidget(self.input, 1, 0)

        # Unit
        self.unit = QLabel(unit, self)
        self.unit.setStyleSheet(self.FONT_STYLE.format(font_weight='normal', color=ui.COLOR.MAIN, font_size=32))
        self.layout.addWidget(self.unit, 1, 1)

        self.setLayout(self.layout)

    def mousePressEvent(self, ev) -> None:
        self.clicked.emit(self.index)

    def set_selected(self, selected):
        font_weight = 'bold' if selected else 'normal'

        self.label.setStyleSheet(self.FONT_STYLE.format(font_weight=font_weight, color=ui.COLOR.MAIN, font_size=32))
        self.unit.setStyleSheet(self.FONT_STYLE.format(font_weight=font_weight, color=ui.COLOR.MAIN, font_size=32))
        self.input.set_selected(selected)

        self.selected = selected

    def set_value(self, value):
        self.value = value
        self.input.set_value(self.value)

    def get_value(self):
        if self.input_type == self.InputType.INPUT:
            try:
                return float(self.value)
            except:
                return 0.0
        elif self.input_type == self.InputType.SELECT:
            return self.value

    def reset(self):
        if self.input_type == self.InputType.INPUT:
            self.value = ''
        elif self.input_type == self.InputType.SELECT:
            self.value = 0

        self.input.set_value(self.value)
        self.set_selected(False)


class Input(QLabel):
    INPUT_STYLE = \
        """QLabel{{
            color: {color};
            font: {font_weight} {font_size}px 微軟正黑體;
            border: 1px solid {border_color};
            border-radius: 5px;
        }}"""

    def __init__(self, parent, label):
        super(Input, self).__init__(f'請輸入{label}', parent)
        self.default_text = f'請輸入{label}'

        self.setStyleSheet(self.INPUT_STYLE.format(font_weight='normal', color=ui.COLOR.GREY, font_size=28,
                                                   border_color=ui.COLOR.GREY))
        self.setMaximumWidth(250)
        self.setMinimumWidth(250)

    def set_selected(self, selected):
        color = ui.COLOR.BLACK if selected else ui.COLOR.GREY
        border_color = ui.COLOR.MAIN if selected else ui.COLOR.GREY

        self.setStyleSheet(
            self.INPUT_STYLE.format(font_weight='normal', color=color, font_size=28, border_color=border_color))

    def set_value(self, value):
        if value == '':
            self.setText(self.default_text)
        else:
            self.setText(value)


class Select(QComboBox):
    SELECT_STYLE = """
            QComboBox {{
                color: {color};
                font: {font_weight} {font_size}px 微軟正黑體;
                background-color: {background_color};
                border: 1px solid {border_color};
                border-radius: 5px;
                padding-left: 15px;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
            
                border-left-width: 1px;
                border-left-color: {border_color};
                border-left-style: solid; /* just a single line */
                border-top-right-radius: 3px; /* same radius as the QComboBox */
                border-bottom-right-radius: 3px;
            }}
            QComboBox::down-arrow {{
                image: url(resource/drop_down.png);
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                font: {font_weight} {font_size}px 微軟正黑體;
                color: {item_color};
                background-color: {background_color};
                border: 1px solid {border_color};
            }}
        """
    data_signal = pyqtSignal(int)

    def __init__(self, parent, label, options):
        super(Select, self).__init__()

        self.setParent(parent)
        self.options = options
        self.label = label

        self.set_options()
        self.currentIndexChanged.connect(self.data_signal.emit)

        self.style_dict = {
            'font_weight': 'normal',
            'color': ui.COLOR.BLACK,
            'font_size': 28,
            'background_color': ui.COLOR.WHITE,
            'border_color': ui.COLOR.BLACK,
            'item_color': ui.COLOR.BLACK,
        }

        self.setStyleSheet(self.SELECT_STYLE.format(**self.style_dict))

        self.setMaximumWidth(250)
        self.setMinimumWidth(250)

        self.setView(QtWidgets.QListView())

    def set_options(self):
        self.options = [f'請選擇{self.label}'] + self.options
        self.addItems(self.options)
        self.setCurrentIndex(0)

    def handler(self, index):
        self.data_signal.emit(index)

    def set_value(self, value):
        self.setCurrentIndex(value)

    def set_selected(self, selected):
        pass

    def reset(self):
        pass
