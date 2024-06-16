import logging
from src.configuration.base_configuration import BaseConfiguration
from src.configuration.environment_variable_configuration import EnvironmentVariableConfiguration
from src.electricity_price_service.api.base_electricity_price_api import BaseElectricityPriceAPI
from src.electricity_price_service.api.nordpool_electricity_price_api import NordpoolElectricityPriceAPI
from src.electricity_price_service.processors.base_electricity_price_processor import BaseElectricityPriceProcessor
from src.electricity_price_service.processors.nordpool_electricity_price_processor import NordpoolElectricityPriceProcessor
from src.weather_service.api.base_weather_api import BaseWeatherAPI
from src.weather_service.processors.base_weather_processor import BaseWeatherProcessor
from src.weather_service.processors.open_meteo_weather_processor import OpenMeteoWeatherProcessor
from src.weather_service.api.open_meteo_weather_api import OpenMeteoWeatherAPI


def app_injection_configuration(binder):
    """
    Configures and binds services to their respective interfaces based on application settings defined in configuration files.

    This function dynamically configures dependency injections based on the specific service implementations
    specified in the configuration file. It establishes mappings between interface types and their concrete implementations,
    ensuring that components throughout the application can rely on consistent and configurable dependency injection.

    Args:
        binder (inject.Binder): The binder provided by the 'inject' library for configuring dependencies.

    Raises:
        ValueError: If the configuration specifies an unsupported service.
    """

    logger = logging.getLogger(__name__)
    try:
        # Bind configuration instance
        configuration_instance = EnvironmentVariableConfiguration()
        binder.bind(BaseConfiguration, configuration_instance)

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
    except Exception as e:
        logger.exception(e)
        raise
