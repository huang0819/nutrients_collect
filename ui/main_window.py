import json
import os
from datetime import datetime

from PyQt5.QtCore import QThreadPool, QTimer
from PyQt5.QtWidgets import QMainWindow

import ui
from ui.component.header import Header
from ui.component.stacked_widget import StackedWidget
from utils.api import Api
from utils.logger import create_logger
from worker.camera_worker import DepthCameraWorker
from worker.worker import Worker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create logger
        self.logger = create_logger(logger_name=__name__)

        self.save_folder = 'data'
        if not os.path.isdir(self.save_folder):
            os.mkdir(self.save_folder)

        self.thread_pool = QThreadPool()
        self.api = Api()

        # Setting
        self.setWindowTitle(ui.APP_NAME)
        self.resize(ui.APP_WIDTH, ui.APP_HEIGHT)
        self.setStyleSheet(f"background-color: {ui.COLOR.WHITE}")
        self.get_dishes()

        # Create header
        self.header = Header(self, '飲食分析資料收集工具')
        self.header.setParent(self)
        self.header.button_exit_signal.connect(self.exit_handler)

        # Create stacked widget
        self.stacked_widget = StackedWidget(self)
        self.stacked_widget.save_signal.connect(self.save_handler)

        # Thread of initialize module
        self.is_depth_camera_ok = False
        self.init_worker = Worker(self.setup_sensors)
        self.init_worker.signals.finished.connect(self.finish_setup_sensors)
        self.init_worker.setAutoDelete(True)
        self.thread_pool.start(self.init_worker)

        # Wait 1 second for saving file
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.save_file)

        self.data = None
        self.file_name = None
        self.file_path = None
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
            self.logger.info(f"depth camera setup success")
        else:
            self.stacked_widget.change_page(ui.UI_PAGE_NAME.ERROR, err_msg=ui.Message.CAMERA_ERR)
            self.logger.info(f"depth camera setup failed")

    def save_handler(self, data):
        self.data = data
        self.stacked_widget.change_page(ui.UI_PAGE_NAME.LOADING)
        self.timer.start()

    def save_file(self):
        self.timer.stop()

        self.file_name = '{}'.format(datetime.now().strftime("%Y%m%d%H%M%S"))
        file_dir = os.path.join(self.save_folder, self.data['meal_date'])
        self.file_path = os.path.join(file_dir, f'{self.file_name}.npz')

        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)

        self.logger.info(f'save file: {self.file_name}')

        _worker = Worker(lambda: self.depth_camera_worker.depth_camera.save_file(self.file_path))
        _worker.signals.finished.connect(self.upload_file)
        _worker.setAutoDelete(True)
        self.thread_pool.start(_worker)

    def upload_file(self):
        data = {
            'payload': self.data,
            'file_path': self.file_path,
            'file_name': self.file_name,
        }

        _worker = Worker(self.api.upload_data, data=data)
        _worker.setAutoDelete(True)
        _worker.signals.result.connect(self.upload_response_handler)
        _worker.signals.error.connect(self.upload_error_handler)
        _worker.signals.finished.connect(lambda: self.stacked_widget.change_page(ui.UI_PAGE_NAME.COLLECT))
        self.thread_pool.start(_worker)

    def upload_response_handler(self, res):
        self.save_json({
            self.file_name: {
                **self.data,
                'is_upload': 1 if res['status_code'] == 200 else 0
            }
        })

        self.data = None
        self.file_name = None
        self.file_path = None

    def upload_error_handler(self, err):
        self.save_json({
            self.file_name: {
                **self.data,
                'is_upload': 0
            }
        })

        self.data = None
        self.file_name = None
        self.file_path = None

    def save_json(self, data):
        json_path = os.path.join(self.save_folder, self.data['meal_date'], 'data.json')
        try:
            if os.path.isfile(json_path):
                with open(json_path, encoding='utf8') as json_file:
                    json_data = json.load(json_file)
            else:
                json_data = {}

            json_data.update(data)

            with open(json_path, 'w') as outfile:
                json.dump(json_data, outfile, indent=4, ensure_ascii=False)

            self.logger.info('save json success')
        except:
            self.logger.error('save json failed', exc_info=True)

    def get_dishes(self):
        _worker = Worker(self.api.get_dishes, year=2023, month=3)
        _worker.signals.result.connect(self.set_dish_options)
        _worker.setAutoDelete(True)
        self.thread_pool.start(_worker)

    def set_dish_options(self, data):
        if data['status_code'] != 200:
            self.stacked_widget.change_page(ui.UI_PAGE_NAME.ERROR, err_msg=ui.Message.NET_ERR)
        else:
            self.stacked_widget.set_collect_page_dishes_option(data['data'])
