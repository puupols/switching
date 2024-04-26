from abc import ABC, abstractmethod

class BaseRepositoryService:
    def __init__(self):
        pass

    @abstractmethod
    def store_weather_data(self, weather_data):
        pass

    @abstractmethod
    def store_electricity_price_data(self, electricity_prices):
        pass

    @abstractmethod
    def get_weather_data_after_date(self, date):
        pass

    @abstractmethod
    def get_electricity_price_data_after_date(self, date):
        pass
