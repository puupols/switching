import inject
import unittest
from unittest.mock import Mock, patch, mock_open
from src.switch_service.switch_service import SwitchService
from src.configuration.base_configuration import BaseConfiguration
from src.switch_service.models.switch_model import SwitchModel


class TestSwitchService(unittest.TestCase):

    def setUp(self):
        self.mock_config = Mock(spec=BaseConfiguration)
        self.mock_weather_service = Mock()
        self.mock_repository_service = Mock()
        self.mock_electricity_price_service = Mock()
        self.mock_logger = Mock()
        with patch('src.switch_service.switch_service.logging.getLogger', return_value=self.mock_logger):
            self.switch_service = SwitchService(self.mock_config, self.mock_weather_service,
                                                self.mock_electricity_price_service, self.mock_repository_service)

    def tearDown(self):
        inject.clear()

    def test_get_allowed_scope(self):
        scope = self.switch_service._get_allowed_scope()
        self.assertIn('datetime', scope['__builtins__'])
        self.assertIn('print', scope['__builtins__'])
        self.assertIn('get_weather_data_after_date', scope)
        self.assertIn('get_electricity_price_data_after_date', scope)

    def test_get_switch_status_calculation_logic_when_switch_exists(self):
        # Setup
        mock_switch = Mock()
        mock_switch.status_calculation_logic = 'mock_logic'
        self.mock_repository_service.get_switch.return_value = mock_switch

        # Actions
        result = self.switch_service._get_switch_status_calculation_logic('test_switch')

        # Asserts
        self.assertEqual(result, 'mock_logic')
        self.mock_repository_service.get_switch.assert_called_once_with('test_switch')

    def test_get_switch_status_calculation_logic_when_switch_does_not_exist(self):
        # Setup
        self.mock_repository_service.get_switch.return_value = None

        # Actions
        result = self.switch_service._get_switch_status_calculation_logic('test_switch')

        # Asserts
        self.assertIsNone(result)
        self.mock_repository_service.get_switch.assert_called_once_with('test_switch')

    @patch.object(SwitchService, '_get_switch_status_calculation_logic',
                  return_value="def get_switch_status(): return 'ON'")
    def test_get_switch_status_success(self, mock_get_logic):
        status = self.switch_service.get_switch_status('test_switch')
        self.assertEqual(status, 'ON')

    @patch.object(SwitchService, '_get_switch_status_calculation_logic',
                  return_value="def get_switch_status(): raise Exception('error')")
    def test_get_switch_status_error(self, mock_get_logic):
        status = self.switch_service.get_switch_status('test_switch')
        self.assertEqual(status, SwitchModel.SWITCH_VALUE_IF_ERROR_OCCURRED)
        self.mock_logger.error.assert_called()

    @patch.object(SwitchService, '_get_switch_status_calculation_logic', return_value=None)
    def test_get_switch_status_not_found(self, mock_get_logic):
        status = self.switch_service.get_switch_status('non_existent_switch')
        self.assertEqual(status, SwitchModel.SWITCH_VALUE_IF_SWITCH_NOT_IMPLEMENTED)
        self.mock_logger.error.assert_called()

    def test_store_switch_data(self):
        # Setup
        switch_data = SwitchModel(name='test_switch', status_calculation_logic='mock_logic')

        # Actions
        self.switch_service.store_switch_data(switch_data)

        # Asserts
        self.mock_repository_service.store_switch_data.assert_called_once_with(switch_data)

    def test_update_switch_data(self):
        # Setup
        switch_data = SwitchModel(name='test_switch', status_calculation_logic='mock_logic')

        # Actions
        self.switch_service.update_switch_data(switch_data)

        # Asserts
        self.mock_repository_service.update_switch_data.assert_called_once_with(switch_data)