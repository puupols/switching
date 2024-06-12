import inject

from src.configuration.base_configuration import BaseConfiguration
from flask import Flask
from flask_smorest import Api
from .resources.switch_status import blp as SwitchStatusBlueprint
from .resources.user import blp as UserBlueprint
from .resources.switch import blp as SwitchBlueprint
from .resources.place import blp as PlaceBlueprint
from flask_jwt_extended import JWTManager


class FlaskRESTAPI:
    """
     A class to create and run a Flask-based REST API.

    Attributes:
        REST_USERNAME_CONFIG_NAME (str): Configuration name for REST username.
        REST_PASSWORD_CONFIG_NAME (str): Configuration name for REST password.
    """

    REST_USERNAME_CONFIG_NAME = 'rest_username'
    REST_PASSWORD_CONFIG_NAME = 'rest_password'
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Switching REST API"
    API_VERSION = "V1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    @inject.autoparams()
    def __init__(self, configuration: BaseConfiguration):
        """
        Initializes the FlaskRESTAPI instance.

        Args:
            configuration (BaseConfiguration): The configuration object to initialize the API.
        """
        self.configuration = configuration
        self.app = self.create_app()

    def run_app(self):
        """
        Runs the Flask application with debug mode disabled.
        """
        self.app.run(debug=False)

    def create_app(self):
        """
        Creates and configures the Flask application.

        Configures the Flask app with the necessary settings, registers blueprints,
        and initializes JWTManager.

        Returns:
            Flask: The configured Flask application instance.
        """
        app = Flask(__name__)
        app.config["PROPAGATE_EXCEPTIONS"] = self.PROPAGATE_EXCEPTIONS
        app.config["API_TITLE"] = self.API_TITLE
        app.config["API_VERSION"] = self.API_VERSION
        app.config["OPENAPI_VERSION"] = self.OPENAPI_VERSION
        app.config["OPENAPI_URL_PREFIX"] = self.OPENAPI_URL_PREFIX
        app.config["OPENAPI_SWAGGER_UI_PATH"] = self.OPENAPI_SWAGGER_UI_PATH
        app.config["OPENAPI_SWAGGER_UI_URL"] = self.OPENAPI_SWAGGER_UI_URL

        api = Api(app)
        api.register_blueprint(SwitchStatusBlueprint)
        api.register_blueprint(UserBlueprint)
        api.register_blueprint(SwitchBlueprint)
        api.register_blueprint(PlaceBlueprint)

        app.config["JWT_SECRET_KEY"] = self.configuration.get("JWT_SECRET_KEY")
        jwt = JWTManager(app)

        return app
