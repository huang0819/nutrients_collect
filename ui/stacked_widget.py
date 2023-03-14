from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QStackedLayout

import ui
from ui.collect_page import CollectPage
from ui.message_page import MessagePage


class StackedWidget(QWidget):
    def __init__(self, parent, **kwargs):
        super(StackedWidget, self).__init__()
        self.kwargs = kwargs

        self.setParent(parent)
        self.setGeometry(0, 150, ui.APP_WIDTH, ui.APP_HEIGHT - 150)

        # Loading page
        self.loading_page = MessagePage(text='處理中，請稍候。', font_size=48, wait_time=0)
        self.loading_page.close_signal.connect(lambda: self.change_page(ui.UI_PAGE_NAME.COLLECT))
        self.loading_page.start_timer()
        # Collect Page
        self.collect_page = CollectPage()

        # Stacked layout
        self.stacked_layout = QStackedLayout()
        self.setLayout(self.stacked_layout)

        self.stacked_layout.addWidget(self.loading_page)
        self.stacked_layout.addWidget(self.collect_page)

        self.stacked_layout.setCurrentIndex(ui.UI_PAGE_NAME.LOADING)

    def change_page(self, page):
        self.stacked_layout.setCurrentIndex(page)

    def show_image(self, img):
        len_y, len_x, _ = img.shape
        img = QImage(img.data, len_x, len_y, QImage.Format_RGB888)
        self.collect_page.image_view.setPixmap(QPixmap.fromImage(img))
