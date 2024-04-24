from abc import ABC, abstractmethod


class BaseConfiguration(ABC):

    @abstractmethod
    def get(self, key):
        pass
