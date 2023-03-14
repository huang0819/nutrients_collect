import logging
import datetime
import os


def create_logger(logger_name):
    logger = logging.getLogger(name=logger_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')

    # Stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    # File handler
    log_file_path = os.path.join('logs', '{}_log.log'.format(datetime.datetime.now().strftime("%Y%m%d")))
    os.makedirs('logs', exist_ok=True)
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger
