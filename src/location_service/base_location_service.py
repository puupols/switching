from abc import ABC, abstractmethod


class BaseLocationService(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_location(self):
        pass
