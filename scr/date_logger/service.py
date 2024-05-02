#   /scr/data_logger/service.py

import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] -> %(message)s', filename='report.log')
logger = logging.getLogger()


def get_data(*data):
    pattern = ('place', 'program', 'data')
    message = ' '.join([f'{key}: {value} | ' for key, value in zip(pattern, data)])
    logger.debug(message)


def error_report():
    logger.debug('Ошибка запроса')
