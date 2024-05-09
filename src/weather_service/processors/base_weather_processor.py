from abc import ABC, abstractmethod


class BaseWeatherProcessor(ABC):
    """
    An abstract base class that defines the interface for weather data processors.

    This class provides the structure for implementing weather data processing capabilities,
    which transform raw weather data into a usable format for application consumption.

    Methods:
        process_raw_data: Abstract method to process raw weather data into a structured format.
    """

    def __init__(self):
        pass

    @abstractmethod
    def process_raw_data(self, raw_data):
        """
        Abstract method to process raw weather data.

        This method should be implemented by subclasses to convert raw weather data
        into a structured and potentially more useful format.

        Args:
            raw_data: The raw data format specific to the weather data source.

        Returns:
            A list or other collection of processed data objects, typically instances of a data model.
        """
        pass
