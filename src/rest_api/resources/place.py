import inject
import logging
from src.place_service.place_service import PlaceService
from src.location_service.location_service import LocationService
from src.location_service.models.location_model import LocationModel
from src.place_service.models.place_model import PlaceModel
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from src.rest_api.schemas import PlaceSchema, PlaceGetSchema, PlaceSwitchesSchema, PlaceGetAllSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

blp = Blueprint("places", __name__, description="Operations with places")

@blp.route("/place")
class Place(MethodView):
    """
    Class to handle the place resource.
    """

    @inject.autoparams()
    def __init__(self, place_service: PlaceService, location_service: LocationService):
        """
        Initializes the Place class with the provided PlaceService.

        Arguments:
            place_service (PlaceService): Service class to interact
        """
        self.place_service = place_service
        self.location_service = location_service
        self.logger = logging.getLogger(__name__)

    @blp.arguments(PlaceSchema)
    @blp.response(201, PlaceSchema)
    @jwt_required()
    def post(self, place_data):
        """
        Stores the place data into the database.

        Arguments:
            place_data (dict): Dictionary containing the place data.

        Returns:
            dict: Dictionary containing the place data.
            Error 400: If a place with the same name already exists.
            Error 500: If an error occurred while storing place data.
        """
        if place_data["user_id"] != get_jwt_identity():
            self.logger.error(
                f"User {get_jwt_identity()} is not authorized to create a place for user {place_data['user_id']}")
            abort(401, message="You are not authorized to create a place for this user.")

        try:
            location = LocationModel(**place_data["location"])
            self.location_service.store_location_data(location)
            stored_location = self.location_service.get_location(place_data["location"]["latitude"],
                                                                 place_data["location"]["longitude"])

            place = PlaceModel(name=place_data["name"],
                               location_id=stored_location.id,
                               user_id=place_data["user_id"],
                               description=place_data["description"]
                               )
            self.place_service.store_place_data(place)
            return place_data, 201
        except IntegrityError:
            self.logger.error(f"Error storing place data into database. A place with the same name already exists.")
            abort(400, message="A place with the same name already exists.")
        except Exception as e:
            self.logger.error(f"Error storing place data into database. Error - {e}")
            abort(500, message="An error occurred while storing place data.")

    @blp.arguments(PlaceGetSchema)
    @blp.response(200, PlaceSwitchesSchema)
    @jwt_required()
    def get(self, place_data):
        """
        Retrieves the place data from the database.

        Arguments:
            place_data (dict): Dictionary containing the place id and user id.

        Returns:
            dict: Dictionary containing the place data.
            Error 404: If the place is not found.
            Error 500: If an error occurred while getting place data.
            Error 401: If the user is not authorized to get the place data.
        """
        place_id = place_data["place_id"]
        user_id = place_data["user_id"]
        if user_id != get_jwt_identity():
            self.logger.error(f"User {get_jwt_identity()} is not authorized to get place {place_id}")
            abort(401, message="You are not authorized to get this place.")
        try:
            place = self.place_service.get_place_and_switches(place_id, user_id)
        except ValueError:
            self.logger.error(f"Error getting place data from the database for the place id {place_id}.")
            abort(404, message=f"Place with the id {place_id} not found.")
        except Exception as e:
            self.logger.error(f"Error getting place data from the database for the place id {place_id}. Error = {e}")
            abort(500, message="An error occurred while getting place data.")
        return place

    @blp.arguments(PlaceGetSchema)
    @jwt_required()
    def delete(self, place_data):
        """
        Deletes the place data from the database.

        Arguments:
            place_data (dict): Dictionary containing the place id and user id.

        Returns:
            dict: Dictionary containing the message.
            Error 404: If the place is not found.
            Error 500: If an error occurred while deleting place data.
            Error 401: If the user is not authorized to delete the place data.
        """
        place_id = place_data["place_id"]
        user_id = place_data["user_id"]
        if user_id != get_jwt_identity():
            self.logger.error(f"User {get_jwt_identity()} is not authorized to delete place {place_id}")
            abort(401, message="You are not authorized to delete this place.")
        try:
            self.place_service.delete_place(place_id, user_id)
            return {"message": f"Place with the id {place_id} has been deleted."}, 200
        except ValueError:
            self.logger.error(f"Error deleting place data from the database for the place id {place_id}.")
            abort(404, message=f"Place with the id {place_id} not found.")
        except Exception as e:
            self.logger.error(f"Error deleting place data from the database for the place id {place_id}. Error = {e}")
            abort(500, message="An error occurred while deleting place data.")


@blp.route("/places")
class Places(MethodView):

    @inject.autoparams()
    def __init__(self, place_service: PlaceService):
        """
        Initializes the Places class with the provided PlaceService.

        Arguments:
            place_service (PlaceService): Service class to interact
        """
        self.place_service = place_service
        self.logger = logging.getLogger(__name__)

    @blp.arguments(PlaceGetAllSchema)
    @blp.response(200, PlaceSwitchesSchema(many=True))
    @jwt_required()
    def get(self, user_data):
        """
        Retrieves all places and switches for a user.

        Arguments:
            user_data (dict): Dictionary containing the user id.

        Returns:
            dict: Dictionary containing the places and switches data.
            Error 404: If the user is not found.
            Error 500: If an error occurred while getting places and switches data.
            Error 401: If the user is not authorized to get the places and switches data.
        """
        user_id = user_data["user_id"]
        if user_id != get_jwt_identity():
            self.logger.error(f"User {get_jwt_identity()} is not authorized to get places for user {user_id}")
            abort(401, message="You are not authorized to get places for this user.")
        try:
            places = self.place_service.get_all_places_and_switches_for_user(user_id)
        except ValueError:
            self.logger.error(f"There are no places for user with id {user_id} in the database.")
            abort(404, message=f"There are no places for user with id {user_id} in the database.")
        except Exception as e:
            self.logger.error(f"Error getting places data from the database for the user id {user_id}. Error = {e}")
            abort(500, message="An error occurred while getting places data.")
        return places
