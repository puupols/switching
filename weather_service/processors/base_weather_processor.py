from abc import ABC, abstractmethod

class BaseWeatherProcessor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def process_raw_data(self, raw_data):
        pass