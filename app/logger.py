import logging
import os

def get_logger(
        log_level: str = 'INFO',
        log_file: str = "app.log",
) -> logging.Logger:
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, log_file)

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level.upper())
    logger.handlers.clear()

    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
