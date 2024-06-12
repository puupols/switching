import inject
import logging
from flask.views import MethodView
from src.switch_service.switch_service import SwitchService
from flask_smorest import Blueprint, abort
from ..schemas import SwitchStatusRetrivalSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.switch_service.models.switch_model import SwitchModel

blp = Blueprint("switch status", __name__, description="Operations on switch status")


@blp.route("/switch/status")
class SwitchStatus(MethodView):
    """
    SwitchStatus class for handling switch status retrieval requests.
    """

    @inject.autoparams()
    def __init__(self, switch_service: SwitchService):
        """
        Initializes the SwitchStatus with the provided SwitchService.
        """
        self.switch_service = switch_service
        self.logger = logging.getLogger(__name__)

    @jwt_required()
    @blp.arguments(SwitchStatusRetrivalSchema)
    @blp.response(200, SwitchStatusRetrivalSchema)
    def get(self, switch_data):
        """
        Retrieves the status of a switch based on the provided switch data.

        Args:
            switch_data (dict): Dictionary containing the name of the switch and place_id.

        Returns:
            dict: Dictionary containing the name of the switch and its status.
        """
        switch_name = switch_data["name"]
        switch_status = self.switch_service.get_switch_status(switch_name)

        if switch_status == SwitchModel.SWITCH_VALUE_IF_ERROR_OCCURRED:
            abort(500, message=f"Could not process request for the switch with name {switch_name}. "
                               f"Please check switch status calculation logic")
        if switch_status == SwitchModel.SWITCH_VALUE_IF_SWITCH_NOT_IMPLEMENTED:
            abort(500, message=f"Could not process request for the switch with name {switch_name}. "
                               f"Switch not defined or calculation logic not set")

        response = {"name": switch_name,
                    "status": switch_status}
        self.logger.info(f'Returned response: {response}')
        return response
