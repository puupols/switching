import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import clear_mappers
from src.configuration.base_configuration import BaseConfiguration
from src.repository_service.location_repository_service import LocationRepositoryService
from src.location_service.models.location_model import LocationModel


class TestLocationRepositoryService(unittest.TestCase):

    def setUp(self):
        self.mock_configuration = MagicMock(spec=BaseConfiguration)
        self.mock_configuration.get.return_value = "sqlite:///:memory:"
        self.locatrion_repository_service = LocationRepositoryService(configuration=self.mock_configuration)
        self.locatrion_repository_service.create_database()
        self.location = LocationModel(latitude=1.0, longitude=1.0)

    def tearDown(self):
        self.locatrion_repository_service.metadata.drop_all(self.locatrion_repository_service.engine)
        clear_mappers()
        self.locatrion_repository_service.engine.dispose()

    def test_store_location_data(self):
        # Setup
        expected_latitude = self.location.latitude
        expected_longitude = self.location.longitude

        # Actions
        self.locatrion_repository_service.store_location_data(self.location)
        with self.locatrion_repository_service.session_maker() as session:
            stored_data = session.query(LocationModel).all()

        # Asserts
        self.assertEqual(len(stored_data), 1)
        self.assertEqual(stored_data[0].latitude, expected_latitude)
        self.assertEqual(stored_data[0].longitude, expected_longitude)

    def test_store_location_data_already_exists(self):
        # Setup
        expected_latitude = self.location.latitude
        expected_longitude = self.location.longitude

        # Actions
        self.locatrion_repository_service.store_location_data(self.location)
        self.locatrion_repository_service.store_location_data(self.location)
        with self.locatrion_repository_service.session_maker() as session:
            stored_data = session.query(LocationModel).all()

        # Asserts
        self.assertEqual(len(stored_data), 1)
        self.assertEqual(stored_data[0].latitude, expected_latitude)
        self.assertEqual(stored_data[0].longitude, expected_longitude)

    def test_get_location(self):
        # Setup
        expected_latitude = self.location.latitude
        expected_longitude = self.location.longitude

        # Actions
        self.locatrion_repository_service.store_location_data(self.location)
        result = self.locatrion_repository_service.get_location(1.0, 1.0)

        # Asserts
        self.assertEqual(result.latitude, expected_latitude)
        self.assertEqual(result.longitude, expected_longitude)
