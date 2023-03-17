from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QStackedLayout

import ui
from ui.page.collect_page import CollectPage
from ui.page.message_page import MessagePage


class StackedWidget(QWidget):
    save_signal = pyqtSignal(object)

    def __init__(self, parent, **kwargs):
        super(StackedWidget, self).__init__()
        self.kwargs = kwargs

        self.setParent(parent)
        self.setGeometry(0, 150, ui.APP_WIDTH, ui.APP_HEIGHT - 150)

        # Loading page
        self.loading_page = MessagePage(text=ui.Message.LOADING, font_size=48, wait_time=0)
        # Error page
        self.error_page = MessagePage(text=ui.Message.CAMERA_ERR, font_size=48, wait_time=0, color=ui.COLOR.RED)
        # Collect Page
        self.collect_page = CollectPage()
        self.collect_page.save_signal.connect(self.save_signal.emit)

        # Stacked layout
        self.stacked_layout = QStackedLayout()
        self.setLayout(self.stacked_layout)

        self.stacked_layout.addWidget(self.loading_page)
        self.stacked_layout.addWidget(self.error_page)
        self.stacked_layout.addWidget(self.collect_page)

        self.stacked_layout.setCurrentIndex(ui.UI_PAGE_NAME.LOADING)

    def change_page(self, page, **kwargs):
        if page == ui.UI_PAGE_NAME.ERROR:
            self.error_page.set_message(kwargs.get('err_msg'))

        if self.get_current_page() != ui.UI_PAGE_NAME.ERROR:
            self.stacked_layout.setCurrentIndex(page)

    def get_current_page(self):
        return self.stacked_layout.currentIndex()

    def set_collect_page_dishes_option(self, data):
        self.collect_page.set_dish_selector_option(data)
