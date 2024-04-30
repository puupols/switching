from src.switch_service.switch_service import SwitchService
from src.configuration.base_configuration import BaseConfiguration
import inject
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth


class FlaskRESTAPI:

    @inject.autoparams()
    def __init__(self, switch_service: SwitchService, configuration: BaseConfiguration):
        self.switch_service = switch_service
        self.configuration = configuration
        self.app = Flask('__name__')
        self.auth = HTTPBasicAuth()
        self.setup_routes()
        self.username = configuration.get('rest_username')
        self.password = configuration.get('rest_password')


    def run_app(self):
        self.app.run(debug=False)

    def setup_routes(self):

        @self.auth.verify_password
        def verify_password(username, password):
            if username == self.username and password == self.password:
                return username

        @self.app.route('/status')
        @self.auth.login_required
        def get_switch_status():
            switch_name = request.args.get('name')
            return self.switch_service.get_switch_status(switch_name)
