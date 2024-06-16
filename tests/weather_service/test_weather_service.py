import unittest
from unittest.mock import Mock, call
from src.weather_service.api.base_weather_api import BaseWeatherAPI
from src.weather_service.processors.base_weather_processor import BaseWeatherProcessor
from src.repository_service.weather_repository_service import WeatherRepositoryService
from src.location_service.location_service import LocationService
from src.location_service.models.location_model import LocationModel
from src.weather_service.weather_service import WeatherService


class TestWeatherService(unittest.TestCase):

    def setUp(self):
        self.mock_weather_api = Mock(spec=BaseWeatherAPI)
        self.mock_weather_processor = Mock(spec=BaseWeatherProcessor)
        self.mock_repository_service = Mock(spec=WeatherRepositoryService)
        self.mock_location_service = Mock(spec=LocationService)
        self.weather_service = WeatherService(self.mock_weather_api, self.mock_weather_processor,
                                              self.mock_repository_service, self.mock_location_service)

    def test_regenerate_weather_data(self):

        # Setup
        self.mock_location_service.get_all_locations.return_value = [LocationModel(latitude=1, longitude=2,id=1),
                                                                     LocationModel(latitude=3, longitude=4, id=2)]
        self.mock_weather_api.get_weather_data.side_effect = [{'temp': 20}, {'temp': 25}]
        self.mock_weather_processor.process_raw_data.side_effect = [{'processed_temp': 18}, {'processed_temp': 23}]

        # Action
        self.weather_service.regenerate_weather_data()

        # Asserts
        self.mock_location_service.get_all_locations.assert_called_once()
        self.mock_weather_api.get_weather_data.assert_any_call(1, 2)
        self.mock_weather_api.get_weather_data.assert_any_call(3, 4)
        self.mock_weather_processor.process_raw_data.assert_any_call({'temp': 20}, 1)
        self.mock_weather_processor.process_raw_data.assert_any_call({'temp': 25}, 2)
        self.mock_repository_service.store_weather_data.assert_any_call({'processed_temp': 18})
        self.mock_repository_service.store_weather_data.assert_any_call({'processed_temp': 23})

    def test_get_weather_data_after_date(self):
        # Setup
        mock_date = '2024.05.02'
        self.mock_repository_service.get_weather_data_after_date.return_value = 'some data'

        # Actions
        mock_result = self.weather_service.get_weather_data_after_date(mock_date)

        # Asserts
        self.mock_repository_service.get_weather_data_after_date.assert_called_once_with(mock_date)
        self.assertEqual(mock_result, 'some data')


