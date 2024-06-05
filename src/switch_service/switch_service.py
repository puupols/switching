from src.configuration.base_configuration import BaseConfiguration
from src.weather_service.weather_service import WeatherService
from src.electricity_price_service.electricity_price_service import ElectricityPriceService
import inject
import logging
import datetime


class SwitchService:
    """
    Service class responsible for managing switch statuses by dynamically executing Python code.

    This service retrieves and executes Python scripts that determine the status of various switches.
    It utilizes external services to fetch weather and electricity price data needed for the switch status calculations.

    Attributes:
        configuration (BaseConfiguration): Configuration object providing access to necessary settings.
        weather_service (WeatherService): Service providing weather data.
        electricity_price_service (ElectricityPriceService): Service providing electricity price data.
        logger (logging.Logger): Logger for recording activity and errors within the service.
    """
    SWITCH_STATUS_FILE_BASE_PATH = 'src/switch_service/switch_statuses/'
    SWITCH_STATUS_FILE_EXTENSION = '.py'
    ALLOWED_SWITCH_NAME_CONFIG_NAME = 'allowed_switch_names'
    RETURN_VALUE_IF_ERROR_OCCURRED = 'ERROR'
    RETURN_VALUE_IF_SWITCH_NOT_FOUND = 'NOT_FOUND'

    @inject.autoparams()
    def __init__(self, configuration: BaseConfiguration,
                 weather_service: WeatherService,
                 electricity_price_service: ElectricityPriceService):
        """
        Initializes the SwitchService with configuration and necessary services.

        Args:
            configuration (BaseConfiguration): Configuration object for retrieving service settings.
            weather_service (WeatherService): The service that provides weather data.
            electricity_price_service (ElectricityPriceService): The service that provides electricity price data.
        """
        self.configuration = configuration
        self.weather_service = weather_service
        self.electricity_price_service = electricity_price_service
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
        Retrieves the Python code for calculating the status of the specified switch.

        Args:
            switch_name (str): The name of the switch whose status logic is to be retrieved.

        Returns:
            str or None: The Python code as a string if the logic exists, otherwise None.
        """
        try:
            with open(f'src/switch_service/switch_statuses/{switch_name}.py', 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def get_switch_status(self, switch_name):
        """
        Determines the status of the specified switch by dynamically executing its associated logic.

        Args:
            switch_name (str): The name of the switch to check.

        Returns:
            str: The status of the switch, or a predefined error status if the logic cannot be executed.
        """
        global_scope = self._get_allowed_scope()
        switch_status_calculation_logic = self._get_switch_status_calculation_logic(switch_name)

        if switch_status_calculation_logic is None:
            self.logger.error(f"Switch calculation logic not found for switch {switch_name}.")
            switch_status = self.RETURN_VALUE_IF_SWITCH_NOT_FOUND
        else:
            try:
                exec(switch_status_calculation_logic, global_scope)
                get_switch_status = global_scope["get_switch_status"]
                switch_status = get_switch_status()
            except Exception as e:
                self.logger.error(f"Error calculating switch status for switch {switch_name}. The exception: {e}")
                switch_status = self.RETURN_VALUE_IF_ERROR_OCCURRED

        return switch_status
