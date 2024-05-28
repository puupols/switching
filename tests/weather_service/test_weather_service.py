import unittest
from unittest.mock import Mock
from src.weather_service.api.base_weather_api import BaseWeatherAPI
from src.weather_service.processors.base_weather_processor import BaseWeatherProcessor
from src.repository_service.repository_service import RepositoryService
from src.location_service.base_location_service import BaseLocationService
from src.weather_service.weather_service import WeatherService


class TestWeatherService(unittest.TestCase):

    def setUp(self):
        self.mock_weather_api = Mock(spec=BaseWeatherAPI)
        self.mock_weather_processor = Mock(spec=BaseWeatherProcessor)
        self.mock_repository_service = Mock(spec=RepositoryService)
        self.mock_location_service = Mock(spec=BaseLocationService)
        self.weather_service = WeatherService(self.mock_weather_api, self.mock_weather_processor,
                                              self.mock_repository_service, self.mock_location_service)

    def test_regenerate_weather_data(self):
        self.mock_location_service.get_location.return_value = (52.111, 24.222)
        self.mock_weather_api.get_weather_data.return_value = {'this': 'is', 'raw': 'data'}
        self.mock_weather_processor.process_raw_data.return_value = ['this', 'is', 'processed', 'data']

        # Action
        self.weather_service.regenerate_weather_data()

        # Asserts
        self.mock_location_service.get_location.assert_called_once()
        self.mock_weather_api.get_weather_data.assert_called_once()
        self.mock_weather_processor.process_raw_data.assert_called_once_with({'this': 'is', 'raw': 'data'})
        self.mock_repository_service.store_weather_data.assert_called_once_with(['this', 'is', 'processed', 'data'])

    def test_get_weather_data_after_date(self):
        # Setup
        mock_date = '2024.05.02'
        self.mock_repository_service.get_weather_data_after_date.return_value = 'some data'

        # Actions
        mock_result = self.weather_service.get_weather_data_after_date(mock_date)

        # Asserts
        self.mock_repository_service.get_weather_data_after_date.assert_called_once_with(mock_date)
        self.assertEqual(mock_result, 'some data')


