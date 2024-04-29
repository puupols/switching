from abc import ABC, abstractmethod
from src.configuration.base_configuration import BaseConfiguration


class BaseWeatherAPI:

    def __init__(self, configuration: BaseConfiguration):
        self.configuration = configuration

    @abstractmethod
    def get_weather_data(self,  latitude, longitude):
        pass
