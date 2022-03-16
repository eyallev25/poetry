import logging
from pathlib import Path
import os

OUTPUT_DIR = os.environ["OUTPUT_DIR"]


def get_loggers():
    logs_dir = Path(OUTPUT_DIR)
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)

    __create_logger("tests", logs_dir / "tests.log", level=logging.INFO)


def __create_logger(
    logger_name,
    log_name,
    formatter="%(asctime)s : %(levelname)s : %(name)s : %(message)s",
    level=logging.INFO,
):
    logger_name = logging.getLogger(logger_name)
    logger_name.setLevel(level)
    file_handler = logging.FileHandler(log_name, "w")
    formatter = logging.Formatter(formatter)
    file_handler.setFormatter(formatter)
    logger_name.addHandler(file_handler)

    return logger_name
