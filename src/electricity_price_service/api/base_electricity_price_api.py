from abc import abstractmethod, ABC
from src.configuration.base_configuration import BaseConfiguration
import logging


class BaseElectricityPriceAPI(ABC):
    """
    Abstract base class defining the interface for electricity price APIs.

    Attributes:
        configuration (BaseConfiguration): Configuration object that holds settings
                                           such as API keys and URLs.
        logger (Logger): Logger instance for logging messages.

    Methods:
        get_electricity_price: Abstract method that should be implemented to fetch
                               electricity prices from a specific service.
    """

    def __init__(self, configuration: BaseConfiguration):
        """
        Initializes the BaseElectricityPriceAPI with the necessary configuration.

        Args:
            configuration (BaseConfiguration): The configuration object containing
                                               necessary parameters and credentials for the API.
        """
        self.configuration = configuration
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def get_electricity_price(self):
        """
        Abstract method to fetch the current electricity price.

        Must be implemented by subclasses to return current electricity price data.

        Returns:
            Implementation-dependent, typically a dictionary or model instance containing
            electricity price data.
        """
        pass
