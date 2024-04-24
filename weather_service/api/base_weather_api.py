from abc import ABC, abstractmethod


class BaseWeatherAPI:

    def __init__(self):
        pass

    @abstractmethod
    def get_weather_data(self,  latitude, longitude):
        pass
