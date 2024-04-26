import json
from src.configuration.base_configuration import BaseConfiguration


class FileConfiguration(BaseConfiguration):
    def __init__(self):
        self.configuration = self._get_configuration_from_file()

    def get(self, key):
        return self.configuration.get(key)

    def _get_configuration_from_file(self):
        with open('src/switching.conf', 'r') as config_file:
            return json.loads(config_file.read())
