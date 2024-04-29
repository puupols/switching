from abc import abstractmethod, ABC
from src.configuration.base_configuration import BaseConfiguration

class BaseElectricityPriceAPI(ABC):

    def __init__(self, configuration: BaseConfiguration):
        self.configuration = configuration

    @abstractmethod
    def get_electricity_price(self):
        pass