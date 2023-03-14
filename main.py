import sys

from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow
from utils.logger import create_logger

def main():
    logger = create_logger(logger_name=__name__)

    logger.info('*** Start application {CODE_VERSION} ***')

    app = QApplication(sys.argv)

    window = MainWindow()

    app.exec()


if __name__ == '__main__':
    main()
