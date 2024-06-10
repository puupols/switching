from src.electricity_price_service.electricity_price_service import ElectricityPriceService
from src.electricity_price_service.api.base_electricity_price_api import BaseElectricityPriceAPI
from src.electricity_price_service.processors.base_electricity_price_processor import BaseElectricityPriceProcessor
from src.repository_service.electricity_price_repository_service import ElectricityPriceRepositoryService
from unittest.mock import Mock
import unittest

class TestElectricityPriceService(unittest.TestCase):

    def setUp(self):
        self.mock_api = Mock(spec=BaseElectricityPriceAPI)
        self.mock_processor = Mock(spec=BaseElectricityPriceProcessor)
        self.mock_repository = Mock(spec=ElectricityPriceRepositoryService)
        self.service = ElectricityPriceService(self.mock_api, self.mock_processor, self.mock_repository)

    def test_regenerate_electricity_price_date(self):

        # Setup
        mock_raw_data = 'raw data'
        mock_processed_data = 'processed_data'
        self.mock_api.get_electricity_price.return_value = mock_raw_data
        self.mock_processor.process_data.return_value = mock_processed_data

        # Action
        self.service.regenerate_electricity_price_data()

        # Asserts
        self.mock_api.get_electricity_price.assert_called_once()
        self.mock_processor.process_data.assert_called_once_with(mock_raw_data)
        self.mock_repository.store_electricity_price_data.assert_called_once_with(mock_processed_data)

    def test_get_electricity_price_data_after_date(self):

        # Setup
        mock_date = '2024.04.30'
        mock_return_data = 'return_data'
        self.mock_repository.get_electricity_price_data_after_date.return_value = mock_return_data

        # Action
        result = self.service.get_electricity_price_data_after_date(mock_date)

        # Asserts
        self.mock_repository.get_electricity_price_data_after_date.assert_called_once_with(mock_date)
        self.assertEqual(result, mock_return_data)

