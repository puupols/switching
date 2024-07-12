import inject
import logging
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..schemas import SwitchSchema, SwitchGetSchema
from src.switch_service.switch_service import SwitchService
from src.switch_service.models.switch_model import SwitchModel
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity


blp = Blueprint("switches", __name__, description="Operations with switches")


@blp.route("/switch")
class Switch(MethodView):
    """
    Class to handle the switch resource
    """

    @inject.autoparams()
    def __init__(self, switch_service: SwitchService):
        """
        Initializes the Switch class with the provided SwitchService.

        Arguments:
            switch_service (SwitchService): Service class to interact
        """
        self.switch_service = switch_service
        self.logger = logging.getLogger(__name__)

    @blp.arguments(SwitchSchema)
    @blp.response(201, SwitchSchema)
    @jwt_required()
    def post(self, switch_data):
        """
        Stores the switch data into the database.

        Arguments:
            switch_data (dict): Dictionary containing the switch data.

        Returns:
            dict: Dictionary containing the switch data.
            Error 400: If a switch with the same name already exists.
            Error 500: If an error occurred while storing switch data.
        """
        place_id = switch_data["place_id"]
        uuid = switch_data["uuid"]
        try:
            switch = SwitchModel(**switch_data)
            self.switch_service.store_switch_data(switch)
            return switch_data
        except IntegrityError:
            self.logger.error(f"Error storing switch data into database. A switch with the same uuid {uuid} "
                              f"already exists or place does not exist id {place_id}.")
            abort(400, message=f"A place with id {place_id} does not exist or switch with the same uuid {uuid} "
                               f"already exists in this place.")
        except Exception as e:
            self.logger.error(f"Error storing switch data into database. Error - {e}")
            abort(500, message="An error occurred while storing switch data.")

    @blp.arguments(SwitchSchema)
    @blp.response(200, SwitchSchema)
    @jwt_required()
    def put(self, switch_data):
        """
        Updates the switch data in the database.

        Arguments:
            switch_data (dict): Dictionary containing the switch data.

        Returns:
            dict: Dictionary containing the updated switch data.
            Error 404: If the switch is not found.
            Error 500: If an error occurred while updating switch data.
        """
        try:
            switch = SwitchModel(**switch_data)
            user_id = get_jwt_identity()
            self.switch_service.update_switch_data(switch, user_id)
        except ValueError as e:
            self.logger.error(f"Error updating switch data in the database. Error = {e}")
            abort(404, message="Switch not found.")
        except Exception as e:
            self.logger.error(f"Error updating switch data in the database. Error = {e}")
            abort(500, message="An error occurred while updating switch data.")
        return switch_data

    @blp.arguments(SwitchGetSchema)
    @blp.response(200, SwitchSchema)
    @jwt_required()
    def get(self, switch_data):
        """
        Retrieves the switch data from the database.

        Arguments:
            switch_data (dict): Dictionary containing the switch data.

        Returns:
            dict: Dictionary containing the switch data.
            Error 404: If the switch is not found.
            Error 500: If an error occurred while getting switch data.
        """
        switch_uuid = switch_data["uuid"]
        user_id = get_jwt_identity()
        try:
            switch = self.switch_service.get_switch_data_for_user(switch_uuid, user_id)
        except ValueError as e:
            self.logger.error(f"Error getting switch data from the database for the switch uuid {switch_uuid}. Error = {e}")
            abort(404, message=f"Switch with the uuid {switch_uuid} not found.")
        except Exception as e:
            self.logger.error(f"Error getting switch data from the database for the switch uuid {switch_uuid}. Error = {e}")
            abort(500, message="An error occurred while getting switch data.")
        return switch

    @blp.arguments(SwitchGetSchema)
    @blp.response(200, SwitchSchema)
    @jwt_required()
    def delete(self, switch_data):
        """
        Deletes the switch data from the database.

        Arguments:
            switch_data (dict): Dictionary containing the switch data.

        Returns:
            dict: Dictionary containing the switch data.
            Error 404: If the switch is not found.
            Error 500: If an error occurred while deleting switch data.
        """
        switch_uuid = switch_data["uuid"]
        user_id = get_jwt_identity()
        try:
            self.switch_service.delete_switch(switch_uuid, user_id)
        except ValueError as e:
            self.logger.error(f"Error deleting switch data from the database for the switch uuid {switch_uuid}. Error = {e}")
            abort(404, message=f"Switch with the uuid {switch_uuid} not found.")
        except Exception as e:
            self.logger.error(f"Error deleting switch data from the database for the switch uuid {switch_uuid}. Error = {e}")
            abort(500, message="An error occurred while deleting switch data.")
        return switch_data
