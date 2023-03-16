from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMainWindow

import ui
from ui.component.header import Header
from ui.component.stacked_widget import StackedWidget
from utils.logger import create_logger
from worker.camera_worker import DepthCameraWorker
from worker.worker import Worker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create logger
        self.logger = create_logger(logger_name=__name__)

        # Setting
        self.setWindowTitle(ui.APP_NAME)
        self.resize(ui.APP_WIDTH, ui.APP_HEIGHT)
        self.setStyleSheet(f"background-color: {ui.COLOR.WHITE}")

        # Create header
        self.header = Header(self, '飲食分析資料收集工具')
        self.header.setParent(self)
        self.header.button_exit_signal.connect(self.exit_handler)

        # Create stacked widget
        self.stacked_widget = StackedWidget(self)

        self.thread_pool = QThreadPool()

        # Thread of initialize module
        self.is_depth_camera_ok = False
        self.init_worker = Worker(self.setup_sensors)
        self.init_worker.signals.finished.connect(self.finish_setup_sensors)
        self.init_worker.setAutoDelete(True)
        self.thread_pool.start(self.init_worker)

        self.showFullScreen()

    def exit_handler(self):
        if self.is_depth_camera_ok:
            self.depth_camera_worker.set_stop(True)
            self.depth_camera_worker.depth_camera.pipeline.stop()

        self.logger.info('*** Close application ***\n\n')
        self.close()

    def setup_sensors(self):
        self.depth_camera_worker = DepthCameraWorker()
        if self.depth_camera_worker.depth_camera is not None:
            self.is_depth_camera_ok = True
            self.depth_camera_worker.signals.data.connect(self.stacked_widget.collect_page.show_image)
            self.thread_pool.start(self.depth_camera_worker)

    def finish_setup_sensors(self):
        if self.is_depth_camera_ok:
            self.stacked_widget.change_page(ui.UI_PAGE_NAME.COLLECT)
            self.logger.info(f"[MAIN] depth camera setup success")
        else:
            self.stacked_widget.change_page(ui.UI_PAGE_NAME.ERROR)
            self.logger.info(f"[MAIN] depth camera setup failed")
