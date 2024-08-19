from src.configuration.base_configuration import BaseConfiguration
from src.weather_service.weather_service import WeatherService
from src.electricity_price_service.electricity_price_service import ElectricityPriceService
from src.repository_service.switch_repository_service import SwitchRepositoryService
from src.switch_service.models.switch_model import SwitchModel
from src.switch_service.models.switch_data_model import SwitchDataModel
from src.switch_service.models.switch_data_model import SwitchDataType
from datetime import datetime
import inject
import logging


class SwitchService:
    """
    The SwitchService class is responsible for managing the switch data and calculating the switch status based on the
    status calculation logic defined in the switch data. The class uses the WeatherService, ElectricityPriceService, and
    RepositoryService to get the required data and store the switch data.
    """

    @inject.autoparams()
    def __init__(self, configuration: BaseConfiguration,
                 weather_service: WeatherService,
                 electricity_price_service: ElectricityPriceService,
                 repository_service: SwitchRepositoryService):
        """
        Initializes the SwitchService with the configuration, WeatherService, ElectricityPriceService, and RepositoryService.
        Arguments:
            configuration (BaseConfiguration): The configuration object.
            weather_service (WeatherService): The WeatherService object.
            electricity_price_service (ElectricityPriceService): The ElectricityPriceService object.
            repository_service (SwitchRepositoryService): The RepositoryService object.

        """
        self.configuration = configuration
        self.weather_service = weather_service
        self.electricity_price_service = electricity_price_service
        self.repository_service = repository_service
        self.logger = logging.getLogger(__name__)

    def _get_allowed_scope(self):
        """
        Defines the scope of allowed built-in functions and service methods for executing switch status logic.

        Returns:
            dict: A dictionary containing the allowed built-ins and service methods.
        """
        return {'__builtins__': {'datetime': datetime, 'print': print, 'sorted': sorted},
                'get_weather_data_after_date': self.weather_service.get_weather_data_after_date,
                'get_electricity_price_data_after_date': self.electricity_price_service.get_electricity_price_data_after_date}

    def _fetch_switch(self, switch_uuid, user_id):
        """
        Fetches the switch model from the repository service for a given switch UUID and user ID.

        Arguments:
            switch_uuid (str): The uuid of the switch.
            user_id (int): The id of the user.

        Returns:
            SwitchModel: The switch model.
        """
        try:
            return self.repository_service.get_switch_for_user(switch_uuid, user_id)
        except Exception as e:
            self.logger.error(
                f"Error fetching switch for switch_uuid {switch_uuid}, user_id {user_id}. The exception: {e}")
            return None

    def _store_switch_status(self, switch, switch_status):
        """
        Stores the status of the switch with the given uuid in the database.

        Arguments:
            switch (SwitchModel): The switch object.
            switch_status (str): The status of the switch.
        """
        try:
            switch_data = SwitchDataModel(switch_id=switch.id, data_type=SwitchDataType.RELAY_STATUS,
                                          log_cre_date=datetime.now(), value_text=switch_status)
            self.store_switch_operational_data(switch_data)
        except Exception as e:
            self.logger.error(
                f"Error storing switch operational data into database for switch uuid {switch.uuid}, exception: {e}")

    def get_switch_status(self, switch_uuid, user_id):
        """
        Calculates the status of the switch with the given uuid based on the status calculation logic defined in the switch data.

        Arguments:
            switch_uuid (str): The uuid of the switch.
            user_id (int): The id of the user.

        Returns:
            str: The status of the switch.
        """
        global_scope = self._get_allowed_scope()
        switch = self._fetch_switch(switch_uuid, user_id)
        switch_status_calculation_logic = switch.status_calculation_logic if switch else None

        if switch_status_calculation_logic is None:
            self.logger.error(f"Switch calculation logic not found for switch {switch_uuid}.")
            switch_status = SwitchModel.SWITCH_VALUE_IF_SWITCH_NOT_IMPLEMENTED
        else:
            try:
                exec(switch_status_calculation_logic, global_scope)
                get_switch_status = global_scope["get_switch_status"]
                switch_status = get_switch_status()
            except Exception as e:
                self.logger.error(f"Error calculating switch status for switch {switch_uuid}. The exception: {e}")
                switch_status = SwitchModel.SWITCH_VALUE_IF_ERROR_OCCURRED

        if switch:
            self._store_switch_status(switch, switch_status)
        return switch_status

    def test_switch_status_calculation_logic(self, switch_status_calculation_logic):
        """
        Tests the status calculation logic for the switch.

        Arguments:
            switch_status_calculation_logic (str): The status calculation logic for the switch.

        Returns:
            str: The status of the switch.
            str: Error message if any arise
        """
        global_scope = self._get_allowed_scope()
        error_message = None
        try:
            exec(switch_status_calculation_logic, global_scope)
            get_switch_status = global_scope["get_switch_status"]
            switch_status = get_switch_status()
        except Exception as e:
            self.logger.error(f"Error calculating switch status. The exception: {e}")
            switch_status = SwitchModel.SWITCH_VALUE_IF_ERROR_OCCURRED
            error_message = e

        return switch_status, error_message

    def store_switch_data(self, switch):
        """
        Stores the switch data in the database.

        Arguments:
            switch (SwitchModel): The switch data to store.

        Return:
            switch_id: Id of the stored switch
        """
        return self.repository_service.store_switch_data(switch)

    def update_switch_data(self, switch, user_id, uuid):
        """
        Updates the switch data in the database.

        Arguments:
            switch (SwitchModel): The switch data to update.
            user_id (int): The id of the user.
            uuid (str): The uuid of the switch.
        """
        self.repository_service.update_switch_data(switch, user_id, uuid)

    def get_switch_data(self, switch_id):
        """
        Retrieves the switch data from the database.

        Arguments:
            switch_id (str): The id of the switch.

        Returns:
            SwitchModel: The switch data.
        """
        return self.repository_service.get_switch(switch_id)

    def get_switch_data_for_user(self, switch_uuid, user_id):
        """
        Retrieves the switch data from the database.

        Arguments:
            switch_uuid (str): The uuid of the switch.
            user_id (str): The id of the user.

        Returns:
            SwitchModel: The switch data.
        """
        return self.repository_service.get_switch_for_user(switch_uuid, user_id)

    def delete_switch(self, switch_uuid, user_id):
        """
        Deletes the switch data from the database.

        Arguments:
            switch_uuid (str): The uuid of the switch.
            user_id (str): The id of the user.
        """
        self.repository_service.delete_switch(switch_uuid, user_id)

    def store_switch_operational_data(self, switch_data):
        """
        Stores a switch operational data object into the database.
        """
        self.repository_service.store_switch_operational_data(switch_data)
