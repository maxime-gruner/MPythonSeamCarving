# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler
import time
from ctypes import *

PROJECT_PATH = os.getcwd()
IMAGE_PATH = PROJECT_PATH + "/images/"

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        logging.info('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap

def config_log():
    # logging setup change of log every 5MB for a maximum of 10 different log files
    logging_level = logging.INFO
    file_handler = RotatingFileHandler("pm.log", mode='a', maxBytes=5 * 1024 * 1024,
                                       backupCount=10, encoding=None, delay=0)
    # format the output
    file_handler.setFormatter(logging.Formatter('%(levelname)s %(module)s.%(funcName)s(): %(message)s'))

    # set also the log to the console
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(levelname)s %(module)s.%(funcName)s(): %(message)s'))

    # set logging level
    logging.Logger.setLevel(logging.root, logging_level)

    logging.getLogger().addHandler(file_handler)
    logging.getLogger().addHandler(console)
    logging.info("*****Starting a new session*****")

@timing
def rotate(data, width, height):
    res = []
    for i in range(height):
        for j in range(width):
            res.append(data[(width-j-1)*height+i])
    return res

def invRotate(data, width, height):
    res = []
    for i in range(height):
        for j in range(width):
            res.append(data[((height-1)-i)+height*j])
    return res
