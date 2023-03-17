from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout

import ui


class FormRow(QWidget):
    class InputType:
        INPUT = 0
        AREA_SELECT = 1
        DISH_SELECT = 2

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
        assert input_type in [self.InputType.INPUT, self.InputType.AREA_SELECT, self.InputType.DISH_SELECT], 'input_type error '
        self.input_type = input_type

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Label
        self.label = QLabel(label, self)
        self.label.setStyleSheet(self.FONT_STYLE.format(font_weight='normal', color=ui.COLOR.MAIN, font_size=32))
        self.layout.addWidget(self.label, 0, 0)

        # Input
        self.selected = False

        self.input = Input(self, label)
        self.value = ''

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
        elif self.input_type == self.InputType.DISH_SELECT:
            return self.value
        elif self.input_type == self.InputType.AREA_SELECT:
            try:
                return int(self.value)
            except:
                return 0

    def reset(self):
        self.value = ''

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
