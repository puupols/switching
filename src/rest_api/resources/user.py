import inject
import logging

from datetime import timedelta
from flask.views import MethodView
from src.configuration.base_configuration import BaseConfiguration
from flask_smorest import Blueprint, abort
from ..schemas import UserSchema
from flask_jwt_extended import create_access_token

blp = Blueprint("users", __name__, description="Operations with users")


@blp.route("/login")
class Login(MethodView):
    """
    A class to handle user login operations through a RESTful API endpoint.

    Attributes:
        REST_USERNAME_CONFIG_NAME (str): Configuration name for REST username.
        REST_PASSWORD_CONFIG_NAME (str): Configuration name for REST password.

    Methods:
        __init__(configuration: BaseConfiguration):
            Initializes the Login class with the provided configuration.

        post(user_data: dict) -> dict:
            Handles POST requests to authenticate a user and generate an access token.
    """
    REST_USERNAME_CONFIG_NAME = 'rest_username'
    REST_PASSWORD_CONFIG_NAME = 'rest_password'

    @inject.autoparams()
    def __init__(self, configuration: BaseConfiguration):
        """
        Initializes the Login instance with the provided configuration.

        Args:
            configuration (BaseConfiguration): The configuration object containing user credentials.
        """
        self.configuration = configuration
        self.logger = logging.getLogger(__name__)

    @blp.arguments(UserSchema)
    def post(self, user_data):
        """
        Handles POST requests to authenticate a user and generate an access token.

        Args:
            user_data (dict): The data for the user, containing username and password.

        Returns:
            dict: A dictionary containing the access token if authentication is successful.

        Raises:
            HTTPException: If the provided credentials are invalid.
        """
        if (user_data["username"] == self.configuration.get(self.REST_USERNAME_CONFIG_NAME) and
                user_data["password"] == self.configuration.get(self.REST_PASSWORD_CONFIG_NAME)):
            access_token = create_access_token(user_data["username"], expires_delta=timedelta(hours=1))
            self.logger.info("User logged in!")
            return {'access_token': access_token}
        else:
            self.logger.warning("User login incorrect!")
            abort(401, message="Invalid credentials")