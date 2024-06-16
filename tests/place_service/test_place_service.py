import inject
import unittest
from unittest.mock import Mock, patch
from src.place_service.place_service import PlaceService
from src.place_service.models.place_model import PlaceModel


class TestPlaceService(unittest.TestCase):

    def setUp(self):
        self.mock_repository_service = Mock()
        self.mock_logger = Mock()
        with patch('src.switch_service.switch_service.logging.getLogger', return_value=self.mock_logger):
            self.switch_service = PlaceService(self.mock_repository_service)

    def tearDown(self):
        inject.clear()

    def test_store_place_data(self):
        # Setup
        place_data = PlaceModel(name='test_place', description="test description", user_id='1', location_id='1')

        # Actions
        self.switch_service.store_place_data(place_data)

        # Asserts
        self.mock_repository_service.store_place_data.assert_called_once_with(place_data)

    def test_get_place(self):
        # Setup
        place_data = PlaceModel(name='test_place', description="test description", user_id='1', location_id='1')

        # Actions
        self.switch_service.get_place(place_data.name, place_data.user_id)

        # Asserts
        self.mock_repository_service.get_place.assert_called_once_with(place_data.name, place_data.user_id)

    def test_get_place_and_switches(self):
        # Setup
        place_data = PlaceModel(name='test_place', description="test description", user_id='1', location_id='1')

        # Actions
        self.switch_service.get_place_and_switches(place_data.name, place_data.user_id)

        # Asserts
        self.mock_repository_service.get_place_and_switches.assert_called_once_with(place_data.name, place_data.user_id)

    def test_get_all_places_and_switches_for_user(self):
        # Setup
        user_id = '1'

        # Actions
        self.switch_service.get_all_places_and_switches_for_user(user_id)

        # Asserts
        self.mock_repository_service.get_all_places_and_switches_for_user.assert_called_once_with(user_id)

    def test_delete_place(self):
        # Setup
        place_data = PlaceModel(name='test_place', description="test description", user_id='1', location_id='1')

        # Actions
        self.switch_service.delete_place(place_data.name, place_data.user_id)

        # Asserts
        self.mock_repository_service.delete_place.assert_called_once_with(place_data.name, place_data.user_id)
