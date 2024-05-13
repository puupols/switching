import json
import logging.config
import logging


def setup_logger():
    """
    Set up the logging configurations for the application using a JSON configuration file.

    This function reads the logging configuration from a file named 'logging_config.json'.
    It then uses this configuration to set up
    the logging settings for the application.

    Raises:
        FileNotFoundError: If the 'logging_config.json' file does not exist.
        json.JSONDecodeError: If there is an error parsing the JSON file.
        KeyError: If the essential keys are missing in the JSON configuration.
    """
    with open('logging_config.json', 'r') as config_file:
        config_dict = json.load(config_file)
        logging.config.dictConfig(config_dict)
