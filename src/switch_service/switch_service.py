from src.configuration.base_configuration import BaseConfiguration
from src.weather_service.weather_service import WeatherService
from src.electricity_price_service.electricity_price_service import ElectricityPriceService
from src.repository_service.repository_service import RepositoryService
from src.switch_service.models.switch_model import SwitchModel
import inject
import logging
import datetime


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
                 repository_service: RepositoryService):
        """
        Initializes the SwitchService with the configuration, WeatherService, ElectricityPriceService, and RepositoryService.
        Arguments:
            configuration (BaseConfiguration): The configuration object.
            weather_service (WeatherService): The WeatherService object.
            electricity_price_service (ElectricityPriceService): The ElectricityPriceService object.
            repository_service (RepositoryService): The RepositoryService object.

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
        return {'__builtins__': {'datetime': datetime, 'print': print},
                'get_weather_data_after_date': self.weather_service.get_weather_data_after_date,
                'get_electricity_price_data_after_date': self.electricity_price_service.get_electricity_price_data_after_date}

    def _get_switch_status_calculation_logic(self, switch_name):
        """
        Gets the status calculation logic from the database for the switch with the given name.

        Arguments:
            switch_name (str): The name of the switch.

        Returns:
            str: The status calculation logic for the switch.
        """
        try:
            switch = self.repository_service.get_switch(switch_name)
            if switch:
                return switch.status_calculation_logic
            else:
                return None
        except Exception as e:
            self.logger.error(f"Error getting switch status calculation logic for switch {switch_name}. The exception: {e}")
            return None

    def get_switch_status(self, switch_name):
        """
        Calculates the status of the switch with the given name based on the status calculation logic defined in the switch data.

        Arguments:
            switch_name (str): The name of the switch.

        Returns:
            str: The status of the switch.
        """
        global_scope = self._get_allowed_scope()
        switch_status_calculation_logic = self._get_switch_status_calculation_logic(switch_name)

        if switch_status_calculation_logic is None:
            self.logger.error(f"Switch calculation logic not found for switch {switch_name}.")
            switch_status = SwitchModel.SWITCH_VALUE_IF_SWITCH_NOT_IMPLEMENTED
        else:
            try:
                exec(switch_status_calculation_logic, global_scope)
                get_switch_status = global_scope["get_switch_status"]
                switch_status = get_switch_status()
            except Exception as e:
                self.logger.error(f"Error calculating switch status for switch {switch_name}. The exception: {e}")
                switch_status = SwitchModel.SWITCH_VALUE_IF_ERROR_OCCURRED

        return switch_status

    def store_switch_data(self, switch):
        """
        Stores the switch data in the database.

        Arguments:
            switch (SwitchModel): The switch data to store.
        """
        self.repository_service.store_switch_data(switch)

    def update_switch_data(self, switch):
        """
        Updates the switch data in the database.

        Arguments:
            switch (SwitchModel): The switch data to update.
        """
        self.repository_service.update_switch_data(switch)

    def get_switch_data(self, switch_name):
        """
        Retrieves the switch data from the database.

        Arguments:
            switch_name (str): The name of the switch.

        Returns:
            SwitchModel: The switch data.
        """
        return self.repository_service.get_switch(switch_name)
