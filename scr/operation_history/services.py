# /scr/operation_history/service.py

import os
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
logs_dir = os.path.join(grandparent_dir, "logs")
os.makedirs(logs_dir, exist_ok=True)

log_file_path = os.path.join(logs_dir, "report.log")

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] -> %(message)s', filename=log_file_path)
logger = logging.getLogger()


def add_operation_history(*data):
    pattern = ('place', 'program', 'data')
    message = ' '.join([f'{key}: {value} | ' for key, value in zip(pattern, data)])
    logger.debug(message)


def error_report():
    logger.debug('Ошибка запроса')
