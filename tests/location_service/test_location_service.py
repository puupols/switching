import unittest
from unittest.mock import Mock
from src.location_service.configuration_based_location_service import ConfigurationBasedLocationService


class TestLocationService(unittest.TestCase):

    def setUp(self):
        self.mock_configuration = Mock()
        self.mock_configuration.get.side_effect = lambda key: {'location_latitude': 555, 'location_longitude': 222}[key]
        self.mock_location_service = ConfigurationBasedLocationService(self.mock_configuration)

    def test_get_location(self):
        # Action
        location = self.mock_location_service.get_location()

        # Assert
        self.assertEqual(location, (555, 222))
        self.mock_configuration.get.assert_any_call('location_latitude')
        self.mock_configuration.get.assert_any_call('location_longitude')
