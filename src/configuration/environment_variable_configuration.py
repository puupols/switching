from src.configuration.base_configuration import BaseConfiguration
import dotenv
import os


class EnvironmentVariableConfiguration(BaseConfiguration):
    """
    Configuration class to load environment variables using dotenv.
    """

    def __init__(self):
        """
        Initialize the configuration by loading the .env file.
        """
        dotenv.load_dotenv()

    def get(self, key, default=None):
        """
        Get the value of the environment variable corresponding to `key`.

        Args:
            key (str): The key of the environment variable.
            default (Any): The default value to return if the environment variable is not found.

        Returns:
            str: The value of the environment variable or the default value.
        """
        return os.getenv(key.upper(), default)

    def get_as_list(self, key, default=None):
        """
        Get the value of the environment variable corresponding to `key` as a list.

        Args:
            key (str): The key of the environment variable.
            default (Any): The default value to return if the environment variable is not found.

        Returns:
            list: The value of the environment variable split by commas, or the default value as a list.
        """
        values = os.getenv(key.upper())
        if values is not None:
            return values.split(",")
        else:
            return default or []
