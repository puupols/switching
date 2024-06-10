import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import clear_mappers
from sqlalchemy.exc import IntegrityError
from src.configuration.base_configuration import BaseConfiguration
from src.repository_service.user_repository_service import UserRepositoryService
from src.user_service.models.user_model import UserModel


class TestUserRepositoryService(unittest.TestCase):

    def setUp(self):
        self.mock_configuration = MagicMock(spec=BaseConfiguration)
        self.mock_configuration.get.return_value = "sqlite:///:memory:"
        self.user_repository_service = UserRepositoryService(configuration=self.mock_configuration)
        self.user_repository_service.create_database()

    def tearDown(self):
        self.user_repository_service.metadata.drop_all(self.user_repository_service.engine)
        clear_mappers()
        self.user_repository_service.engine.dispose()

    def test_store_user_data(self):
        # Setup
        user = UserModel(user_name="User 1", user_email="test@test.lv", password="password")
        expected_name = user.user_name
        # Actions
        self.user_repository_service.store_user_data(user)
        with self.user_repository_service.session_maker() as session:
            stored_data = session.query(UserModel).all()

        # Asserts
        self.assertEqual(len(stored_data), 1)
        self.assertEqual(stored_data[0].user_name, expected_name)

    def test_store_user_data_if_already_exists(self):
        # Setup
        user = UserModel(user_name="User 1", user_email="test@test.lv", password="password")
        duplicate_user = UserModel(user_name="User 1", user_email="test@test.lv", password="password")

        # Actions
        self.user_repository_service.store_user_data(user)

        # Asserts
        with self.assertRaises(IntegrityError):
            self.user_repository_service.store_user_data(duplicate_user)

    def test_update_user_data(self):
        # Setup
        user = UserModel(user_name="User 1", user_email="test@test.lv", password="password")
        updated_user = UserModel(user_name="User 1", user_email="test@testttt.lv", password="new_password")

        # Actions
        self.user_repository_service.store_user_data(user)
        self.user_repository_service.update_user_data(updated_user)
        changed_user = self.user_repository_service.get_user("User 1")

        # Asserts
        self.assertEqual(changed_user.user_email, "test@testttt.lv")
        self.assertEqual(changed_user.password, "new_password")

    def test_update_user_data_if_not_exists(self):
        # Setup
        user = UserModel(user_name="User 1", user_email="teswt@test.lv", password="password")
        updated_user = UserModel(user_name="User 2", user_email="test@test.lv", password="new_password")

        # Actions
        self.user_repository_service.store_user_data(user)

        # Asserts
        with self.assertRaises(ValueError):
            self.user_repository_service.update_user_data(updated_user)

    def test_get_user(self):
        # Setup
        user = UserModel(user_name="User 1", user_email="test@test.lv", password="password")
        expected_name = user.user_name

        # Actions
        self.user_repository_service.store_user_data(user)
        result = self.user_repository_service.get_user("User 1")

        # Asserts
        self.assertEqual(result.user_name, expected_name)

    def test_get_user_if_not_exists(self):
        # Setup
        user = UserModel(user_name="User 1", user_email="test@test.lv", password="password")

        # Actions
        self.user_repository_service.store_user_data(user)

        # Asserts
        with self.assertRaises(ValueError):
            self.user_repository_service.get_user("User 2")
