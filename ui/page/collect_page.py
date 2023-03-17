from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

import ui
from ui.component.dish_select import DishSelect
from ui.component.form import FormRow
from ui.component.keyboard import KeyBoard
from ui.component.message_widget import MessageWidget
from ui.component.pointer import Pointer


class CollectPage(QWidget):
    IMG_SIZE = (int(640 * 1.5), int(480 * 1.5))
    save_signal = pyqtSignal(object)

    def __init__(self, **kwargs):
        super(CollectPage, self).__init__()

        top = (ui.APP_HEIGHT - 150 - self.IMG_SIZE[1]) // 2

        # set image area
        self.image_view = QLabel(self)
        self.image_view.setScaledContents(True)
        self.image_view.setGeometry(QtCore.QRect(50, top, *self.IMG_SIZE))

        self.pointers = list()
        for i in range(1, 5):
            x = 240 + (i - 1) % 2 * 470
            y = 30 + ((i - 1) // 2) * (95 + self.IMG_SIZE[1])
            self.pointers.append(Pointer(self, f'{i}', (x, y), index=i))
            self.pointers[-1].clicked_signal.connect(self.pointer_click_handler)

        # form area
        self.selected_form_index = None
        self.form_data = [
            {'attr': 'area', 'label': '餐盤區域', 'unit': '', 'value': None, 'input_type': FormRow.InputType.AREA_SELECT,
             'options': [str(x) for x in range(1, 5)]},
            {'attr': 'name', 'label': '菜色名稱', 'unit': '', 'value': None, 'input_type': FormRow.InputType.DISH_SELECT},
            {'attr': 'calorie', 'label': '熱量', 'unit': '大卡', 'value': None, 'input_type': FormRow.InputType.INPUT},
            {'attr': 'protein', 'label': '蛋白質', 'unit': '公克', 'value': None, 'input_type': FormRow.InputType.INPUT},
            {'attr': 'fat', 'label': '脂肪', 'unit': '公克', 'value': None, 'input_type': FormRow.InputType.INPUT},
            {'attr': 'carbohydrate', 'label': '碳水化合物', 'unit': '公克', 'value': None,
             'input_type': FormRow.InputType.INPUT}
        ]

        self.forms = list()
        for i, form in enumerate(self.form_data):
            self.forms.append(FormRow(self, index=i, **form))
            self.forms[-1].setGeometry(QtCore.QRect(100 + self.IMG_SIZE[0], top + (36 + 90) * i, 325, 90))
            self.forms[-1].clicked.connect(self.select_handler)

        # keyboard
        self.key_board = KeyBoard(self)
        self.key_board.setGeometry(QtCore.QRect(150 + self.IMG_SIZE[0] + 325, top, 420, 720))
        self.key_board.output_signal.connect(self.input_handler)
        self.key_board.save_signal.connect(self.save_handler)

        # message window
        self.message_window = MessageWidget(self)
        self.message_window.close_signal.connect(self.close_message_handler)

        # dish select
        self.dish_select = DishSelect(self, options=[f'apple {x}' for x in range(1, 5)])
        self.dish_select.close_signal.connect(self.close_dish_select_handler)

    def show_image(self, img):
        len_y, len_x, _ = img.shape
        img = QImage(img.data, len_x, len_y, QImage.Format_RGB888)
        self.image_view.setPixmap(QPixmap.fromImage(img))

    def select_handler(self, index):
        self.selected_form_index = index
        for i, f in enumerate(self.forms):
            f.set_selected(i == index)

        if self.form_data[index]['input_type'] == FormRow.InputType.DISH_SELECT:
            self.key_board.setEnabled(False)
            self.dish_select.show()
        elif self.form_data[index]['input_type'] == FormRow.InputType.INPUT:
            self.key_board.set_output(str(self.forms[index].value))

    def input_handler(self, output):
        if self.selected_form_index is not None and \
                self.form_data[self.selected_form_index]['input_type'] == FormRow.InputType.INPUT:
            self.forms[self.selected_form_index].set_value(output)

    def save_handler(self):
        self.key_board.setEnabled(False)
        self.selected_form_index = None

        invalids = []
        for i, form in enumerate(self.form_data):
            form['value'] = self.forms[i].get_value()
            self.forms[i].set_selected(False)
            if (form['input_type'] == FormRow.InputType.AREA_SELECT and form['value'] == 0) or \
                    (form['input_type'] == FormRow.InputType.DISH_SELECT and form['value'] == ''):
                invalids.append(form['label'])

        if invalids:
            self.show_message(text=f"請選擇{'、'.join(invalids)}", color=ui.COLOR.RED)
        else:
            self.show_message(text='儲存成功', color=ui.COLOR.GREEN)
            self.dish_select.reset()
            for i, form in enumerate(self.forms):
                form.reset()

            data = dict((f['attr'], f['value']) for f in self.form_data)
            self.save_signal.emit(data)

    def show_message(self, text, **kwargs):
        self.message_window.set_message(text, **kwargs)
        self.message_window.show()

    def close_message_handler(self):
        self.key_board.setEnabled(True)

    def close_dish_select_handler(self, dish_name):
        for i, form in enumerate(self.form_data):
            if form['input_type'] == FormRow.InputType.DISH_SELECT:
                self.forms[i].set_value(dish_name)

        self.key_board.setEnabled(True)

    def pointer_click_handler(self, index):
        if self.selected_form_index is not None and \
                self.form_data[self.selected_form_index]['input_type'] == FormRow.InputType.AREA_SELECT:
            self.forms[self.selected_form_index].set_value(str(index))
