import inject
from src.configuration.base_configuration import BaseConfiguration
from src.configuration.file_configuration import FileConfiguration
from src.electricity_price_service.api.base_electricity_price_api import BaseElectricityPriceAPI
from src.electricity_price_service.api.nordpool_electricity_price_api import NordpoolElectricityPriceAPI
from src.electricity_price_service.processors.base_electricity_price_processor import BaseElectricityPriceProcessor
from src.electricity_price_service.processors.nordpool_electricity_price_processor import NordpoolElectricityPriceProcessor
from src.weather_service.api.base_weather_api import BaseWeatherAPI
from src.weather_service.processors.base_weather_processor import BaseWeatherProcessor
from src.weather_service.processors.open_meteo_weather_processor import OpenMeteoWeatherProcessor
from src.location_service.base_location_service import BaseLocationService
from src.location_service.configuration_based_location_service import ConfigurationBasedLocationService
from src.weather_service.api.open_meteo_weather_api import OpenMeteoWeatherAPI
from src.repository_service.base_repository_service import BaseRepositoryService
from src.repository_service.sqllite_repository_service import SQLLiteRepositoryService


def app_injection_configuration(binder):
    # Bind configuration instance
    configuration_instance = FileConfiguration()
    binder.bind(BaseConfiguration, configuration_instance)

    if configuration_instance.get('location_service') == 'configuration_file':
        binder.bind(BaseLocationService, ConfigurationBasedLocationService(configuration_instance))

    if configuration_instance.get('weather_service') == 'open_meteo':
        binder.bind(BaseWeatherAPI, OpenMeteoWeatherAPI(configuration_instance))

    if configuration_instance.get('weather_service') == 'open_meteo':
        binder.bind(BaseWeatherProcessor, OpenMeteoWeatherProcessor())

    if configuration_instance.get('electricity_price_service') == 'nordpool':
        binder.bind(BaseElectricityPriceAPI, NordpoolElectricityPriceAPI(configuration_instance))

    if configuration_instance.get('electricity_price_service') == 'nordpool':
        binder.bind(BaseElectricityPriceProcessor, NordpoolElectricityPriceProcessor())

    if configuration_instance.get('repository_service') == 'sqllite':
        binder.bind(BaseRepositoryService, SQLLiteRepositoryService())
