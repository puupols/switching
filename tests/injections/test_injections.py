import unittest
from unittest.mock import patch, MagicMock, call

from src.electricity_price_service.api.base_electricity_price_api import BaseElectricityPriceAPI
from src.electricity_price_service.processors.base_electricity_price_processor import BaseElectricityPriceProcessor
from src.injections.injections import app_injection_configuration
from src.location_service.base_location_service import BaseLocationService
from src.weather_service.api.base_weather_api import BaseWeatherAPI
from src.weather_service.processors.base_weather_processor import BaseWeatherProcessor


class TestAppInjectionConfiguration(unittest.TestCase):
    @patch('src.injections.injections.FileConfiguration', autospec=True)
    @patch('src.injections.injections.ConfigurationBasedLocationService', autospec=True)
    @patch('src.injections.injections.OpenMeteoWeatherAPI', autospec=True)
    @patch('src.injections.injections.OpenMeteoWeatherProcessor', autospec=True)
    @patch('src.injections.injections.NordpoolElectricityPriceAPI', autospec=True)
    @patch('src.injections.injections.NordpoolElectricityPriceProcessor', autospec=True)
    @patch('src.injections.injections.logging.getLogger')
    def test_app_injection_configuration(self, mock_logger, mock_nordpool_processor,
                                         mock_nordpool_api, mock_weather_processor, mock_weather_api,
                                         mock_location_service, mock_file_config):
        # Setup mock configuration to return specific values
        mock_config_instance = MagicMock()
        mock_file_config.return_value = mock_config_instance
        mock_config_instance.get.side_effect = lambda key: {
            'location_service': 'configuration_file',
            'weather_service': 'open_meteo',
            'electricity_price_service': 'nordpool'
        }.get(key, None)

        # Create a mock for the binder used in the function
        mock_binder = MagicMock()

        # Run the function under test
        app_injection_configuration(mock_binder)

        expected_calls = [
            call(BaseLocationService, mock_location_service.return_value),
            call(BaseWeatherAPI, mock_weather_api.return_value),
            call(BaseWeatherProcessor, mock_weather_processor.return_value),
            call(BaseElectricityPriceAPI, mock_nordpool_api.return_value),
            call(BaseElectricityPriceProcessor, mock_nordpool_processor.return_value),
        ]

        mock_binder.bind.assert_has_calls(expected_calls, any_order=True)

    @patch('src.injections.injections.FileConfiguration', autospec=True)
    @patch('src.injections.injections.ConfigurationBasedLocationService', autospec=True)
    @patch('src.injections.injections.OpenMeteoWeatherAPI', autospec=True)
    @patch('src.injections.injections.OpenMeteoWeatherProcessor', autospec=True)
    @patch('src.injections.injections.NordpoolElectricityPriceAPI', autospec=True)
    @patch('src.injections.injections.NordpoolElectricityPriceProcessor', autospec=True)
    @patch('src.injections.injections.logging.getLogger')
    def test_invalid_location_service_config(self, mock_logger, mock_nordpool_processor,
                                             mock_nordpool_api, mock_weather_processor, mock_weather_api,
                                             mock_location_service, mock_file_config):
        # Setup mock configuration to return an invalid value for location service
        mock_config_instance = MagicMock()
        mock_file_config.return_value = mock_config_instance
        mock_config_instance.get.side_effect = lambda key: {
            'location_service': 'invalid_config',
            'weather_service': 'open_meteo',
            'electricity_price_service': 'nordpool'
        }.get(key, None)

        # Create a mock for the binder used in the function
        mock_binder = MagicMock()

        # Assert that a ValueError is raised with the correct message
        with self.assertRaises(ValueError) as context:
            app_injection_configuration(mock_binder)
        self.assertIn("Unsupported location service", str(context.exception))

    @patch('src.injections.injections.FileConfiguration', autospec=True)
    @patch('src.injections.injections.ConfigurationBasedLocationService', autospec=True)
    @patch('src.injections.injections.OpenMeteoWeatherAPI', autospec=True)
    @patch('src.injections.injections.OpenMeteoWeatherProcessor', autospec=True)
    @patch('src.injections.injections.NordpoolElectricityPriceAPI', autospec=True)
    @patch('src.injections.injections.NordpoolElectricityPriceProcessor', autospec=True)
    @patch('src.injections.injections.logging.getLogger')
    def test_invalid_weather_service_config(self, mock_logger, mock_nordpool_processor,
                                            mock_nordpool_api, mock_weather_processor, mock_weather_api,
                                            mock_location_service, mock_file_config):
        # Setup mock configuration to return an invalid value for location service
        mock_config_instance = MagicMock()
        mock_file_config.return_value = mock_config_instance
        mock_config_instance.get.side_effect = lambda key: {
            'location_service': 'configuration_file',
            'weather_service': 'invalid_config',
            'electricity_price_service': 'nordpool'
        }.get(key, None)

        # Create a mock for the binder used in the function
        mock_binder = MagicMock()

        # Assert that a ValueError is raised with the correct message
        with self.assertRaises(ValueError) as context:
            app_injection_configuration(mock_binder)
        self.assertIn("Unsupported weather api service", str(context.exception))

    @patch('src.injections.injections.FileConfiguration', autospec=True)
    @patch('src.injections.injections.ConfigurationBasedLocationService', autospec=True)
    @patch('src.injections.injections.OpenMeteoWeatherAPI', autospec=True)
    @patch('src.injections.injections.OpenMeteoWeatherProcessor', autospec=True)
    @patch('src.injections.injections.NordpoolElectricityPriceAPI', autospec=True)
    @patch('src.injections.injections.NordpoolElectricityPriceProcessor', autospec=True)
    @patch('src.injections.injections.logging.getLogger')
    def test_invalid_electricity_price_service_config(self, mock_logger, mock_nordpool_processor,
                                                      mock_nordpool_api, mock_weather_processor, mock_weather_api,
                                                      mock_location_service, mock_file_config):
        # Setup mock configuration to return an invalid value for location service
        mock_config_instance = MagicMock()
        mock_file_config.return_value = mock_config_instance
        mock_config_instance.get.side_effect = lambda key: {
            'location_service': 'configuration_file',
            'weather_service': 'open_meteo',
            'electricity_price_service': 'invalid_config'
        }.get(key, None)

        # Create a mock for the binder used in the function
        mock_binder = MagicMock()

        # Assert that a ValueError is raised with the correct message
        with self.assertRaises(ValueError) as context:
            app_injection_configuration(mock_binder)
        self.assertIn("Unsupported electricity price api service", str(context.exception))
