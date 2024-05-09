import logging


def setup_logger():
    """
    Configures the root logger to output log messages to both the console and a file.

    This function sets up logging with a specific format for messages and directs these messages to
    both the standard output (console) and a file named 'application.log'. Both handlers are configured
    to capture log messages at the INFO level and above.

    The log format includes the timestamp, logger name, log level, and log message which aids in debugging
    and tracking application behavior.

    Effects:
        - Configures the root logger to log at the INFO level.
        - Adds a console handler to the root logger to output logs to the console.
        - Adds a file handler to the root logger to output logs to 'application.log'.
    """
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
