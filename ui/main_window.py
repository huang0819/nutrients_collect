from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMainWindow

import ui
from ui.header import Header
from ui.stacked_widget import StackedWidget
from utils.logger import create_logger
from worker.camera_worker import DepthCameraWorker


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
        # self.depth_camera_worker = DepthCameraWorker()
        # if self.depth_camera_worker.depth_camera is not None:
        #     self.is_depth_camera_ok = True
        #     self.depth_camera_worker.signals.data.connect(self.stacked_widget.show_image)
        #     self.thread_pool.start(self.depth_camera_worker)
        # else:
        #     self.is_depth_camera_ok = False

        self.show()

    def exit_handler(self):
        # self.depth_camera_worker.set_stop(True)
        # self.depth_camera_worker.depth_camera.pipeline.stop()
        self.logger.info('*** Close application ***\n\n')
        self.close()
