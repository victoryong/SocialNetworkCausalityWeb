# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 10:17:00 2017

@author: Victor Xie

"""
import logging


def get_console_logger(logger_name='', format_str='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    """
    Init a logger of console and return its handle for invoking.
    :param logger_name: Name of logger. If is none, a root logger will be return.
    :param format_str: Logs will be sort according to this format.
    :return: The handle of logger.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    cs = logging.StreamHandler()
    cs.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format_str)
    cs.setFormatter(formatter)
    logger.addHandler(cs)
    return logger
