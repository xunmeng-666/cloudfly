#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
from logging import handlers
from cloudfly_heketi.conf.conf import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def logger(LOG_INFO,LOG_LEVEL=logging.INFO,log_type='Heketi_Log'):
    logger = logging.getLogger(log_type)
    logger.setLevel(LOG_LEVEL)
    ch = logging.StreamHandler()
    fh = handlers.RotatingFileHandler(LOGS, maxBytes=4, backupCount=2)
    fh.setLevel(logging.WARNING)
    ch.setLevel(LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.info(LOG_INFO)
    logger.removeHandler(ch)
    return logger

