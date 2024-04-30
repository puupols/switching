import json
import datetime
from src.electricity_price_service.processors.nordpool_electricity_price_processor import NordpoolElectricityPriceProcessor
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel
import unittest
from pathlib import Path

class TestNordpoolElectricityPriceProcessor(unittest.TestCase):

    def test_process_data(self):

        # Setup
        raw_data = self.get_data()
        processor = NordpoolElectricityPriceProcessor()

        # Actions
        processed_data = processor.process_data(raw_data)

        # Asserts
        self.assertEqual(len(processed_data), 24)
        self.assertIsInstance(processed_data[0], ElectricityPriceModel)
        self.assertEqual(processed_data[0].price, 71.99)
        self.assertEqual(processed_data[0].datetime, datetime.datetime(2024, 4, 30, 0, 0))

    def get_data(self):
        base_path = Path(__file__).parent.parent.parent
        file_path = base_path / 'electricity_price_service' / 'data' / 'nordpool_sample_response.json'
        with file_path.open('r') as file:
            raw_data = file.read()
        return json.loads(raw_data)