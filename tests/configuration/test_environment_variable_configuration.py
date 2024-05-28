import unittest
from unittest.mock import patch
from src.configuration.base_configuration import BaseConfiguration
from src.configuration.environment_variable_configuration import EnvironmentVariableConfiguration
import os


class TestEnvironmentVariableConfiguration(unittest.TestCase):

    def setUp(self):
        self.config = EnvironmentVariableConfiguration()

    @patch('dotenv.load_dotenv')
    def test_init_loads_dotenv(self, mock_load_dotenv):
        # Actions
        config = EnvironmentVariableConfiguration()

        # Asserts
        mock_load_dotenv.assert_called_once()

    @patch('os.getenv')
    def test_get_existing_key(self, mock_getenv):
        # Setup
        mock_getenv.return_value = 'value'

        # Actions
        result = self.config.get('key')

        # Asserts
        mock_getenv.assert_called_with('KEY', None)
        self.assertEqual(result, 'value')

    @patch('os.getenv')
    def test_get_non_existing_key_with_default(self, mock_getenv):
        # Setup
        mock_getenv.return_value = 'default_value'

        # Actions
        result = self.config.get('non_existing_key', default='default_value')

        # Asserts
        mock_getenv.assert_called_with('NON_EXISTING_KEY', 'default_value')
        self.assertEqual(result, 'default_value')

    @patch('os.getenv')
    def test_get_as_list_existing_key(self, mock_getenv):
        # Setup
        mock_getenv.return_value = 'value1,value2,value3'

        # Actions
        result = self.config.get_as_list('key')

        # Asserts
        mock_getenv.assert_called_with('KEY')
        self.assertEqual(result, ['value1', 'value2', 'value3'])

    @patch('os.getenv')
    def test_get_as_list_non_existing_key_with_default(self, mock_getenv):
        # Setup
        mock_getenv.return_value = None

        # Actions
        result = self.config.get_as_list('non_existing_key', default=['default_value1', 'default_value2'])

        # Asserts
        mock_getenv.assert_called_with('NON_EXISTING_KEY')
        self.assertEqual(result, ['default_value1', 'default_value2'])

    @patch('os.getenv')
    def test_get_as_list_non_existing_key_no_default(self, mock_getenv):
        # Setup
        mock_getenv.return_value = None

        # Actions
        result = self.config.get_as_list('non_existing_key')

        # Asserts
        mock_getenv.assert_called_with('NON_EXISTING_KEY')
        self.assertEqual(result, [])
