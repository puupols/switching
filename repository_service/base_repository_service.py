from abc import ABC, abstractmethod

class BaseRepositoryService:
    def __init__(self):
        pass

    @abstractmethod
    def store_weather_data(self, weather_data):
        pass

