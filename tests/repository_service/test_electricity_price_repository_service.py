import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import clear_mappers
from datetime import datetime
from src.configuration.base_configuration import BaseConfiguration
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel
from src.repository_service.electricity_price_repository_service import ElectricityPriceRepositoryService


class TestRepositoryService(unittest.TestCase):

    def setUp(self):
        self.mock_configuration = MagicMock(spec=BaseConfiguration)
        self.mock_configuration.get.return_value = "sqlite:///:memory:"
        self.electricity_price_repository_service = ElectricityPriceRepositoryService(
            configuration=self.mock_configuration)
        self.electricity_price_repository_service.create_database()

        self.electricity_price_data = [
            ElectricityPriceModel(datetime=datetime(2023, 1, 1, 12, 0), price=20.5),
        ]
        self.duplicate_electricity_price_data = [
            ElectricityPriceModel(datetime=datetime(2023, 1, 1, 12, 0), price=20.5),
            ElectricityPriceModel(datetime=datetime(2023, 1, 1, 12, 0), price=35.0),
        ]

    def tearDown(self):
        self.electricity_price_repository_service.metadata.drop_all(self.electricity_price_repository_service.engine)
        clear_mappers()
        self.electricity_price_repository_service.engine.dispose()

    def test_store_electricity_price_data(self):
        # Setup
        expected_price = self.electricity_price_data[0].price

        # Actions
        self.electricity_price_repository_service.store_electricity_price_data(self.electricity_price_data)
        with self.electricity_price_repository_service.session_maker() as session:
            stored_data = session.query(ElectricityPriceModel).all()

        # Asserts
        self.assertEqual(len(stored_data), len(self.electricity_price_data))
        self.assertEqual(stored_data[0].price, expected_price)

    def test_update_electricity_price_data_if_it_exists(self):
        # Setup
        expected_price = self.duplicate_electricity_price_data[1].price

        # Actions
        self.electricity_price_repository_service.store_electricity_price_data(self.duplicate_electricity_price_data)
        with self.electricity_price_repository_service.session_maker() as session:
            stored_data = session.query(ElectricityPriceModel).all()

        # Asserts

        self.assertEqual(stored_data[0].price, expected_price)

    def test_get_electricity_price_data_after_date(self):
        # Setup
        expected_date = self.electricity_price_data[0].datetime
        expected_price = self.electricity_price_data[0].price

        # Actions
        self.electricity_price_repository_service.store_electricity_price_data(self.electricity_price_data)
        date_filter = datetime(2023, 1, 1, 0, 0)
        result = self.electricity_price_repository_service.get_electricity_price_data_after_date(date_filter)

        # Asserts
        self.assertEqual(len(result), len(self.electricity_price_data))
        self.assertEqual(result[0].datetime, expected_date)
        self.assertEqual(result[0].price, expected_price)
