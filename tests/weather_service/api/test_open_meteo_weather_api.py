import unittest
from unittest.mock import Mock, patch
from src.weather_service.api.open_meteo_weather_api import OpenMeteoWeatherAPI

class TestOpenMeteoWeatherAPI(unittest.TestCase):

    @patch('src.weather_service.api.open_meteo_weather_api.requests')
    def test_get_weather_data(self, mock_requests):

        # Setup
        expected_url = 'https://api.openmeteo.com?latitude=52.555&longitude=24.5555&weather_data_types=cloud_cover,temperature,sunshine_duration&forecast_days=3&timezone=EET'
        data = {"my": "json", "file": "here"}
        response = Mock()
        response.json.return_value = data
        mock_requests.get.return_value = response
        mock_configuration = Mock()
        mock_configuration.get.side_effect = lambda key: {
            'open_meteo_url': 'https://api.openmeteo.com?latitude={latitude}&longitude={longitude}&weather_data_types={weather_data_types}&forecast_days={forecast_days}&timezone={timezone}'}[
            key]
        api_service = OpenMeteoWeatherAPI(mock_configuration)

        # Action
        result = api_service.get_weather_data(52.555, 24.5555)

        # Assertion
        mock_requests.get.assert_called_once_with(expected_url)
        response.json.assert_called_once()
        self.assertEqual(result, data)

    @patch('src.weather_service.api.open_meteo_weather_api.requests')
    def test_get_weather_data_request_exception(self, mock_requests):
        # Setup
        mock_requests.get.side_effect = Exception('Boom!')
        mock_configuration = Mock()
        mock_configuration.get.side_effect = lambda key: {
            'open_meteo_url': 'https://api.openmeteo.com?latitude={latitude}&longitude={longitude}&weather_data_types={weather_data_types}&forecast_days={forecast_days}&timezone={timezone}'}[
            key]
        api_service = OpenMeteoWeatherAPI(mock_configuration)

        # Action
        result = api_service.get_weather_data(52.555, 24.5555)

        # Assertion
        self.assertIsNone(result)

