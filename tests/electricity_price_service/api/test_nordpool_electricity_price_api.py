import unittest
from pathlib import Path
import json
from unittest.mock import Mock, patch
from src.configuration.base_configuration import BaseConfiguration
from src.electricity_price_service.api.nordpool_electricity_price_api import NordpoolElectricityPriceAPI

class TestNordpoolElectricityPriceAPI(unittest.TestCase):

    def setUp(self):
        self.mock_config = Mock(spec=BaseConfiguration)
        self.mock_config.get.return_value = 'http://some_url'
        self.api = NordpoolElectricityPriceAPI(self.mock_config)

    @patch('src.electricity_price_service.api.nordpool_electricity_price_api.requests.get')
    def test_get_electricity_price(self, mock_get):

        # Setup
        mock_response = Mock()
        expected_json = self.get_expected_json()
        mock_response.json.return_value = expected_json
        mock_get.return_value = mock_response

        # Action
        result = self.api.get_electricity_price()

        # Assert
        mock_get.assert_called_once_with('http://some_url')
        self.assertEqual(result, expected_json)

    def get_expected_json(self):
        root_path = Path(__file__).parent.parent.parent
        data_path = root_path / 'electricity_price_service' / 'data' / 'nordpool_sample_response.json'
        with data_path.open('r') as file:
            data = file.read()
        return json.loads(data)