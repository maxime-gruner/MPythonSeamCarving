import os
import logging
from logging.handlers import RotatingFileHandler

PROJECT_PATH = os.getcwd()
IMAGE_PATH = PROJECT_PATH + "/images/"


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
    logging.info("************************************Starting a new session************************************")
