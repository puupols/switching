import unittest
from unittest.mock import Mock, patch, mock_open
from src.switch_service.switch_service import SwitchService


class TestSwitchService(unittest.TestCase):

    def setUp(self):
        self.mock_config = Mock()
        self.mock_weather_service = Mock()
        self.mock_electricity_price_service = Mock()
        self.mock_logger = Mock()
        with patch('src.switch_service.switch_service.logging.getLogger', return_value=self.mock_logger):
            self.switch_service = SwitchService(self.mock_config, self.mock_weather_service,
                                                self.mock_electricity_price_service)

    def test_get_allowed_scope(self):
        scope = self.switch_service._get_allowed_scope()
        self.assertIn('datetime', scope['__builtins__'])
        self.assertIn('print', scope['__builtins__'])
        self.assertIn('get_weather_data_after_date', scope)
        self.assertIn('get_electricity_price_data_after_date', scope)

    @patch("builtins.open", new_callable=mock_open, read_data="def get_switch_status(): return 'ON'")
    def test_get_switch_status_calculation_logic_success(self, mock_open):
        logic = self.switch_service._get_switch_status_calculation_logic('test_switch')
        self.assertEqual(logic, "def get_switch_status(): return 'ON'")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_get_switch_status_calculation_logic_not_found(self, mock_open):
        logic = self.switch_service._get_switch_status_calculation_logic('non_existent_switch')
        self.assertIsNone(logic)

    @patch.object(SwitchService, '_get_switch_status_calculation_logic', return_value="def get_switch_status(): return 'ON'")
    def test_get_switch_status_success(self, mock_get_logic):
        status = self.switch_service.get_switch_status('test_switch')
        self.assertEqual(status, 'ON')

    @patch.object(SwitchService, '_get_switch_status_calculation_logic', return_value="def get_switch_status(): raise Exception('error')")
    def test_get_switch_status_error(self, mock_get_logic):
        status = self.switch_service.get_switch_status('test_switch')
        self.assertEqual(status, SwitchService.RETURN_VALUE_IF_ERROR_OCCURRED)
        self.mock_logger.error.assert_called()

    @patch.object(SwitchService, '_get_switch_status_calculation_logic', return_value=None)
    def test_get_switch_status_not_found(self, mock_get_logic):
        status = self.switch_service.get_switch_status('non_existent_switch')
        self.assertEqual(status, SwitchService.RETURN_VALUE_IF_SWITCH_NOT_FOUND)
        self.mock_logger.error.assert_called()
