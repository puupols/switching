import unittest
from unittest.mock import Mock, patch
from src.switch_service.switch_service import SwitchService


class TestSwitchService(unittest.TestCase):

    def setUp(self):
        self.mock_config = Mock()
        self.mock_weather_service = Mock()
        self.mock_electricity_price_service = Mock()
        self.switch_service = SwitchService(self.mock_config, self.mock_weather_service,
                                            self.mock_electricity_price_service)

    @patch('src.switch_service.switch_service.importlib.util')
    @patch('src.switch_service.switch_service.sys')
    def test_load_module_success(self, mock_sys, mock_importlib):
        # Setup
        mock_spec = Mock()
        mock_module = Mock()
        mock_importlib.spec_from_file_location.return_value = mock_spec
        mock_importlib.module_from_spec.return_value = mock_module
        mock_spec.loader.exec_module.return_value = None

        # Actions
        self.mock_config.get.return_value = ['valid_switch']
        result = self.switch_service._load_module('valid_switch')

        # Asserts
        self.assertEqual(result, mock_module)
        mock_spec.loader.exec_module.assert_called_once()

    @patch('src.switch_service.switch_service.importlib.util')
    def test_load_module_invalid_switch_name(self, mock_importlib):
        self.mock_config.get.return_value = ['valid_switch']
        with self.assertRaises(ValueError):
            self.switch_service._load_module('invalid_switch')

    @patch('src.switch_service.switch_service.SwitchService._load_module')
    def test_get_switch_status_success(self, mock_load_module):
        # Setup
        mock_switch_module = Mock()
        mock_switch_module.get_switch_status.return_value = 'ON'
        mock_load_module.return_value = mock_switch_module

        # Actions
        status = self.switch_service.get_switch_status('valid_switch')

        # Asserts
        self.assertEqual(status, 'ON')

    @patch('src.switch_service.switch_service.SwitchService._load_module')
    def test_get_switch_status_fail(self, mock_load_module):
        # Setup
        mock_load_module.side_effect = Exception('Test Exception')

        # Actions
        status = self.switch_service.get_switch_status('invalid_switch')

        # Asserts
        self.assertEqual(status, 'ERROR')
