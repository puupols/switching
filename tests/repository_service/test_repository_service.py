import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy import inspect
from sqlalchemy.orm import clear_mappers
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from src.configuration.base_configuration import BaseConfiguration
from src.weather_service.models.weather_model import WeatherModel
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel
from src.repository_service.repository_service import RepositoryService
from src.switch_service.models.switch_model import SwitchModel


class TestRepositoryService(unittest.TestCase):

    def setUp(self):
        self.mock_configuration = MagicMock(spec=BaseConfiguration)
        self.mock_configuration.get.return_value = "sqlite:///:memory:"
        self.repository_service = RepositoryService(configuration=self.mock_configuration)
        self.repository_service.create_database()

        self.weather_data = [
            WeatherModel(datetime=datetime(2023, 1, 1, 12, 0), cloud_cover=20.5, temperature=25.0, latitude=50.0,
                         longitude=8.0, sunshine_duration=5.0)
        ]
        self.duplicate_weather_data = [
            WeatherModel(datetime=datetime(2023, 1, 1, 12, 0), cloud_cover=20.5, temperature=25.0, latitude=50.0,
                         longitude=8.0, sunshine_duration=5.0),
            WeatherModel(datetime=datetime(2023, 1, 1, 12, 0), cloud_cover=20.5, temperature=35.0, latitude=50.0,
                         longitude=8.0, sunshine_duration=5.0)
        ]
        self.electricity_price_data = [
            ElectricityPriceModel(datetime=datetime(2023, 1, 1, 12, 0), price=50.0)
        ]
        self.duplicate_electricity_price_data = [
            ElectricityPriceModel(datetime=datetime(2023, 1, 1, 12, 0), price=50.0),
            ElectricityPriceModel(datetime=datetime(2023, 1, 1, 12, 0), price=100.0)
        ]

    def tearDown(self):
        self.repository_service.metadata.drop_all(self.repository_service.engine)
        clear_mappers()
        self.repository_service.engine.dispose()

    def test_create_database(self):
        # Setup
        inspector = inspect(self.repository_service.engine)

        # Asserts
        self.assertTrue(inspector.has_table('weather'))
        self.assertTrue(inspector.has_table('electricity_price'))

    def test_store_weather_data(self):
        # Setup
        expected_temperature = self.weather_data[0].temperature

        # Actions
        self.repository_service.store_weather_data(self.weather_data)
        with self.repository_service.session_maker() as session:
            stored_data = session.query(WeatherModel).all()

        # Asserts
        self.assertEqual(len(stored_data), len(self.weather_data))
        self.assertEqual(stored_data[0].temperature, expected_temperature)

    def test_store_electricity_price_data(self):
        # Setup
        expected_price = self.electricity_price_data[0].price

        # Actions
        self.repository_service.store_electricity_price_data(self.electricity_price_data)
        with self.repository_service.session_maker() as session:
            stored_data = session.query(ElectricityPriceModel).all()

        # Asserts
        self.assertEqual(len(stored_data), len(self.electricity_price_data))
        self.assertEqual(stored_data[0].price, expected_price)

    def test_update_weather_data_if_it_exists(self):
        # Setup
        expected_temperature = self.duplicate_weather_data[1].temperature

        # Actions
        self.repository_service.store_weather_data(self.duplicate_weather_data)
        with self.repository_service.session_maker() as session:
            stored_data = session.query(WeatherModel).all()

        # Asserts
        self.assertEqual(stored_data[0].temperature, expected_temperature)

    def test_update_electricity_price_data_if_it_exists(self):
        # Setup
        expected_price = self.duplicate_electricity_price_data[1].price

        # Actions
        self.repository_service.store_electricity_price_data(self.duplicate_electricity_price_data)
        with self.repository_service.session_maker() as session:
            stored_data = session.query(ElectricityPriceModel).all()

        # Asserts
        self.assertEqual(stored_data[0].price, expected_price)

    def test_get_weather_data_after_date(self):
        # Setup
        expected_date = self.weather_data[0].datetime
        expected_temperature = self.weather_data[0].temperature

        # Actions
        self.repository_service.store_weather_data(self.weather_data)
        date_filter = datetime(2023, 1, 1, 0, 0)
        result = self.repository_service.get_weather_data_after_date(date_filter)

        # Asserts
        self.assertEqual(len(result), len(self.weather_data))
        self.assertEqual(result[0].datetime, expected_date)
        self.assertEqual(result[0].temperature, expected_temperature)

    def test_get_electricity_price_data_after_date(self):
        # Setup
        expected_date = self.electricity_price_data[0].datetime
        expected_price = self.electricity_price_data[0].price

        # Actions
        self.repository_service.store_electricity_price_data(self.electricity_price_data)
        date_filter = datetime(2023, 1, 1, 0, 0)
        result = self.repository_service.get_electricity_price_data_after_date(date_filter)

        # Asserts
        self.assertEqual(len(result), len(self.electricity_price_data))
        self.assertEqual(result[0].datetime, expected_date)
        self.assertEqual(result[0].price, expected_price)

    def test_store_switch_data(self):
        # Setup
        switch = SwitchModel(name="Switch 1", status_calculation_logic="status_calculation_logic")
        expected_name = switch.name
        # Actions
        self.repository_service.store_switch_data(switch)
        with self.repository_service.session_maker() as session:
            stored_data = session.query(SwitchModel).all()

        # Asserts
        self.assertEqual(len(stored_data), 1)
        self.assertEqual(stored_data[0].name, expected_name)

    def test_store_switch_data_if_already_exists(self):
        # Setup
        switch = SwitchModel(name="Switch 1", status_calculation_logic="status_calculation_logic")
        duplicate_switch = SwitchModel(name="Switch 1", status_calculation_logic="new_status_calculation_logic")

        # Actions
        self.repository_service.store_switch_data(switch)

        # Asserts
        with self.assertRaises(IntegrityError):
            self.repository_service.store_switch_data(duplicate_switch)

    def test_update_switch_data(self):
        # Setup
        switch = SwitchModel(name="Switch 1", status_calculation_logic="status_calculation_logic")
        updated_switch = SwitchModel(name="Switch 1", status_calculation_logic="new_status_calculation_logic")

        # Actions
        self.repository_service.store_switch_data(switch)
        self.repository_service.update_switch_data(updated_switch)
        changed_switch = self.repository_service.get_switch("Switch 1")

        # Asserts
        self.assertEqual(changed_switch.status_calculation_logic, "new_status_calculation_logic")

    def test_update_switch_data_if_not_exists(self):
        # Setup
        switch = SwitchModel(name="Switch 1", status_calculation_logic="status_calculation_logic")
        updated_switch = SwitchModel(name="Switch 2", status_calculation_logic="new_status_calculation_logic")

        # Actions
        self.repository_service.store_switch_data(switch)

        # Asserts
        with self.assertRaises(ValueError):
            self.repository_service.update_switch_data(updated_switch)

    def test_get_switch(self):
        # Setup
        switch = SwitchModel(name="Switch 1", status_calculation_logic="status_calculation_logic")
        expected_name = switch.name

        # Actions
        self.repository_service.store_switch_data(switch)
        result = self.repository_service.get_switch("Switch 1")

        # Asserts
        self.assertEqual(result.name, expected_name)

    def test_get_switch_if_not_exists(self):
        # Setup
        switch = SwitchModel(name="Switch 1", status_calculation_logic="status_calculation_logic")

        # Actions
        self.repository_service.store_switch_data(switch)

        # Asserts
        with self.assertRaises(ValueError):
            self.repository_service.get_switch("Switch 2")
