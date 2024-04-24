from abc import abstractmethod, ABC

class BaseElectricityPriceAPI(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_electricity_pirce(self):
        pass