from src.switch_service.switch_service import SwitchService
from src.configuration.base_configuration import BaseConfiguration
import inject
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth


class FlaskRESTAPI:
    """
    A Flask-based REST API class for managing switch services with HTTP basic authentication.

    This class creates a Flask application that exposes REST endpoints to control and monitor
    switch statuses through an authenticated interface. The API uses basic authentication and
    integrates a switch service for actual switch status handling.

    Attributes:
        switch_service (SwitchService): The service responsible for managing switches.
        configuration (BaseConfiguration): Configuration service for accessing API credentials.
        app (Flask): The Flask application object that handles API requests.
        auth (HTTPBasicAuth): HTTP basic authentication handler.
    """
    REST_USERNAME_CONFIG_NAME = 'rest_username'
    REST_PASSWORD_CONFIG_NAME = 'rest_password'

    @inject.autoparams()
    def __init__(self, switch_service: SwitchService, configuration: BaseConfiguration):
        """
        Initializes the FlaskRESTAPI with necessary services and configurations.

        Args:
            switch_service (SwitchService): The service responsible for switch operations.
            configuration (BaseConfiguration): Configuration object to retrieve API credentials.

        Sets up the Flask application and routes, and configures basic authentication.
        """
        self.switch_service = switch_service
        self.configuration = configuration
        self.app = Flask('__name__')
        self.auth = HTTPBasicAuth()
        self.setup_routes()
        self.username = configuration.get(self.REST_USERNAME_CONFIG_NAME)
        self.password = configuration.get(self.REST_PASSWORD_CONFIG_NAME)

    def run_app(self):
        """
        Starts the Flask application.

        Runs the Flask app in production mode with debug features turned off.
        """
        self.app.run(debug=False)

    def setup_routes(self):
        """
        Sets up the routes for the Flask application with authentication.

        Defines the routes and their corresponding authentication and handlers within the Flask application.
        """
        @self.auth.verify_password
        def verify_password(username, password):
            """
            Verifies the provided username and password against configured values.

            Args:
                username (str): The username provided by the client.
                password (str): The password provided by the client.

            Returns:
                str: The username if authentication is successful, None otherwise.
            """
            if username == self.username and password == self.password:
                return username

        @self.app.route('/status')
        @self.auth.login_required
        def get_switch_status():
            """
            Endpoint to get the status of a switch.

            Retrieves the status of a switch specified by the 'name' query parameter in the request.

            Returns:
                str: The current status of the switch.
            """
            switch_name = request.args.get('name')
            return self.switch_service.get_switch_status(switch_name)
