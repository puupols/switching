import inject
import logging
from flask.views import MethodView
from src.switch_service.switch_service import SwitchService
from flask_smorest import Blueprint, abort
from ..schemas import SwitchStatusRetrivalSchema
from ..schemas import SwitchStatusCalculationTestSchema
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
        switch_uuid = switch_data["uuid"]
        user_id = get_jwt_identity()
        switch_status = self.switch_service.get_switch_status(switch_uuid, user_id)

        if switch_status == SwitchModel.SWITCH_VALUE_IF_ERROR_OCCURRED:
            abort(500, message=f"Could not process request for the switch with uuid {switch_uuid}. "
                               f"Please check switch status calculation logic")
        if switch_status == SwitchModel.SWITCH_VALUE_IF_SWITCH_NOT_IMPLEMENTED:
            abort(500, message=f"Could not process request for the switch with uuid {switch_uuid}. "
                               f"Switch not defined or calculation logic not set")

        response = {"uuid": switch_uuid,
                    "status": switch_status}
        self.logger.info(f'Returned response: {response}')
        return response

@blp.route("/switch/status/test_logic")
class SwitchStatusCalculationTest(MethodView):
    """
    SwitchStatusCalculationTest class for handling switch status calculation logic test requests.
    """
    @inject.autoparams()
    def __init__(self, switch_service: SwitchService):
        """
        Initializes the SwitchStatus with the provided SwitchService.
        """
        self.switch_service = switch_service
        self.logger = logging.getLogger(__name__)

    @jwt_required()
    @blp.arguments(SwitchStatusCalculationTestSchema)
    @blp.response(200, SwitchStatusCalculationTestSchema)
    def post(self, switch_calculation_logic):
        """
        Tests the calculation logic of a switch status based on the provided switch calculation logic.

        Args:
            switch_calculation_logic (dict): Dictionary containing the switch calculation logic.

        Returns:
            dict: Dictionary containing the switch calculation logic and the calculated status.
        """
        switch_status_calculation_logic = switch_calculation_logic["switch_calculation_logic"]
        switch_status, error_message = self.switch_service.test_switch_status_calculation_logic(switch_status_calculation_logic)

        response = {"switch_calculation_logic": switch_status_calculation_logic,
                    "switch_status": switch_status,
                    "error_message": error_message}
        self.logger.info(f'Returned response: {response}')
        return response
