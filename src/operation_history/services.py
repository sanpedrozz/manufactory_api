# /scr/operation_history/service.py

from datetime import datetime


def add_operation_history(time: datetime, *data):
    pattern = ('place', 'program', 'data')
    message = dict([(key, value) for key, value in zip(pattern, data)])
    message.update({'time': time})
    return message


def error_report(time: datetime):
    pattern = ('place', 'program', 'data')
    data = ('error', 'error', 'error')
    message = dict([(key, value) for key, value in zip(pattern, data)])
    message.update({'time': time})
    return message
