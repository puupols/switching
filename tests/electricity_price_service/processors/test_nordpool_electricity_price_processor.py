import json
import datetime
from src.electricity_price_service.processors.nordpool_electricity_price_processor import NordpoolElectricityPriceProcessor
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel
import unittest
from pathlib import Path

class TestNordpoolElectricityPriceProcessor(unittest.TestCase):

    def _get_data(self, file_name):
        base_path = Path(__file__).parent.parent.parent
        file_path = base_path / 'electricity_price_service' / 'data' / file_name
        with file_path.open('r') as file:
            raw_data = file.read()
        return json.loads(raw_data)

    def test_process_data(self):
        # Setup
        raw_data = self._get_data('nordpool_sample_response.json')
        processor = NordpoolElectricityPriceProcessor()

        # Actions
        processed_data = processor.process_data(raw_data)

        # Asserts
        self.assertEqual(len(processed_data), 24)
        self.assertIsInstance(processed_data[0], ElectricityPriceModel)
        self.assertEqual(processed_data[0].price, 71.99)
        self.assertEqual(processed_data[0].datetime, datetime.datetime(2024, 4, 30, 0, 0))

    def test_process_data_broken_data(self):
        # Setup
        raw_data = self._get_data('nordpool_sample_response_broken.json')
        processor = NordpoolElectricityPriceProcessor()

        # Actions
        processed_data = processor.process_data(raw_data)

        # Asserts
        self.assertEqual(len(processed_data), 22)