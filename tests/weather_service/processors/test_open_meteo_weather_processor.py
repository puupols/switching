import json
import unittest
import datetime
from pathlib import Path
from src.weather_service.processors.open_meteo_weather_processor import OpenMeteoWeatherProcessor
from src.weather_service.models.weather_model import WeatherModel


class TestOpenMeteoWeatherProcessor(unittest.TestCase):

    def _get_data(self, file_name):
        base_path = Path(__file__).parent.parent.parent
        file_path = base_path / 'weather_service' / 'data' / file_name
        with file_path.open('r') as file:
            raw_data = file.read()
        return json.loads(raw_data)

    def test_process_raw_data(self):
        # Setup
        self.data = self._get_data('open_meteo_sample_response.json')
        self.processor = OpenMeteoWeatherProcessor()

        # Actions
        processed_data = self.processor.process_raw_data(self.data)

        # Asserts
        self.assertEqual(len(processed_data), 24)
        self.assertIsInstance(processed_data[0], WeatherModel)
        self.assertEqual(processed_data[0].datetime, datetime.datetime(2024, 5, 4, 0, 0))
        self.assertEqual(processed_data[0].latitude, 54.25)
        self.assertEqual(processed_data[0].longitude, 24.25)
        self.assertEqual(processed_data[0].cloud_cover, 41)
        self.assertEqual(processed_data[0].temperature, 11.7)
        self.assertEqual(processed_data[0].sunshine_duration, 0.0)

    def test_process_raw_data_missing_data(self):
        # Setup
        self.data = self._get_data('open_meteo_sample_response_missing_data.json')
        self.processor = OpenMeteoWeatherProcessor()

        # Actions
        processed_data = self.processor.process_raw_data(self.data)

        # Asserts
        self.assertIsNone(processed_data)