from src.configuration.base_configuration import BaseConfiguration
from src.weather_service.weather_service import WeatherService
from src.electricity_price_service.electricity_price_service import ElectricityPriceService
import inject
import importlib.util
import sys
import logging


class SwitchService:
    """
    Service class responsible for managing switch statuses based on dynamic loading of switch status modules.

    This service dynamically loads Python modules corresponding to specific switch names to determine their status.
    It uses configuration settings to restrict the allowed switch names and handles interactions with both the weather
    and electricity price services to provide necessary data for switch status determination.

    Attributes:
        configuration (BaseConfiguration): Configuration object providing access to necessary settings like allowed switch names.
        weather_service (WeatherService): Service providing weather data.
        electricity_price_service (ElectricityPriceService): Service providing electricity price data.
        logger (logging.Logger): Logger for recording activity and errors within the service.
    """
    SWITCH_STATUS_FILE_BASE_PATH = 'src/switch_service/switch_statuses/'
    SWITCH_STATUS_FILE_EXTENSION = '.py'
    ALLOWED_SWITCH_NAME_CONFIG_NAME = 'allowed_switch_names'
    RETURN_VALUE_IF_ERROR_OCCURRED = 'ERROR'

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

    def _load_module(self, switch_name):
        """
        Dynamically loads a Python module corresponding to the given switch name.

        Checks if the switch name is allowed based on the configuration. If allowed, the corresponding Python
        file is loaded as a module to determine the switch status.

        Args:
            switch_name (str): The name of the switch for which the status module is to be loaded.

        Returns:
            module: The loaded Python module corresponding to the switch, or None if an error occurs.

        Raises:
            ValueError: If the switch name is not allowed based on configuration settings.
        """
        allowed_switch_names = self.configuration.get(self.ALLOWED_SWITCH_NAME_CONFIG_NAME)
        if switch_name not in allowed_switch_names:
            self.logger.exception('Switch name must be defined in configuration')
            raise ValueError('Switch name must be defined in configuration')

        try:
            module_path = self.SWITCH_STATUS_FILE_BASE_PATH + switch_name + self.SWITCH_STATUS_FILE_EXTENSION
            module_name = switch_name
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            return module
        except FileNotFoundError as e:
            self.logger.exception(
                f'Switch status file not defined in switch_service/switch_statuses for a switch {switch_name}.')
        except Exception as e:
            self.logger.exception(f'And error occurred')
        return None

    def get_switch_status(self, switch_name):
        """
        Retrieves the status of a switch by dynamically loading its status module and executing its status determination logic defined in the module.

        Args:
            switch_name (str): The name of the switch whose status is to be determined.

        Returns:
            str: The status of the switch, or 'ERROR' if an error occurs during the process.
        """
        try:
            module = self._load_module(switch_name)
            return module.get_switch_status(self.weather_service, self.electricity_price_service)
        except Exception as e:
            self.logger.exception(f'Error occurred during the call to get_switch_status for a switch {switch_name}.')
            return self.RETURN_VALUE_IF_ERROR_OCCURRED
