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
        self.loading_page = MessagePage(text='處理中，請稍候。', font_size=48, wait_time=0)
        # Error page
        self.error_page = MessagePage(text='無法使用深度攝影機，請重新確認後再開啟應用程式。', font_size=48, wait_time=0, color=ui.COLOR.RED)
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

    def change_page(self, page):
        self.stacked_layout.setCurrentIndex(page)
