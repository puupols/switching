import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_jwt_extended import create_access_token, JWTManager
from flask_smorest import Api
from src.switch_service.switch_service import SwitchService
from src.rest_api.resources.switch_status import SwitchStatus, blp
from src.switch_service.models.switch_model import SwitchModel
import inject


class TestSwitchStatus(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config["API_TITLE"] = "Stores REST API"
        self.app.config["API_VERSION"] = "V1"
        self.app.config["OPENAPI_VERSION"] = "3.0.3"
        self.app.config["OPENAPI_URL_PREFIX"] = "/"
        self.app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
        self.app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'

        self.jwt = JWTManager(self.app)
        api = Api(self.app)
        api.register_blueprint(blp)
        self.client = self.app.test_client()

        self.mock_switch_service = MagicMock()

        def configure_injector(binder):
            binder.bind(SwitchService, self.mock_switch_service)

        inject.configure(configure_injector)

        self.switch_view = SwitchStatus(switch_service=self.mock_switch_service)

        with self.app.app_context():
            self.access_token = create_access_token(identity='test_user')

    def tearDown(self):
        inject.clear()

    @patch('src.rest_api.resources.switch_status.SwitchStatusRetrivalSchema')
    @patch('src.rest_api.resources.switch_status.jwt_required')
    def test_get_switch_status_success(self, mock_jwt_required, mock_schema):
        # Setup
        mock_jwt_required.return_value = lambda fn: fn
        self.mock_switch_service.get_switch_status.return_value = "ON"
        mock_schema.return_value.load.return_value = {"name": "test_switch"}

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Actions
        with self.app.app_context():
            response = self.client.get("/switch/status", json={"name": "test_switch"}, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "name": "test_switch",
            "status": "ON"
        })

    @patch('src.rest_api.resources.switch_status.SwitchStatusRetrivalSchema')
    @patch('src.rest_api.resources.switch_status.jwt_required')
    def test_get_switch_status_error(self, mock_jwt_required, mock_schema):
        # Setup
        mock_jwt_required.return_value = lambda fn: fn
        self.mock_switch_service.get_switch_status.return_value = SwitchModel.SWITCH_VALUE_IF_ERROR_OCCURRED
        mock_schema.return_value.load.return_value = {"name": "test_switch"}

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Actions
        with self.app.app_context():
            response = self.client.get("/switch/status", json={"name": "test_switch"}, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 500)
        self.assertIn("Could not process request for the switch with name test_switch", response.json["message"])
