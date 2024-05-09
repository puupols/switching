from src.weather_service.api.base_weather_api import BaseWeatherAPI
import requests


class OpenMeteoWeatherAPI(BaseWeatherAPI):
    """
    Concrete implementation of the BaseWeatherAPI that uses the Open Meteo service to fetch weather data.

    This class fetches weather data such as cloud cover, temperature, and sunshine duration for specified
    geographical coordinates and returns this data in a JSON format.

    Attributes:
        WEATHER_DATA_TYPES (str): Specifies the types of weather data to fetch (e.g., cloud_cover, temperature).
        FORECAST_DAYS (str): Specifies the number of days to forecast.
        TIMEZONE (str): Specifies the timezone for the forecast data.
        OPEN_METEO_URN_CONFIG_NAME (str): Configuration key to retrieve the Open Meteo API URL.
    """
    WEATHER_DATA_TYPES = 'cloud_cover,temperature,sunshine_duration'
    FORECAST_DAYS = '3'
    TIMEZONE = 'EET'
    OPEN_METEO_URN_CONFIG_NAME = 'open_meteo_url'

    def __init__(self, configuration):
        """
        Initializes the OpenMeteoWeatherAPI with a configuration object.

        Args:
            configuration: Inherits the configuration object from BaseWeatherAPI.
        """
        super().__init__(configuration)

    def get_weather_data(self, latitude, longitude):
        """
        Fetches weather data from the Open Meteo API for specified latitude and longitude.

        Constructs a request URL with parameters for location, weather data types, forecast duration, and timezone,
        then sends a GET request to the Open Meteo API and returns the response in JSON format.

        Args:
            latitude (float): The latitude of the location for which to retrieve weather data.
            longitude (float): The longitude of the location for which to retrieve weather data.

        Returns:
            dict: JSON dictionary containing the requested weather data.
        """
        open_meteo_url = self.configuration.get(self.OPEN_METEO_URN_CONFIG_NAME)
        url = open_meteo_url.format(latitude=latitude,
                                    longitude=longitude,
                                    weather_data_types=self.WEATHER_DATA_TYPES,
                                    forecast_days=self.FORECAST_DAYS,
                                    timezone=self.TIMEZONE)
        resp = requests.get(url)
        return resp.json()
