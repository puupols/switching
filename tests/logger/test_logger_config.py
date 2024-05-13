import unittest
from unittest.mock import patch, MagicMock
import json
from src.logger.logger_config import setup_logger


class TestSetupLogger(unittest.TestCase):

    @patch('builtins.open', MagicMock())
    @patch('json.load')
    @patch('logging.config.dictConfig')
    def test_setup_logger_success(self, mock_dict_config, mock_json_load):
        # Setup
        config_data = json.loads('{"some": "json", "file": "here"}')
        mock_json_load.return_value = config_data
        setup_logger()

        # Assert
        mock_dict_config.assert_called_once_with(config_data)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_setup_logger_file_not_found(self, mock_open):
        with self.assertRaises(FileNotFoundError):
            setup_logger()

    @patch('builtins.open', MagicMock())
    @patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "doc", 0))
    def test_setup_logger_invalid_json(self, mock_json_load):
        with self.assertRaises(json.JSONDecodeError):
            setup_logger()
