import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_jwt_extended import create_access_token, JWTManager
from flask_smorest import Api
from src.switch_service.switch_service import SwitchService
from src.rest_api.resources.switch import Switch, blp
from src.switch_service.models.switch_model import SwitchModel
import inject

class TestSwitch(unittest.TestCase):

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

        self.switch_view = Switch(switch_service=self.mock_switch_service)

        with self.app.app_context():
            self.access_token = create_access_token(identity='test_user')

    def tearDown(self):
        inject.clear()

    @patch('src.rest_api.resources.switch.jwt_required')
    def test_post_switch_success(self, mock_jwt_required):
        # Setup
        switch_data = {
            "name": "test_switch",
            "uuid": "uuid_1",
            "status_calculation_logic": "some logic",
            "place_id": 1
        }

        mock_jwt_required.return_value = lambda fn: fn
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Actions
        response = self.client.post("/switch", json=switch_data, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, switch_data)

    @patch('src.rest_api.resources.switch.jwt_required')
    def test_post_switch_failure(self, mock_jwt_required):
        # Setup
        switch_data = {
            "name": "test_switch",
            "uuid": "uuid_1",
            "status_calculation_logic": "some logic",
            "place_id": 1
        }
        self.mock_switch_service.store_switch_data.side_effect = Exception("Some error")
        mock_jwt_required.return_value = lambda fn: fn
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Actions
        response = self.client.post("/switch", json=switch_data, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 500)

    @patch('src.rest_api.resources.switch.jwt_required')
    def test_post_switch_exists(self, mock_jwt_required):
        # Setup
        switch_data = {
            "name": "test_switch",
            "uuid": "uuid_1",
            "status_calculation_logic": "some logic",
            "place_id": 1
        }
        self.mock_switch_service.store_switch_data.side_effect = ValueError("Switch already exists")
        mock_jwt_required.return_value = lambda fn: fn
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Actions
        response = self.client.post("/switch", json=switch_data, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 500)

    @patch('src.rest_api.resources.switch.jwt_required')
    def test_put_switch_success(self, mock_jwt_required):
        # Setup
        switch_data = {
            "name": "test_switch",
            "uuid": "uuid_1",
            "status_calculation_logic": "some logic",
            "place_id": 1
        }
        mock_jwt_required.return_value = lambda fn: fn
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Actions
        response = self.client.put("/switch", json=switch_data, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, switch_data)

    @patch('src.rest_api.resources.switch.jwt_required')
    def test_put_switch_failure(self, mock_jwt_required):
        # Setup
        switch_data = {
            "name": "test_switch",
            "uuid": "uuid_1",
            "status_calculation_logic": "some logic",
            "place_id": 1
        }
        self.mock_switch_service.update_switch_data.side_effect = ValueError("Switch not found")
        mock_jwt_required.return_value = lambda fn: fn
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Actions
        response = self.client.put("/switch", json=switch_data, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 404)

    @patch('src.rest_api.resources.switch.jwt_required')
    def test_get_switch_success(self, mock_jwt_required):
        # Setup
        switch_data = {
            "uuid": "uuid_1"
        }
        mock_switch = SwitchModel(name="test_switch", uuid="uuid_1", status_calculation_logic="some logic", place_id=1)
        self.mock_switch_service.get_switch_data_for_user.return_value = mock_switch
        mock_jwt_required.return_value = lambda fn: fn
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Actions
        response = self.client.get("/switch", json=switch_data, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "name": "test_switch",
            "uuid": "uuid_1",
            'status': None,
            "status_calculation_logic": "some logic",
            "place_id": 1
        })

    @patch('src.rest_api.resources.switch.jwt_required')
    def test_get_switch_failure(self, mock_jwt_required):
        # Setup
        switch_data = {
            "uuid": "uuid_1"
        }
        self.mock_switch_service.get_switch_data_for_user.side_effect = ValueError("Switch not found")
        mock_jwt_required.return_value = lambda fn: fn
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Actions
        response = self.client.get("/switch", json=switch_data, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 404)

    @patch('src.rest_api.resources.switch.jwt_required')
    def test_delete_switch_success(self, mock_jwt_required):
        # Setup
        switch_data = {
            "uuid": "uuid_1"
        }
        mock_jwt_required.return_value = lambda fn: fn
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        self.mock_switch_service.delete_switch.return_value = None

        # Actions
        response = self.client.delete("/switch", json=switch_data, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, switch_data)

    @patch('src.rest_api.resources.switch.jwt_required')
    def test_delete_switch_failure(self, mock_jwt_required):
        # Setup
        switch_data = {
            "uuid": "uuid_1"
        }
        mock_jwt_required.return_value = lambda fn: fn
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        self.mock_switch_service.delete_switch.side_effect = ValueError("Switch not found")

        # Actions
        response = self.client.delete("/switch", json=switch_data, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 404)
