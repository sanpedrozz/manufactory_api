#   /scr/data_logger/service.py

import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] ->\n%(message)s', filename='report.txt')
logger = logging.getLogger()


def get_data(*data):
    pattern = ('place', 'program', 'data')
    messege = ''
    for number, values in enumerate(data):
        messege += f'{pattern[number]} : {values}\n'
    logger.debug(messege)


def error_report():
    logger.debug('Ошибка запроса')
