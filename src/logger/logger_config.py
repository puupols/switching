import logging


def setup_logger():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))

    file_handler = logging.FileHandler('application.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
