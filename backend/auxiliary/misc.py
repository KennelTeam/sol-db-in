import logging
import time

from backend.constants import LOGS_DIRECTORY


_loggers = {}

logs_file_handler = logging.FileHandler(LOGS_DIRECTORY / f'sol-db-in-{int(time.time())}.log')  # Initilize file handler
logs_stream_handler = logging.StreamHandler()  # Initialize stdout handler

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Set format
logs_file_handler.setFormatter(formatter)
logs_stream_handler.setFormatter(formatter)

logs_file_handler.setLevel(logging.DEBUG)
logs_stream_handler.setLevel(logging.INFO)


def get_sol_db_logger(module: str) -> logging.Logger:
    if module in _loggers:  # Check if the logger already exists
        return _loggers[module]

    logger = logging.getLogger(f'sol-db-in.{module}')  # Get the logger
    logger.setLevel(logging.DEBUG)  # Set level

    logger.addHandler(logs_file_handler)  # Add the handlers
    logger.addHandler(logs_stream_handler)

    _loggers[module] = logger
    return logger
