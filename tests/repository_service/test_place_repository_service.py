import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import clear_mappers
from src.configuration.base_configuration import BaseConfiguration
from src.repository_service.place_repository_service import PlaceRepositoryService
from src.place_service.models.place_model import PlaceModel
from src.location_service.models.location_model import LocationModel


class TestPlaceRepositoryService(unittest.TestCase):

    def setUp(self):
        self.mock_configuration = MagicMock(spec=BaseConfiguration)
        self.mock_configuration.get.return_value = "sqlite:///:memory:"
        self.place_repository_service = PlaceRepositoryService(configuration=self.mock_configuration)
        self.place_repository_service.create_database()
        self.place = PlaceModel(name="Place 1", user_id=1, location_id=1, description="test description")

    def tearDown(self):
        self.place_repository_service.metadata.drop_all(self.place_repository_service.engine)
        clear_mappers()
        self.place_repository_service.engine.dispose()

    def test_store_place_data(self):
        # Setup
        expected_name = self.place.name
        # Actions
        self.place_repository_service.store_place_data(self.place)
        with self.place_repository_service.session_maker() as session:
            stored_data = session.query(PlaceModel).all()

        # Asserts
        self.assertEqual(len(stored_data), 1)
        self.assertEqual(stored_data[0].name, expected_name)

    def test_get_place(self):
        # Setup
        expected_name = self.place.name

        # Actions
        self.place_repository_service.store_place_data(self.place)
        result = self.place_repository_service.get_place("Place 1", 1)

        # Asserts
        self.assertEqual(result.name, expected_name)

    def test_get_place_and_switches(self):
        # Setup
        expected_name = self.place.name

        # Actions
        self.place_repository_service.store_place_data(self.place)
        result = self.place_repository_service.get_place_and_switches("Place 1", 1)

        # Asserts
        self.assertEqual(result.name, expected_name)

    def test_get_all_paces_and_switches_for_user(self):
        # Setup
        place_two = PlaceModel(name="Place 2", user_id=1, location_id=1, description="test description")
        expected_name = self.place.name
        expected_name_two = place_two.name

        # Actions
        self.place_repository_service.store_place_data(self.place)
        self.place_repository_service.store_place_data(place_two)
        result = self.place_repository_service.get_all_places_and_switches_for_user(1)

        # Asserts
        self.assertEqual(result[0].name, expected_name)
        self.assertEqual(result[1].name, expected_name_two)
        self.assertEqual(len(result), 2)

    def test_delete_place(self):

        # Actions
        self.place_repository_service.store_place_data(self.place)
        self.place_repository_service.delete_place("Place 1", 1)
        with self.place_repository_service.session_maker() as session:
            stored_data = session.query(PlaceModel).all()

        # Asserts
        self.assertEqual(len(stored_data), 0)