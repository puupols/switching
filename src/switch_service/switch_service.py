from src.configuration.base_configuration import BaseConfiguration
from src.weather_service.weather_service import WeatherService
from src.electricity_price_service.electricity_price_service import ElectricityPriceService
import importlib.util
import sys
import logging


class SwitchService:
    def __init__(self, configuration: BaseConfiguration,
                 weather_service: WeatherService,
                 electricity_price_service: ElectricityPriceService):
        self.configuration = configuration
        self.weather_service = weather_service
        self.electricity_price_service = electricity_price_service
        self.logger = logging.getLogger(__name__)

    def _load_module(self, switch_name):
        allowed_switch_names = self.configuration.get('allowed_switch_names')
        if switch_name in allowed_switch_names:
            try:
                module_path = 'src/switch_service/switch_statuses/' + switch_name + '.py'
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
        else:
            self.logger.exception('Switch name must be defined in configuration')
            raise ValueError('Switch name must be defined in configuration')

    def get_switch_status(self, switch_name):
        try:
            module = self._load_module(switch_name)
            return module.get_switch_status(self.weather_service, self.electricity_price_service)
        except Exception as e:
            self.logger.exception(f'Error occurred during the call to get_switch_status for a switch {switch_name}.')
            return 'ERROR'
