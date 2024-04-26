from factory import factory
from configuration.file_configuration import FileConfiguration
from weather_service.weather_service import WeatherService
from electricity_price_service.electricity_price_service import ElectricityPriceService
from switch_service.switch_service import SwitchService
from rest_api.flask_rest_api import FlaskRESTAPI

configuration = FileConfiguration()

location_service = factory.get_location_service_from_config(configuration)
weather_api = factory.get_weather_api_from_config(configuration)
electricity_price_api = factory.get_electricity_price_api(configuration)
electricity_price_processor = factory.get_electricity_price_processor(configuration)
weather_processor = factory.get_weather_processor(configuration)
repository_service = factory.get_repository_service(configuration)

electricity_price_service = ElectricityPriceService(electricity_price_api, electricity_price_processor, repository_service)
weather_service = WeatherService(weather_api, weather_processor, repository_service)
switch_service = SwitchService(configuration, weather_service, electricity_price_service)

import sys
import os

print("Current Path:", os.getcwd())
print("Python Executable:", sys.executable)
print("System Path:", sys.path)

rest_api = FlaskRESTAPI(switch_service, configuration)
rest_api.run_app()

# weather_service.regenerate_weather_data(*location_service.get_location())
# electricity_price_service.regenerate_electricity_price_data()
# status = switch_service.get_switch_status('boiler01')
# print(status)