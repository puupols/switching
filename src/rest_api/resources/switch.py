import inject
import logging
from flask.views import MethodView
from src.switch_service.switch_service import SwitchService
from flask_smorest import Blueprint, abort
from ..schemas import SwitchSchema
from flask_jwt_extended import jwt_required

blp = Blueprint("switches", __name__, description="Operations on switches")


@blp.route("/switch/status")
class Switch(MethodView):
    """
    A class to handle switch status operations through a RESTful API endpoint.

    Attributes:
        SWITCH_VALUE_IF_ERROR_OCCURRED (str): Value returned if an error occurs.

    Methods:
        __init__(switch_service: SwitchService):
            Initializes the Switch class with the provided switch service.

        get(switch_data: dict) -> dict:
            Handles GET requests to retrieve the status of a switch.
    """

    SWITCH_VALUE_IF_ERROR_OCCURRED = 'ERROR'

    @inject.autoparams()
    def __init__(self, switch_service: SwitchService):
        """
        Initializes the Switch instance with a SwitchService.

        Args:
            switch_service (SwitchService): The service used to interact with switches.
        """
        self.switch_service = switch_service
        self.logger = logging.getLogger(__name__)

    @jwt_required()
    @blp.arguments(SwitchSchema)
    @blp.response(200, SwitchSchema)
    def get(self, switch_data):
        """
        Handles GET requests to retrieve the status of a switch.

        Args:
            switch_data (dict): The data for the switch, containing the switch name.

        Returns:
            dict: A dictionary containing the switch name and its status.

        Raises:
            HTTPException: If an error occurs while processing the request.
        """
        switch_name = switch_data["name"]
        switch_status = self.switch_service.get_switch_status(switch_name)

        if switch_status == self.SWITCH_VALUE_IF_ERROR_OCCURRED:
            abort(500, message=f"Could not process request for the switch with name {switch_name}. "
                               f"Please check if support for specific switch is implemented")

        response = {"name": switch_name,
                    "details": {"status": switch_status}
                    }
        self.logger.info(f'Returned response: {response}')
        return response
