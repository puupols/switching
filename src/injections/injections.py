import logging
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

    logger = logging.getLogger(__name__)
    try:
        # Bind configuration instance
        configuration_instance = FileConfiguration()
        binder.bind(BaseConfiguration, configuration_instance)

        location_service_config = configuration_instance.get('location_service')
        if location_service_config == 'configuration_file':
            binder.bind(BaseLocationService, ConfigurationBasedLocationService(configuration_instance))
        else:
            raise ValueError(f'Unsupported location service: {location_service_config}')

        weather_service_config = configuration_instance.get('weather_service')
        if configuration_instance.get('weather_service') == 'open_meteo':
            binder.bind(BaseWeatherAPI, OpenMeteoWeatherAPI(configuration_instance))
            binder.bind(BaseWeatherProcessor, OpenMeteoWeatherProcessor())
        else:
            raise ValueError(f'Unsupported weather api service: {weather_service_config}')

        electricity_price_api_config = configuration_instance.get('electricity_price_service')
        if electricity_price_api_config == 'nordpool':
            binder.bind(BaseElectricityPriceAPI, NordpoolElectricityPriceAPI(configuration_instance))
            binder.bind(BaseElectricityPriceProcessor, NordpoolElectricityPriceProcessor())
        else:
            raise ValueError(f'Unsupported electricity price api service: {electricity_price_api_config}')

        repository_service_config = configuration_instance.get('repository_service')
        if repository_service_config == 'sqllite':
            binder.bind(BaseRepositoryService, SQLLiteRepositoryService())
        else:
            raise ValueError(f'Unsupported repository service: {repository_service_config}')
    except Exception as e:
        logger.exception(e)
        raise
