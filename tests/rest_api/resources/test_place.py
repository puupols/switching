import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_jwt_extended import create_access_token, JWTManager
from flask_smorest import Api
from src.place_service.place_service import PlaceService
from src.location_service.location_service import LocationService
from src.rest_api.resources.place import Place, Places, blp
from src.place_service.models.place_model import PlaceModel
import inject


class TestPlace(unittest.TestCase):

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

        self.mock_place_service = MagicMock()
        self.mock_location_service = MagicMock()

        def configure_injector(binder):
            binder.bind(PlaceService, self.mock_place_service)
            binder.bind(LocationService, self.mock_location_service)

        inject.configure(configure_injector)

        self.place_view = Place(place_service=self.mock_place_service, location_service=self.mock_location_service)

        with self.app.app_context():
            self.access_token = create_access_token(identity=1)

    def tearDown(self):
        inject.clear()

    @patch('src.rest_api.resources.place.jwt_required')
    def test_post_place_success(self, mock_jwt_required):
        # Setup
        place_data = {
            "name": "test_place",
            "user_id": 1,
            "description": "some description",
            "location": {"latitude": 1.0, "longitude": 1.0}
        }

        mock_jwt_required.return_value = lambda fn: fn
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Actions
        response = self.client.post("/place", json=place_data, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, place_data)
        self.mock_location_service.store_location_data.assert_called_once()
        self.mock_location_service.get_location.assert_called_once()
        self.mock_place_service.store_place_data.assert_called_once()

    def test_get_place_success(self):
        # Setup
        place_data = {
            "user_id": 1,
            "place_id": 1
        }
        mock_place = PlaceModel(name="test_place", user_id=1, description="some description", location_id=1)
        self.mock_place_service.get_place_and_switches.return_value = mock_place
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Actions
        response = self.client.get("/place", json=place_data, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "name": "test_place",
            "user_id": 1,
            "description": "some description",
            "id": None,
            "switches": None,
            "location": None
        })

    def test_delete_place_success(self):
        # Setup
        place_data = {
            "place_id": "1",
            "user_id": 1
        }
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        self.mock_place_service.delete_place.return_value = None

        # Actions
        response = self.client.delete("/place", json=place_data, headers=headers)

        # Asserts
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Place with the id 1 has been deleted.'})
