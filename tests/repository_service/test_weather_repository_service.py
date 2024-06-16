import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy import inspect
from sqlalchemy.orm import clear_mappers
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from src.configuration.base_configuration import BaseConfiguration
from src.weather_service.models.weather_model import WeatherModel
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel
from src.repository_service.weather_repository_service import WeatherRepositoryService
from src.repository_service.base_repository_service import BaseRepositoryService
from src.switch_service.models.switch_model import SwitchModel


class TestWeatherRepositoryService(unittest.TestCase):

    def setUp(self):
        self.mock_configuration = MagicMock(spec=BaseConfiguration)
        self.mock_configuration.get.return_value = "sqlite:///:memory:"
        self.weather_repository_service = WeatherRepositoryService(self.mock_configuration)
        self.weather_repository_service.create_database()

        self.weather_data = [
            WeatherModel(datetime=datetime(2023, 1, 1, 12, 0), cloud_cover=20.5, temperature=25.0, latitude=50.0,
                         longitude=8.0, sunshine_duration=5.0, location_id=1)
        ]
        self.duplicate_weather_data = [
            WeatherModel(datetime=datetime(2023, 1, 1, 12, 0), cloud_cover=20.5, temperature=25.0, latitude=50.0,
                         longitude=8.0, sunshine_duration=5.0, location_id=1),
            WeatherModel(datetime=datetime(2023, 1, 1, 12, 0), cloud_cover=20.5, temperature=35.0, latitude=50.0,
                         longitude=8.0, sunshine_duration=5.0, location_id=1)
        ]

    def tearDown(self):
        self.weather_repository_service.metadata.drop_all(self.weather_repository_service.engine)
        clear_mappers()
        self.weather_repository_service.engine.dispose()

    def test_store_weather_data(self):
        # Setup
        expected_temperature = self.weather_data[0].temperature

        # Actions
        self.weather_repository_service.store_weather_data(self.weather_data)
        with self.weather_repository_service.session_maker() as session:
            stored_data = session.query(WeatherModel).all()

        # Asserts
        self.assertEqual(len(stored_data), len(self.weather_data))
        self.assertEqual(stored_data[0].temperature, expected_temperature)

    def test_update_weather_data_if_it_exists(self):
        # Setup
        expected_temperature = self.duplicate_weather_data[1].temperature

        # Actions
        self.weather_repository_service.store_weather_data(self.duplicate_weather_data)
        with self.weather_repository_service.session_maker() as session:
            stored_data = session.query(WeatherModel).all()

        # Asserts
        self.assertEqual(stored_data[0].temperature, expected_temperature)

    def test_get_weather_data_after_date(self):
        # Setup
        expected_date = self.weather_data[0].datetime
        expected_temperature = self.weather_data[0].temperature

        # Actions
        self.weather_repository_service.store_weather_data(self.weather_data)
        date_filter = datetime(2023, 1, 1, 0, 0)
        result = self.weather_repository_service.get_weather_data_after_date(date_filter)

        # Asserts
        self.assertEqual(len(result), len(self.weather_data))
        self.assertEqual(result[0].datetime, expected_date)
        self.assertEqual(result[0].temperature, expected_temperature)

    def test_get_weather_data_after_date_no_results(self):
        # Setup
        date_filter = datetime(2024, 1, 1, 0, 0)

        # Actions
        result = self.weather_repository_service.get_weather_data_after_date(date_filter)

        # Asserts
        self.assertEqual(len(result), 0)