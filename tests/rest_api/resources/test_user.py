import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from src.configuration.base_configuration import BaseConfiguration
from src.rest_api.resources.user import Login, blp
import inject


class TestLogin(unittest.TestCase):

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

        self.mock_configuration = MagicMock()

        def configure_injector(binder):
            binder.bind(BaseConfiguration, self.mock_configuration)
        inject.configure(configure_injector)

        self.login_view = Login(configuration=self.mock_configuration)

        self.mock_configuration.get.side_effect = lambda key: {
            'rest_username': 'test_user',
            'rest_password': 'test_password'
        }[key]

    def tearDown(self):
        inject.clear()

    @patch('src.rest_api.resources.user.UserSchema')
    def test_login_success(self, mock_schema):
        # Setup
        mock_schema.return_value.load.return_value = {"username": "test_user", "password": "test_password"}

        # Actions
        response = self.client.post("/login", json={"username": "test_user", "password": "test_password"})

        # Asserts
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)

    @patch('src.rest_api.resources.user.UserSchema')
    def test_login_failure(self, mock_schema):
        # Setup
        mock_schema.return_value.load.return_value = {"username": "wrong_user", "password": "wrong_password"}

        # Actions
        response = self.client.post("/login", json={"username": "wrong_user", "password": "wrong_password"})

        # Asserts
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid credentials", response.json["message"])
