from src.repository_service.base_repository_service import BaseRepositoryService
from src.user_service.models.user_model import UserModel
from sqlalchemy.exc import IntegrityError


class UserRepositoryService(BaseRepositoryService):

    def store_user_data(self, user):
        """
        Stores a user object into the database.

        Args: user (UserModel): UserModel object to be stored in the database.

        Returns:
            None, raises an IntegrityError if the user already exists in the database.
        """
        try:
            with self.session_maker() as session:
                session.add(user)
                session.commit()
        except IntegrityError:
            self.logger.error(f"User with name {user.user_name} already exists in the database.")
            raise
        except Exception as e:
            self.logger.error(f"Error storing user data into database. Error = {e}")
            raise

    def get_user(self, user_name):
        """
        Retrieves a user object from the database based on the user name.

        Args:
            user_name (str): The name of the user to be retrieved.

        Returns:
            UserModel: The user object retrieved from the database.
        """
        with self.session_maker() as session:
            user = session.query(UserModel).filter_by(user_name=user_name).first()
            if user is None:
                raise ValueError(f"User with name {user_name} does not exist in the database.")
            return user

    def update_user_data(self, user):
        """
        Updates an existing user object in the database.

        Args:
            user (UserModel): UserModel object to be updated in the database.

        Returns:
            None, raises a ValueError if the user does not exist in the database.
        """
        try:
            with self.session_maker() as session:
                existing_user = self.get_user(user.user_name)
                existing_user.user_email = user.user_email
                existing_user.password = user.password
                session.add(existing_user)
                session.commit()
        except ValueError as ve:
            self.logger.error(f"User with name {user.user_name} does not exist in the database. Error = {ve}")
            raise ve
        except Exception as e:
            self.logger.error(f"Error updating user data into database. Error = {e}")
            raise e

    def delete_user(self, user_name):
        """
        Deletes a user object from the database based on the user name.

        Args:
            user_name (str): The name of the user to be deleted.

        Returns:
            None, raises a ValueError if the user does not exist in the database.
        """
        try:
            with self.session_maker() as session:
                user = self.get_user(user_name)
                session.delete(user)
                session.commit()
        except ValueError as ve:
            self.logger.error(f"User with name {user_name} does not exist in the database. Error = {ve}")
            raise ve
        except Exception as e:
            self.logger.error(f"Error deleting user data from database. Error = {e}")
            raise e
