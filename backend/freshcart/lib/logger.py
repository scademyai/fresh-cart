import logging
from pathlib import Path

LOG_FILE_PATH = Path("/var/log/fresh-cart.log")

LOG_FORMAT = """
------------ %(asctime)s ----------
%(message)s
--------------------- end ---------------------
"""


def __create_logger(name):
    logger = logging.getLogger(name)
    handler = logging.FileHandler(LOG_FILE_PATH)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger


__LOGGER = __create_logger("fresh-cart")


def log(message):
    __LOGGER.info(message)
