from abc import ABC, abstractmethod


class BaseElectricityPriceProcessor:
    """
    Abstract base class for processors that handle raw electricity price data.

    This class provides a framework for implementing data processing methods that convert raw data
    from electricity price sources into a more usable format.

    Methods:
        process_data: An abstract method that must be implemented to define how raw data is processed.
    """

    def __init__(self):
        pass

    @abstractmethod
    def process_data(self, raw_data):
        """
        Abstract method to process raw electricity price data.

        This method must be implemented by subclasses to parse and convert raw data into
        a structured format, typically as a list of model instances.

        Args:
            raw_data: The raw data format specific to the electricity price source.

        Returns:
            A list of processed data objects, typically instances of a data model.
        """
        pass
