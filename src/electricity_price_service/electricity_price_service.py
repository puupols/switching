import inject
from src.electricity_price_service.api.base_electricity_price_api import BaseElectricityPriceAPI
from src.electricity_price_service.processors.base_electricity_price_processor import BaseElectricityPriceProcessor
from src.repository_service.base_repository_service import BaseRepositoryService

class ElectricityPriceService:
    """
    Service class that coordinates the fetching, processing, and storing of electricity price data.

    This class integrates components that handle API interactions, data processing, and data persistence,
    providing a high-level interface for managing electricity price data.

    Attributes:
        electricity_price_api (BaseElectricityPriceAPI): An API client for fetching electricity price data.
        electricity_price_processor (BaseElectricityPriceProcessor): A processor to transform raw data into a usable format.
        repository_service (BaseRepositoryService): A repository service for storing and retrieving processed data.
    """

    @inject.autoparams()
    def __init__(self, electricity_price_api: BaseElectricityPriceAPI, electricity_price_processor: BaseElectricityPriceProcessor,
                 repository_service: BaseRepositoryService):
        """
        Initializes the ElectricityPriceService with the necessary components.

        The parameters for this constructor are automatically injected with the inject.autoparams() decorator,
        which relies on type hints to resolve the dependencies.

        Args:
            electricity_price_api (BaseElectricityPriceAPI): The API client component for fetching electricity prices.
            electricity_price_processor (BaseElectricityPriceProcessor): The data processor component.
            repository_service (BaseRepositoryService): The data storage and retrieval component.
        """
        self.electricity_price_api = electricity_price_api
        self .electricity_price_processor = electricity_price_processor
        self.repository_service = repository_service

    def regenerate_electricity_price_data(self):
        """
        Fetches, processes, and stores electricity price data.

        This method serves as a workflow to update stored electricity price data by:
        1. Fetching raw data from the API.
        2. Processing that data into a structured format.
        3. Storing the processed data in the repository.
        """
        raw_data = self.electricity_price_api.get_electricity_price()
        processed_data = self.electricity_price_processor.process_data(raw_data)
        self.repository_service.store_electricity_price_data(processed_data)

    def get_electricity_price_data_after_date(self, date):
        """
        Retrieves processed electricity price data stored after a specified date.

        Args:
            date (datetime): The starting date from which to retrieve data.

        Returns:
            list[ElectricityPriceModel]: A list of ElectricityPriceModel instances representing hourly electricity prices starting from the specified date.
        """
        return self.repository_service.get_electricity_price_data_after_date(date)
