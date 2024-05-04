from src.weather_service.models.weather_model import WeatherModel
import unittest

class TestWeatherModel(unittest.TestCase):

    def test_weather_model(self):
        # Setup
        self.datetime = '2024.03.12'
        self.cloud_cover = 100
        self.temperature = 24
        self.latitude = 52.123
        self.longitude = 24.123
        self.sunshine_duration = 3100

        # Actions
        self.weather = WeatherModel(self.datetime, self.cloud_cover, self.temperature, self.latitude, self.longitude, self.sunshine_duration)

        # Asserts
        self.assertEqual(self.weather.datetime, self.datetime)
        self.assertEqual(self.weather.cloud_cover, self.cloud_cover)
        self.assertEqual(self.weather.temperature, self.temperature)
        self.assertEqual(self.weather.latitude, self.latitude)
        self.assertEqual(self.weather.longitude, self.longitude)
        self.assertEqual(self.weather.sunshine_duration, self.sunshine_duration)

