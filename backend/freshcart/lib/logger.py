import logging
import sys
from pathlib import Path

LOG_FILE_PATH = Path("/var/log/fresh-cart.log")

LOG_FORMAT = """
------------ %(asctime)s ----------
%(message)s
--------------------- end ---------------------
"""


class FlushingFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()


class FlushingStreamHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()


def __create_logger(name):
    logger = logging.getLogger(name)

    # File handler
    file_handler = FlushingFileHandler(LOG_FILE_PATH)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)

    # Stream (stdout) handler
    stream_handler = FlushingStreamHandler(sys.stdout)
    stream_formatter = logging.Formatter(LOG_FORMAT)
    stream_handler.setFormatter(stream_formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


__LOGGER = __create_logger("fresh-cart")


def log(message):
    __LOGGER.info(message)
