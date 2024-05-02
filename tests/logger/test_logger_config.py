import unittest
from unittest.mock import patch, MagicMock
import logging
from src.logger.logger_config import setup_logger


class TestLoggerSetup(unittest.TestCase):
    @patch('logging.FileHandler')
    @patch('logging.StreamHandler')
    def test_setup_logger(self, mock_stream_handler, mock_file_handler):
        # Create mock handlers
        mock_stream = MagicMock()
        mock_stream_handler.return_value = mock_stream

        mock_file = MagicMock()
        mock_file_handler.return_value = mock_file

        # Call the function to set up the logger
        setup_logger()

        # Get the root logger to check its configuration
        root_logger = logging.getLogger()

        # Test logger level
        self.assertEqual(root_logger.level, logging.INFO, "Root logger level should be INFO")

        # Test handlers setup
        self.assertTrue(mock_stream_handler.called, "Stream handler should be set up")
        self.assertTrue(mock_file_handler.called, "File handler should be set up")

        # Test handlers' levels
        self.assertEqual(mock_stream.setLevel.call_args[0][0], logging.INFO, "Stream handler level should be INFO")
        self.assertEqual(mock_file.setLevel.call_args[0][0], logging.INFO, "File handler level should be INFO")

        # Test correct formatter set
        expected_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        stream_formatter = mock_stream.setFormatter.call_args[0][0]._fmt
        file_formatter = mock_file.setFormatter.call_args[0][0]._fmt
        self.assertEqual(stream_formatter, expected_format, "Stream formatter should have the correct format")
        self.assertEqual(file_formatter, expected_format, "File formatter should have the correct format")

        # Ensure exactly two handlers are added
        self.assertEqual(len(root_logger.handlers), 2, "Two handlers should be added to the root logger")
