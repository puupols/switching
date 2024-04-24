from factory import factory
from configuration.file_configuration import FileConfiguration
from weather_service.weather_service import WeatherService

configuration = FileConfiguration()

location_service = factory.get_location_service_from_config(configuration)
weather_api = factory.get_weather_api_from_config(configuration)
electricity_price_service = factory.get_electricity_price_api(configuration)
weather_processor = factory.get_weather_processor(configuration)
repository_service = factory.get_repository_service(configuration)

weather_service = WeatherService(weather_api, weather_processor, repository_service)

weather_service.regenerate_weather_data(*location_service.get_location())

# print(electricity_price_service.get_electricity_pirce())