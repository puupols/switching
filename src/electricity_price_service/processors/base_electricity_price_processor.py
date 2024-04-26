from abc import ABC, abstractmethod

class BaseElectricityPriceProcessor:
    def __init__(self):
        pass

    @abstractmethod
    def process_data(self, raw_data):
        pass