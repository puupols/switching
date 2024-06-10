import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_smorest import Api
from src.user_service.user_service import UserService
from src.user_service.models.user_model import UserModel
from src.rest_api.resources.user import Login, User, blp
from flask_jwt_extended import create_access_token, JWTManager
from sqlalchemy.exc import IntegrityError
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

        self.mock_user_service = MagicMock()

        def configure_injector(binder):
            binder.bind(UserService, self.mock_user_service)

        inject.configure(configure_injector)

        self.login_view = Login(user_service=self.mock_user_service)
        self.user_view = User(user_service=self.mock_user_service)

        with self.app.app_context():
            self.access_token = create_access_token(identity='test_user')

    def tearDown(self):
        inject.clear()

    @patch('src.rest_api.resources.user.UserLoginSchema')
    def test_login_success(self, mock_schema):
        # Setup
        self.mock_user_service.get_user.return_value = UserModel(user_name="test_user", password="hashed_password",
                                                                 user_email="test_email")
        self.mock_user_service.verify_password.return_value = True
        mock_schema.return_value.load.return_value = {"username": "test_user", "password": "test_password"}

        # Actions
        response = self.client.post("/login", json={"user_name": "test_user", "password": "test_password"})

        # Asserts
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)

    @patch('src.rest_api.resources.user.UserLoginSchema')
    def test_login_failure(self, mock_schema):
        # Setup
        self.mock_user_service.get_user.return_value = UserModel(user_name="test_user", password="hashed_password",
                                                                 user_email="test_email")
        self.mock_user_service.verify_password.return_value = False
        mock_schema.return_value.load.return_value = {"username": "test_user", "password": "wrong_password"}

        # Actions
        response = self.client.post("/login", json={"user_name": "test_user", "password": "wrong_password"})

        # Asserts
        self.assertEqual(response.status_code, 401)
        self.assertIn("message", response.json)

    @patch('src.rest_api.resources.user.UserSchema')
    @patch('src.rest_api.resources.user.jwt_required')
    def test_save_user_success(self, mock_jwt_required, mock_schema):
        # Setup
        mock_jwt_required.return_value = lambda fn: fn
        self.mock_user_service.hash_password.return_value = "hashed_password"
        mock_schema.return_value.load.return_value = {"user_name": "test_user", "password": "test_password",
                                                      "user_email": "tes@tst.lv"}
        self.mock_user_service.save_user_data.return_value = None

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        # Actions
        response = self.client.post("/user", json={"user_name": "test_user", "password": "test_password",
                                                   "user_email": "tes@tst.lv"}, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 201)
        self.mock_user_service.hash_password.assert_called_once_with("test_password")
        self.mock_user_service.store_user_data.assert_called_once()

    @patch('src.rest_api.resources.user.UserSchema')
    @patch('src.rest_api.resources.user.jwt_required')
    def test_save_user_failure(self, mock_jwt_required, mock_schema):
        # Setup
        mock_jwt_required.return_value = lambda fn: fn
        self.mock_user_service.hash_password.return_value = "hashed_password"
        mock_schema.return_value.load.return_value = {"user_name": "test_user", "password": "test_password",
                                                      "user_email": "test@test.lv"}
        self.mock_user_service.store_user_data.side_effect = Exception("Error storing user data into database.")

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        # Actions
        response = self.client.post("/user", json={"user_name": "test_user", "password": "test_password",
                                                   "user_email": "test@test.lv"}, headers=headers)

        # Asserts
        self.mock_user_service.hash_password.assert_called_once_with("test_password")
        self.assertEqual(response.status_code, 500)
        self.assertIn("message", response.json)

    @patch('src.rest_api.resources.user.UserSchema')
    @patch('src.rest_api.resources.user.jwt_required')
    @patch('src.rest_api.resources.user.get_jwt_identity')
    def test_get_user_data_success(self, mock_get_jwt_identity, mock_jwt_required, mock_schema):
        # Setup
        mock_get_jwt_identity.return_value = 1
        mock_jwt_required.return_value = lambda fn: fn
        self.mock_user_service.get_user.return_value = UserModel(id=1, user_name="test_user", password="hashed_password",
                                                                 user_email="test@test.lv")
        mock_schema.return_value.load.return_value = {"user_name": "test_user"}

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        # Actions
        response = self.client.get("/user", json={"user_name": "test_user"}, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 200)
        self.mock_user_service.get_user.assert_called_once_with("test_user")

    @patch('src.rest_api.resources.user.UserSchema')
    @patch('src.rest_api.resources.user.jwt_required')
    @patch('src.rest_api.resources.user.get_jwt_identity')
    def test_get_user_data_not_authorized(self, mock_get_jwt_identity, mock_jwt_required, mock_schema):
        # Setup
        mock_get_jwt_identity.return_value = 2
        mock_jwt_required.return_value = lambda fn: fn
        self.mock_user_service.get_user.return_value = UserModel(id=1, user_name="test_user", password="hashed_password",
                                                                 user_email="test@test.lv")
        mock_schema.return_value.load.return_value = {"user_name": "test_user"}

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        # Actions
        response = self.client.get("/user", json={"user_name": "test_user"}, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 401)
        self.mock_user_service.get_user.assert_called_once_with("test_user")


#### test to udate user, put method

    @patch('src.rest_api.resources.user.UserSchema')
    @patch('src.rest_api.resources.user.jwt_required')
    @patch('src.rest_api.resources.user.get_jwt_identity')
    def test_update_user_data_success(self, mock_get_jwt_identity, mock_jwt_required, mock_schema):
        # Setup
        mock_get_jwt_identity.return_value = 1
        mock_jwt_required.return_value = lambda fn: fn
        self.mock_user_service.get_user.return_value = UserModel(id=1, user_name="test_user", password="hashed_password",
                                                                 user_email="test@test.lv")
        self.mock_user_service.hash_password.return_value = "hashed_password"
        mock_schema.return_value.load.return_value = {"user_name": "test_user", "password": "test_password",
                                                      "user_email": "test@test.lv"}

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Actions
        response = self.client.put("/user", json={"user_name": "test_user", "password": "test_password",
                                                   "user_email": "test@test.lv"}, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 200)
        self.mock_user_service.get_user.assert_called_once_with("test_user")
        self.mock_user_service.hash_password.assert_called_once_with("test_password")
        self.mock_user_service.update_user_data.assert_called_once()

    @patch('src.rest_api.resources.user.UserSchema')
    @patch('src.rest_api.resources.user.jwt_required')
    @patch('src.rest_api.resources.user.get_jwt_identity')
    def test_update_user_data_not_authorized(self, mock_get_jwt_identity, mock_jwt_required, mock_schema):
        # Setup
        mock_get_jwt_identity.return_value = 2
        mock_jwt_required.return_value = lambda fn: fn
        self.mock_user_service.get_user.return_value = UserModel(id=1, user_name="test_user",
                                                                 password="hashed_password",
                                                                 user_email="test@test.lv")
        self.mock_user_service.hash_password.return_value = "hashed_password"
        mock_schema.return_value.load.return_value = {"user_name": "test_user", "password": "test_password",
                                                      "user_email": "test@test.lv"}

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Actions
        response = self.client.put("/user", json={"user_name": "test_user", "password": "test_password",
                                                  "user_email": "test@test.lv"}, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 401)
        self.mock_user_service.get_user.assert_called_once_with("test_user")
        self.mock_user_service.hash_password.asser_not_called()
        self.mock_user_service.update_user_data.asser_not_called()


    ### test to delete user

    @patch('src.rest_api.resources.user.UserGetSchema')
    @patch('src.rest_api.resources.user.jwt_required')
    @patch('src.rest_api.resources.user.get_jwt_identity')
    def test_delete_user_data_success(self, mock_get_jwt_identity, mock_jwt_required, mock_schema):
        # Setup
        mock_get_jwt_identity.return_value = 1
        mock_jwt_required.return_value = lambda fn: fn
        self.mock_user_service.get_user.return_value = UserModel(id=1, user_name="test_user", password="hashed_password",
                                                                 user_email="test@test.lv")
        mock_schema.return_value.load.return_value = {"user_name": "test_user"}

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        # Actions
        response = self.client.delete("/user", json={"user_name": "test_user"}, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 200)
        self.mock_user_service.get_user.assert_called_once_with("test_user")
        self.mock_user_service.delete_user.assert_called_once_with("test_user")


    @patch('src.rest_api.resources.user.UserGetSchema')
    @patch('src.rest_api.resources.user.jwt_required')
    @patch('src.rest_api.resources.user.get_jwt_identity')
    def test_delete_user_data_unauthorized(self, mock_get_jwt_identity, mock_jwt_required, mock_schema):
        # Setup
        mock_get_jwt_identity.return_value = 2
        mock_jwt_required.return_value = lambda fn: fn
        self.mock_user_service.get_user.return_value = UserModel(id=1, user_name="test_user", password="hashed_password",
                                                                 user_email="test@test.lv")
        mock_schema.return_value.load.return_value = {"user_name": "test_user"}

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        # Actions
        response = self.client.delete("/user", json={"user_name": "test_user"}, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 401)
        self.mock_user_service.get_user.assert_called_once_with("test_user")
        self.mock_user_service.delete_user.assert_not_called()

