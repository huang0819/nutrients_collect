import sys

from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow
from utils.logger import create_logger
import utils

def main():
    logger = create_logger(logger_name=__name__)

    logger.info(f'*** Start application {utils.config.app_version} ***')

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()
