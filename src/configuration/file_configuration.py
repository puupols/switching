import json
from src.configuration.base_configuration import BaseConfiguration


class FileConfiguration(BaseConfiguration):
    """
    Concrete implementation of BaseConfiguration that retrieves settings from a JSON file.
    """
    CONFIGURATION_FILE_PATH = 'src/switching.conf'

    def __init__(self):
        """
        Initializes the FileConfiguration instance by loading data from the specified JSON configuration file.
        """
        self.configuration = self._get_configuration_from_file()

    def get(self, key):
        """
        Retrieves a configuration value by key from the loaded JSON data.

        Args:
            key (str): The key for the configuration value to retrieve.

        Returns:
            The value corresponding to the provided key from the configuration.
            Returns None if the key does not exist in the configuration.
        """
        return self.configuration.get(key)

    def _get_configuration_from_file(self):
        """
        Private method to load and parse the configuration from the JSON file specified by CONFIGURATION_FILE_PATH.

        Returns:
            dict: A dictionary containing the configuration settings.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            json.JSONDecodeError: If there is an error in decoding the JSON.
        """
        with open(self.CONFIGURATION_FILE_PATH, 'r') as config_file:
            return json.loads(config_file.read())
