from abc import ABC, abstractmethod

class BaseRepositoryService:
    """
    Abstract base class that defines the interface for repository services.

    This class provides a structured way to handle storage and retrieval of weather and electricity
    price data, ensuring that any concrete repository implementation adheres to these defined methods.

    Methods:
        store_weather_data: Store weather data in a repository.
        store_electricity_price_data: Store electricity price data in a repository.
        get_weather_data_after_date: Retrieve weather data stored after a specified date.
        get_electricity_price_data_after_date: Retrieve electricity price data stored after a specified date.
    """
    def __init__(self):
        pass

    @abstractmethod
    def store_weather_data(self, weather_data):
        """
        Store weather data in the repository.

        Args:
            weather_data: The weather data to be stored.
        """
        pass

    @abstractmethod
    def store_electricity_price_data(self, electricity_prices):
        """
        Store electricity price data in the repository.

        Args:
            electricity_prices: The electricity price data to be stored.
        """
        pass

    @abstractmethod
    def get_weather_data_after_date(self, date):
        """
        Retrieve weather data stored after a specified date.

        Args:
            date: The date after which to retrieve weather data.

        Returns:
            An iterable of weather data entries.
        """
        pass

    @abstractmethod
    def get_electricity_price_data_after_date(self, date):
        """
        Retrieve electricity price data stored after a specified date.

        Args:
            date: The date after which to retrieve electricity price data.

        Returns:
            An iterable of electricity price data entries.
        """
        pass
