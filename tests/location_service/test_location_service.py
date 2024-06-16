from unittest import TestCase
from unittest.mock import Mock
from src.location_service.location_service import LocationService


class TestLocationService(TestCase):

    def setUp(self):
        self.mock_location_repository_service = Mock()
        self.location_service = LocationService(location_repository_service=self.mock_location_repository_service)

    def test_store_location_data(self):
        # Setup
        mock_location = 'some location'

        # Action
        self.location_service.store_location_data(mock_location)

        # Asserts
        self.location_service.location_repository_service.store_location_data.assert_called_once_with(mock_location)

    def test_get_location(self):
        # Setup
        mock_latitude = 1
        mock_longitude = 2

        # Action
        self.location_service.get_location(mock_latitude, mock_longitude)

        # Asserts
        self.location_service.location_repository_service.get_location.assert_called_once_with(mock_latitude,
                                                                                               mock_longitude)

    def test_get_all_locations(self):
        # Action
        self.location_service.get_all_locations()

        # Asserts
        self.location_service.location_repository_service.get_all_locations.assert_called_once()
