import inject
from passlib.hash import pbkdf2_sha256
from src.repository_service.user_repository_service import UserRepositoryService


class UserService:
    """
    Class to handle the business logic for the user service.
    """
    @inject.autoparams()
    def __init__(self, user_repository_service: UserRepositoryService):
        self.user_repository_service = user_repository_service

    def store_user_data(self, user):
        """
        Stores the user data into the database.

        Arguments:
            user (UserModel): Dictionary containing the user data.

        Return:
            None
        """
        self.user_repository_service.store_user_data(user)

    def get_user(self, user_name):
        """
        Retrieves the user data from the database.

        Arguments:
            user_name (str): The name of the user to be retrieved.

        Return:
            user (UserModel): UserModel object containing the user data.
        """
        return self.user_repository_service.get_user(user_name)

    def update_user_data(self, user):
        """
        Updates the user data in the database.

        Arguments:
            user (UserModel): Dictionary containing the user data.

        Return:
            None
        """
        self.user_repository_service.update_user_data(user)

    def delete_user(self, user_name):
        """
        Deletes the user data from the database.

        Arguments:
            user_name (str): The name of the user to be deleted.

        Return:
            None
        """
        self.user_repository_service.delete_user(user_name)

    def hash_password(cls, password):
        """
        Hashes the password using the pbkdf2_sha256 algorithm.

        Arguments:
            password (str): The password to be hashed.

        Return:
            str: The hashed password.
        """
        return pbkdf2_sha256.hash(password)

    def verify_password(cls, password, hashed_password):
        """
        Verifies the password using the pbkdf2_sha256 algorithm.

        Arguments:
            password (str): The password to be verified.
            hashed_password (str): The hashed password.

        Return:
            bool: True if the password is verified, False otherwise.
        """
        return pbkdf2_sha256.verify(password, hashed_password)
