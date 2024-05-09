import unittest
from unittest.mock import patch
from src import app


class TestApp(unittest.TestCase):
    @patch('src.logger.logger_config.setup_logger')
    @patch('inject.configure')
    @patch('src.main.Main.run')
    @patch('src.main.Main.__init__', return_value=None)
    def test_main_function_calls(self, mock_main_init, mock_main_run, mock_inject_configure, mock_setup_logger):
        # Actions
        app.main()

        # Asserts
        mock_setup_logger.assert_called_once()
        mock_inject_configure.assert_called_once()
        from src.injections.injections import app_injection_configuration
        mock_inject_configure.assert_called_once_with(app_injection_configuration)
        mock_main_init.assert_called_once()
        mock_main_run.assert_called_once()
