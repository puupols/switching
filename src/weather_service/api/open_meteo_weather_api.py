from src.weather_service.api.base_weather_api import BaseWeatherAPI
import requests


class OpenMeteoWeatherAPI(BaseWeatherAPI):
    WEATHER_DATA_TYPES = 'cloud_cover,temperature,sunshine_duration'
    FORECAST_DAYS = '3'
    TIMEZONE = 'EET'
    OPEN_METEO_URN_CONFIG_NAME = 'open_meteo_url'

    def __init__(self, configuration):
        super().__init__(configuration)

    def get_weather_data(self, latitude, longitude):
        open_meteo_url = self.configuration.get(self.OPEN_METEO_URN_CONFIG_NAME)
        url = open_meteo_url.format(latitude=latitude,
                                    longitude=longitude,
                                    weather_data_types=self.WEATHER_DATA_TYPES,
                                    forecast_days=self.FORECAST_DAYS,
                                    timezone=self.TIMEZONE)
        resp = requests.get(url)
        return resp.json()
