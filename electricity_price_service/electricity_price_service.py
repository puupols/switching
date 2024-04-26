from electricity_price_service.api.base_electricity_price_api import BaseElectricityPriceAPI
from electricity_price_service.processors.base_electricity_price_processor import BaseElectricityPriceProcessor
from repository_service.base_repository_service import BaseRepositoryService

class ElectricityPriceService:

    def __init__(self, electricity_price_api: BaseElectricityPriceAPI, electricity_price_processor: BaseElectricityPriceProcessor,
                 repository_service: BaseRepositoryService):
        self.electricity_price_api = electricity_price_api
        self .electricity_price_processor = electricity_price_processor
        self.repository_service = repository_service

    def regenerate_electricity_price_data(self):
        raw_data = self.electricity_price_api.get_electricity_price()
        processed_data = self.electricity_price_processor.process_data(raw_data)
        self.repository_service.store_electricity_price_data(processed_data)

    def get_electricity_price_data_after_date(self, date):
        return self.repository_service.get_electricity_price_data_after_date(date)
