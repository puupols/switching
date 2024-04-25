from location_service.configuration_based_location_service import ConfigurationBasedLocationService
from configuration.file_configuration import BaseConfiguration
from weather_service.api.open_meteo_weather_api import OpenMeteoWeatherAPI
from electricity_price_service.api.nordpool_electricity_price_api import NordpoolElectricityPriceAPI
from electricity_price_service.processors.nordpool_electricity_price_processor import NordpoolElectricityPriceProcessor
from weather_service.processors.open_meteo_weather_processor import OpenMeteoWeatherProcessor
from repository_service.sqllite_repository_service import SQLLiteRepositoryService


def get_location_service_from_config(configuration: BaseConfiguration):

    location_service_configuration = configuration.get('location_service')
    if location_service_configuration == 'configuration_file':
        return ConfigurationBasedLocationService(configuration)


def get_weather_api_from_config(configuration: BaseConfiguration):
    weather_api_configuration = configuration.get('weather_service')
    if weather_api_configuration == 'open_meteo':
        return OpenMeteoWeatherAPI()

def get_electricity_price_api(configuration: BaseConfiguration):
    electricity_price_api_configuration = configuration.get('electricity_price_service')
    if electricity_price_api_configuration == 'nordpool':
        return NordpoolElectricityPriceAPI()

def get_electricity_price_processor(configuration: BaseConfiguration):
    electricity_price_processor_configuration = configuration.get('electricity_price_service')
    if electricity_price_processor_configuration == 'nordpool':
        return NordpoolElectricityPriceProcessor()

def get_weather_processor(configuration: BaseConfiguration):
    weather_processor_configuration = configuration.get('weather_service')
    if weather_processor_configuration == 'open_meteo':
        return OpenMeteoWeatherProcessor()

def get_repository_service(configuration: BaseConfiguration):
    repository_service_configuration = configuration.get('repository_service')
    if repository_service_configuration == 'sqllite':
        return SQLLiteRepositoryService()
