import unittest
from unittest.mock import MagicMock
from flask_testing import TestCase
from flask import Flask
from src.switch_service.switch_service import SwitchService
from src.configuration.base_configuration import BaseConfiguration
from src.rest_api.flask_rest_api import FlaskRESTAPI
import base64


class TestFlaskRESTAPI(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.mock_switch_service = MagicMock(spec=SwitchService)
        self.mock_configuration = MagicMock(spec=BaseConfiguration)
        self.mock_configuration.get.side_effect = lambda key: {'rest_username': 'user', 'rest_password': 'pass'}.get(
            key, None)

        self.api = FlaskRESTAPI(self.mock_switch_service, self.mock_configuration)
        self.client = self.api.app.test_client()

    def test_authentication_success(self):
        # Actions
        response = self.client.get('/status', headers=self._get_basic_auth_headers('user', 'pass'))

        # Asserts
        self.assertEqual(response.status_code, 200)

    def test_authentication_failure(self):
        # Actions
        response = self.client.get('/status', headers=self._get_basic_auth_headers('baduser', 'badpass'))

        # Asserts
        self.assertEqual(response.status_code, 401)

    def test_get_switch_status(self):
        # Setup
        expected_status = 'ON'
        self.mock_switch_service.get_switch_status.return_value = expected_status

        # Actions
        response = self.client.get('/status?name=mySwitch', headers=self._get_basic_auth_headers('user', 'pass'))

        # Asserts
        self.assertEqual(response.data.decode(), expected_status)
        self.mock_switch_service.get_switch_status.assert_called_once_with('mySwitch')

    def _get_basic_auth_headers(self, username, password):
        # Helper method to create HTTP Basic Auth headers
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode('utf-8')
        return {'Authorization': f'Basic {credentials}'}
