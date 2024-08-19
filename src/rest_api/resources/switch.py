import inject
import logging
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..schemas import SwitchSchema
from src.switch_service.switch_service import SwitchService
from src.switch_service.models.switch_model import SwitchModel
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity


blp = Blueprint("switches", __name__, description="Operations with switches")


@blp.route("/switch/<string:uuid>")
class SwitchItem(MethodView):
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

    @blp.response(200, SwitchSchema)
    @jwt_required()
    def get(self, uuid):
        """
        Retrieves the switch data from the database.

        Arguments:
            switch_data (dict): Dictionary containing the switch data.

        Returns:
            dict: Dictionary containing the switch data.
            Error 404: If the switch is not found.
            Error 500: If an error occurred while getting switch data.
        """
        user_id = get_jwt_identity()
        try:
            switch = self.switch_service.get_switch_data_for_user(uuid, user_id)
        except ValueError as e:
            self.logger.error(f"Error getting switch data from the database for the switch uuid {uuid}. Error = {e}")
            abort(404, message=f"Switch with the uuid {uuid} not found.")
        except Exception as e:
            self.logger.error(f"Error getting switch data from the database for the switch uuid {uuid}. Error = {e}")
            abort(500, message="An error occurred while getting switch data.")
        return switch

    @blp.arguments(SwitchSchema)
    @blp.response(200, SwitchSchema)
    @jwt_required()
    def put(self, switch_data, uuid):
        """
        Updates the switch data in the database.

        Arguments:
            uuid (str): UUID of the switch to be updated.
            switch_data (dict): Dictionary containing the switch data.

        Returns:
            dict: Dictionary containing the updated switch data.
            Error 404: If the switch is not found.
            Error 500: If an error occurred while updating switch data.
        """
        try:
            switch = SwitchModel(**switch_data)
            user_id = get_jwt_identity()
            self.switch_service.update_switch_data(switch, user_id, uuid)
        except ValueError as e:
            self.logger.error(f"Error updating switch data in the database. Error = {e}")
            abort(404, message="Switch not found.")
        except Exception as e:
            self.logger.error(f"Error updating switch data in the database. Error = {e}")
            abort(500, message="An error occurred while updating switch data.")
        return switch_data

    @jwt_required()
    def delete(self, uuid):
        """
        Deletes the switch data from the database.

        Arguments:
            switch_data (dict): Dictionary containing the switch data.

        Returns:
            dict: Dictionary containing the switch data.
            Error 404: If the switch is not found.
            Error 500: If an error occurred while deleting switch data.
        """
        user_id = get_jwt_identity()
        try:
            self.switch_service.delete_switch(uuid, user_id)
        except ValueError as e:
            self.logger.error(f"Error deleting switch data from the database for the switch uuid {uuid}. Error = {e}")
            abort(404, message=f"Switch with the uuid {uuid} not found.")
        except Exception as e:
            self.logger.error(f"Error deleting switch data from the database for the switch uuid {uuid}. Error = {e}")
            abort(500, message="An error occurred while deleting switch data.")
        return {"message": "Switch deleted"}, 200

@blp.route("/switch")
class SwitchList(MethodView):
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
            stored_switch_id = self.switch_service.store_switch_data(switch)
            stored_switch = self.switch_service.get_switch_data(stored_switch_id)
            return stored_switch
        except IntegrityError:
            self.logger.error(f"Error storing switch data into database. A switch with the same uuid {uuid} "
                              f"already exists or place does not exist id {place_id}.")
            abort(400, message=f"A place with id {place_id} does not exist or switch with the same uuid {uuid} "
                               f"already exists in this place.")
        except Exception as e:
            self.logger.error(f"Error storing switch data into database. Error - {e}")
            abort(500, message="An error occurred while storing switch data.")