from datetime import datetime, timedelta

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QDate
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QDateEdit, QButtonGroup, QRadioButton, \
    QGraphicsDropShadowEffect

import ui


class DishSelect(QWidget):
    FONT_STYLE = \
        """QLabel{{
            color: {color};
            font: {font_weight} {font_size}px 微軟正黑體;
            background-color: {background_color};
        }}"""

    RADIO_STYLE = \
        """
        QRadioButton{{
            font: normal 28px 微軟正黑體;
        }}
        QRadioButton:hover {{
            color: {hover_color};
        }}
        QRadioButton::indicator {{
            margin-right: 20px;
            width: 26px;
            height: 26px;
        }}
        QRadioButton::indicator::unchecked {{
            image: url(resource/radio-button.png);
        }}
        QRadioButton::indicator:unchecked:hover {{
            image: url(resource/radio-button-hover.png);
        }}
        QRadioButton::indicator::checked {{
            image: url(resource/radio-button-checked.png);
        }}
        QRadioButton::indicator:checked:hover {{
            image: url(resource/radio-button-checked-hover.png);
        }}
        
        """

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

    DATE_BTN_STYLE = \
        """
            QPushButton{{
                image: url(resource/{type}.png);
                border: none;
                background-color: transparent;
            }}
            QPushButton:pressed {{
                image: url(resource/{type}_pressed.png);
            }}
        """

    close_signal = pyqtSignal(str)

    def __init__(self, parent, **kwargs):
        super().__init__()
        self.date = datetime.now()
        self.menus = {}

        self.setParent(parent)
        self.setGeometry(
            (ui.APP_WIDTH - 450) // 2,
            (ui.APP_HEIGHT - 650 - 150) // 2 - 40,
            450, 650
        )
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        self.setGraphicsEffect(shadow)

        self.background = QLabel('', self)
        self.background.setGeometry(0, 0, 450, 650)
        self.background.setStyleSheet(f"background-color: {ui.COLOR.WHITE}")

        # title
        self.title = QLabel('菜色名稱選擇', self)
        self.title.setStyleSheet(self.FONT_STYLE.format(
            color=ui.COLOR.WHITE,
            font_size='36',
            font_weight='bold',
            background_color=ui.COLOR.MAIN
        ))
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setGeometry(0, 0, 450, 60)

        # line
        self.line = QLabel('', self)
        self.line.setStyleSheet(f'background-color: {ui.COLOR.GREY}')
        self.line.setGeometry(20, 190, 410, 2)

        # Date
        self.date_label = QLabel('日期', self)
        self.date_label.setGeometry(50, 80, 64, 39)
        self.date_label.setStyleSheet(self.FONT_STYLE.format(
            color=ui.COLOR.MAIN,
            font_size='32',
            font_weight='bold',
            background_color=ui.COLOR.WHITE
        ))
        self.date_label.setAlignment(QtCore.Qt.AlignCenter)

        self.date_display = QLabel(self.date.strftime('%Y / %m / %d'), self)
        self.date_display.setGeometry(114, 127, 220, 50)
        self.date_display.setStyleSheet(self.FONT_STYLE.format(
            color=ui.COLOR.BLACK,
            font_size='32',
            font_weight='normal',
            background_color=ui.COLOR.WHITE
        ))
        self.date_display.setAlignment(QtCore.Qt.AlignCenter)

        self.btn_sub_date = QPushButton(self)
        self.btn_sub_date.setGeometry(62, 132, 40, 40)
        self.btn_sub_date.setStyleSheet(self.DATE_BTN_STYLE.format(type='previous'))
        self.btn_sub_date.clicked.connect(lambda: self.change_date(-1))

        self.btn_add_date = QPushButton(self)
        self.btn_add_date.setGeometry(346, 132, 40, 40)
        self.btn_add_date.setStyleSheet(self.DATE_BTN_STYLE.format(type='next'))
        self.btn_add_date.clicked.connect(lambda: self.change_date(1))

        # recipe name select
        self.food_label = QLabel('菜色名稱', self)
        self.food_label.setGeometry(50, 200, 128, 39)
        self.food_label.setStyleSheet(self.FONT_STYLE.format(
            color=ui.COLOR.MAIN,
            font_size='32',
            font_weight='bold',
            background_color=ui.COLOR.WHITE
        ))
        self.food_label.setAlignment(QtCore.Qt.AlignCenter)

        self.button_group = QButtonGroup(self)

        self.radio_buttons = list()
        for i in range(4):
            self.radio_buttons.append(QRadioButton(f'{i}', self))
            self.radio_buttons[i].setGeometry(50, 250 + (50 + 30) * i, 340, 50)
            self.radio_buttons[i].setStyleSheet(self.RADIO_STYLE.format(hover_color=ui.COLOR.MAIN))
            self.button_group.addButton(self.radio_buttons[i], i)

        # Button
        self.button = QPushButton('確認', self)
        self.button.setGeometry(175, 580, 100, 50)
        self.button.setStyleSheet(self.BTN_STYLE.format(color=ui.COLOR.BLACK))
        self.button.clicked.connect(self.close_handler)

        self.hide()

    def set_message(self, text, **kwargs):
        self.message.setText(text)
        self.message.setStyleSheet(self.FONT_STYLE.format(color=kwargs.get('color', ui.COLOR.BLACK), ))
        self.head.setStyleSheet(f"background-color: {kwargs.get('color', ui.COLOR.MAIN)}")

    def close_handler(self):
        self.hide()
        self.close_signal.emit(self.button_group.checkedButton().text())

    def change_date(self, day_delta):
        self.date = self.date + timedelta(days=day_delta)
        self.date_display.setText(self.date.strftime('%Y / %m / %d'))
        self.set_options()

    def get_date(self):
        return self.date

    def set_options(self):
        options = self.menus.get(self.date.strftime('%Y-%m-%d'), [{'dish_name': f'食譜{i + 1}'} for i in range(4)])

        for option, radio_button in zip(options, self.radio_buttons):
            radio_button.setText(option['dish_name'])
            radio_button.setChecked(False)
        self.radio_buttons[0].setChecked(True)

    def reset(self):
        self.radio_buttons[0].setChecked(True)

    def set_menu(self, data):
        self.menus = data
        self.set_options()
