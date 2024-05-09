from abc import ABC, abstractmethod
from src.configuration.base_configuration import BaseConfiguration


class BaseWeatherAPI:
    """
    An abstract base class that defines the interface for weather data APIs.

    This class establishes the fundamental functions that any weather data fetching API should implement,
    ensuring that all concrete implementations provide a consistent method for retrieving weather data.

    Attributes:
        configuration (BaseConfiguration): A configuration object which stores API keys, endpoints, and other necessary configuration settings.
    """

    def __init__(self, configuration: BaseConfiguration):
        self.configuration = configuration

    @abstractmethod
    def get_weather_data(self,  latitude, longitude):
        """
        Abstract method to retrieve weather data for a specific geographical location.

        Args:
            latitude (float): The latitude of the location for which to retrieve weather data.
            longitude (float): The longitude of the location for which to retrieve weather data.

        Returns:
            This method should return a structured dictionary of weather data specific to the implementation.
        """
        pass
