import json
import unittest
from unittest.mock import mock_open, patch
from src.configuration.file_configuration import FileConfiguration


class TestFileConfiguration(unittest.TestCase):

    def setUp(self):
        # Mock configuration data
        self.config_data = {"location_service": "configuration_file","weather_service": "open_meteo"}
        # Mock file content as a JSON string
        self.file_content = json.dumps(self.config_data)

    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_initialization_without_file(self, mock_file):
        with self.assertRaises(json.JSONDecodeError):
            FileConfiguration()

    @patch('builtins.open', new_callable=mock_open, read_data='not a json')
    def test_initialization_with_malformed_json(self, mock_file):
        with self.assertRaises(json.JSONDecodeError):
            FileConfiguration()

    @patch('builtins.open', new_callable=mock_open)
    def test_initialization_and_get_data(self, mock_file):
        # Setting the mock to use the setup file content
        mock_file.return_value.read.return_value = self.file_content
        configuration = FileConfiguration()
        # Testing the get method to ensure it correctly fetches values
        self.assertEqual(configuration.get('location_service'), 'configuration_file')
        # Testing for a non-existing key
        self.assertIsNone(configuration.get('non_existing_key'))
