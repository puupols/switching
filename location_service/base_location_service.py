from abc import ABC, abstractmethod
from configuration.file_configuration import BaseConfiguration


class BaseLocationService(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_location(self):
        pass
