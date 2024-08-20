import inject
import logging
from datetime import timedelta
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..schemas import UserSchema, UserLoginSchema
from flask_jwt_extended import create_access_token, create_refresh_token
from src.user_service.models.user_model import UserModel
from src.user_service.user_service import UserService
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

blp = Blueprint("users", __name__, description="Operations with users")


@blp.route("/user/<int:user_id>")
class UserItem(MethodView):
    """
    Class to handle to create a new user.
    """

    @inject.autoparams()
    def __init__(self, user_service: UserService):
        """
        Initializes the User class with the provided UserService.

        Arguments:
            user_service (UserService): Service class to interact
        """
        self.user_service = user_service
        self.logger = logging.getLogger(__name__)

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    @jwt_required()
    def put(self, user_data, user_id):
        """
        Updates the user data in the database.

        Arguments:
            user_id (int): The id of the user to be updated.
            user_data (dict): Dictionary containing the user data.

        Returns:
            dict: Dictionary containing the updated user data.
            Error 400: If a user with the same name already exists.
            Error 500: If an error occurred while updating user data.
        """
        if user_id != get_jwt_identity():
            self.logger.error(f"User {get_jwt_identity()} is not authorized to update user {user_id}")
            abort(401, message="You are not authorized to update this user.")
        try:
            hashed_password = self.user_service.hash_password(user_data["password"])
            user_data["password"] = hashed_password
            user_data["id"] = user_id
            user = UserModel(**user_data)
            self.user_service.update_user_data(user)
            return user_data
        except IntegrityError:
            self.logger.error(f"Error updating user data into database. A user with the same name already exists.")
            abort(400, message="A user with the same name already exists.")
        except Exception as e:
            self.logger.error(f"Error updating user data into database. Error - {e}")
            abort(500, message="An error occurred while updating user data.")

    @jwt_required()
    def delete(self, user_id):
        """
        Deletes a user object from the database based on the user id.

        Arguments:
            user_id (int): The id of the user to be deleted.

        Returns:
            Status code 200: If the user is deleted successfully.
            Error 404: If the user is not found.
            Error 500: If an error occurred while deleting user data.
        """
        if user_id != get_jwt_identity():
            self.logger.error(f"User {get_jwt_identity()} is not authorized to delete user {user_id}")
            abort(401, message="You are not authorized to delete this user.")
        try:
            self.user_service.delete_user(user_id)
        except ValueError:
            self.logger.error(f"Error deleting user data from database for the user id {user_id}.")
            abort(404, message=f"User with the id {user_id} not found.")
        except Exception as e:
            self.logger.error(f"Error deleting user data from database. Error - {e}")
            abort(500, message="An error occurred while deleting user data.")

        return {"message": f"User with user id {user_id} deleted successfully!"}, 200

    @blp.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        """
        Retrieves the user data from the database.

        Arguments:
            user_id (int): User id.

        Returns:
            dict: Dictionary containing the user data.
            Error 404: If the user is not found.
            Error 500: If an error occurred while getting user data.
            Error 401: If the user is not authorized to get the user data.
        """
        if user_id != get_jwt_identity():
            self.logger.error(f"User {get_jwt_identity()} is not authorized to get user {user_id}")
            abort(401, message="You are not authorized to get this user.")
        try:
            user = self.user_service.get_user(user_id)
        except ValueError:
            self.logger.error(f"Error getting user data from the database for the user id {user_id}.")
            abort(404, message=f"User with the id {user_id} not found.")
        except Exception as e:
            self.logger.error(f"Error getting user data from the database for the user id {user_id}. Error = {e}")
            abort(500, message="An error occurred while getting user data.")
        return user


@blp.route("/user")
class UserList(MethodView):
    """
    Class to handle to create a new user.
    """

    @inject.autoparams()
    def __init__(self, user_service: UserService):
        """
        Initializes the User class with the provided UserService.

        Arguments:
            user_service (UserService): Service class to interact
        """
        self.user_service = user_service
        self.logger = logging.getLogger(__name__)

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        """
        Stores the user data into the database.

        Arguments:
            user_data (dict): Dictionary containing the user data.

        Returns:
            dict: Dictionary containing the user data.
            Error 400: If a user with the same name already exists.
            Error 500: If an error occurred while storing user data.
        """
        try:
            hashed_password = self.user_service.hash_password(user_data["password"])
            user_data["password"] = hashed_password
            user = UserModel(**user_data)
            stored_user_id = self.user_service.store_user_data(user)
            stored_user = self.user_service.get_user(stored_user_id)
            return stored_user
        except IntegrityError:
            self.logger.error(f"Error storing user data into database. A user with the same name already exists.")
            abort(400, message="A user with the same name already exists.")
        except Exception as e:
            self.logger.error(f"Error storing user data into database. Error - {e}")
            abort(500, message="An error occurred while storing user data.")


@blp.route("/login")
class Login(MethodView):
    """
    Class to handle the login resource
    """

    @inject.autoparams()
    def __init__(self, user_service: UserService):
        """
        Initializes the Login class with the provided UserService.
        """
        self.user_service = user_service
        self.logger = logging.getLogger(__name__)

    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        """
        Logs in the user with the provided credentials.

        Arguments:
            user_data (dict): Dictionary containing the user data.

        Returns:
            dict: Dictionary containing the access token.
            Error 401: If the credentials are invalid.
        """
        try:
            user = self.user_service.get_user_by_user_name(user_data["user_name"])
        except ValueError:
            self.logger.error(f"User with name {user_data['user_name']} does not exist in the database.")
            abort(401, message="Invalid credentials")

        if self.user_service.verify_password(user_data["password"], user.password):
            access_token = create_access_token(user.id, expires_delta=timedelta(hours=1))
            refresh_token = create_refresh_token(user.id)
            self.logger.info(f"User {user_data['user_name']} logged in!")
            return {'access_token': access_token,
                    'refresh_token': refresh_token}, 200
        else:
            self.logger.warning("User login incorrect!")
            abort(401, message="Invalid credentials")


@blp.route("/refresh")
class Refresh(MethodView):
    """
    Class to handle the refresh token resource
    """

    @inject.autoparams()
    def __init__(self, user_service: UserService):
        """
        Initializes the Refresh class with the provided UserService.
        """
        self.user_service = user_service
        self.logger = logging.getLogger(__name__)

    @jwt_required(refresh=True)
    def post(self):
        """
        Refreshes the access token with the provided refresh token.

        Returns:
            dict: Dictionary containing the access token.
            Error 401: If the refresh token is invalid.
        """
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, expires_delta=timedelta(hours=1))
        refresh_token = create_refresh_token(identity=current_user)
        self.logger.info(f"Access token refreshed for user {current_user}")
        return {'access_token': access_token,
                'refresh_token': refresh_token}, 200
