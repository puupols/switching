from factory import factory
from configuration.file_configuration import FileConfiguration
from weather_service.weather_service import WeatherService
from electricity_price_service.electricity_price_service import ElectricityPriceService
from switch_service.switch_service import SwitchService

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

weather_service.regenerate_weather_data(*location_service.get_location())
electricity_price_service.regenerate_electricity_price_data()
status = switch_service.get_switch_status('boiler01')
print(status)