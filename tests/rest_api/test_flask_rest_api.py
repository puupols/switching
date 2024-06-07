import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.configuration.base_configuration import BaseConfiguration
from src.rest_api.flask_rest_api import FlaskRESTAPI
from flask_smorest import Api


class TestFlaskRESTAPI(unittest.TestCase):

    @patch('src.rest_api.flask_rest_api.Api')
    @patch('src.rest_api.flask_rest_api.JWTManager')
    @patch('src.rest_api.flask_rest_api.SwitchBlueprint')
    @patch('src.rest_api.flask_rest_api.SwitchStatusBlueprint')
    @patch('src.rest_api.flask_rest_api.UserBlueprint')
    @patch('src.rest_api.flask_rest_api.Flask')
    def test_create_app(self, mock_flask, mock_switch_blueprint, mock_switch_status_blueprint, mock_user_blueprint, mock_jwt_manager, mock_api):

        # Setup
        mock_config = MagicMock(spec=BaseConfiguration)
        mock_config.get.return_value = "super_secret_key"

        mock_app = MagicMock(spec=Flask)
        mock_app.config = {}
        mock_flask.return_value = mock_app
        mock_api_instance = MagicMock(spec=Api)
        mock_api.return_value = mock_api_instance

        # Actions
        api_instance = FlaskRESTAPI(mock_config)

        # Asserts
        mock_flask.assert_called_once()

        # Check if app configurations are set correctly
        self.assertEqual(mock_app.config["PROPAGATE_EXCEPTIONS"], True)
        self.assertEqual(mock_app.config["API_TITLE"], "Switching REST API")
        self.assertEqual(mock_app.config["API_VERSION"], "V1")
        self.assertEqual(mock_app.config["OPENAPI_VERSION"], "3.0.3")
        self.assertEqual(mock_app.config["OPENAPI_URL_PREFIX"], "/")
        self.assertEqual(mock_app.config["OPENAPI_SWAGGER_UI_PATH"], "/swagger-ui")
        self.assertEqual(mock_app.config["OPENAPI_SWAGGER_UI_URL"], "https://cdn.jsdelivr.net/npm/swagger-ui-dist/")
        self.assertEqual(mock_app.config["JWT_SECRET_KEY"], "super_secret_key")

        # Check if blueprints are registered
        mock_api_instance.register_blueprint.assert_any_call(mock_switch_blueprint)
        mock_api_instance.register_blueprint.assert_any_call(mock_user_blueprint)
        mock_api_instance.register_blueprint.assert_any_call(mock_switch_status_blueprint)

        # Check if JWTManager is initialized
        mock_jwt_manager.assert_called_once_with(mock_app)

    @patch('src.rest_api.flask_rest_api.FlaskRESTAPI.create_app')
    def test_init(self, mock_create_app):
        # Setup
        mock_config = MagicMock(spec=BaseConfiguration)

        # Actions
        api_instance = FlaskRESTAPI(mock_config)

        # Asserts
        # Check if configuration is set
        self.assertEqual(api_instance.configuration, mock_config)

        # Check if create_app is called during initialization
        mock_create_app.assert_called_once()

    @patch('src.rest_api.flask_rest_api.FlaskRESTAPI.create_app')
    def test_run_app(self, mock_create_app):
        # Setup
        mock_config = MagicMock(spec=BaseConfiguration)
        mock_app = MagicMock(spec=Flask)
        mock_create_app.return_value = mock_app

        # Actions
        api_instance = FlaskRESTAPI(mock_config)
        api_instance.run_app()

        # Asserts
        # Check if Flask app run is called
        mock_app.run.assert_called_once_with(debug=False)