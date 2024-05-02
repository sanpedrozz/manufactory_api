#   /scr/data_logger/service.py

import os
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_dir, "report.log")

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] -> %(message)s', filename=log_file_path)
logger = logging.getLogger()


def get_data(*data):
    pattern = ('place', 'program', 'data')
    message = ' '.join([f'{key}: {value} | ' for key, value in zip(pattern, data)])
    logger.debug(message)


def error_report():
    logger.debug('Ошибка запроса')
