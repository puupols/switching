from src.weather_service.api.base_weather_api import BaseWeatherAPI
import requests


class OpenMeteoWeatherAPI(BaseWeatherAPI):

    def __init__(self, configuration):
        super().__init__(configuration)
        self.weather_data_types = 'cloud_cover,temperature,sunshine_duration'
        self.forecast_days = '3'
        self.timezone = 'EET'

    def get_weather_data(self, latitude, longitude):
        open_meteo_url = self.configuration.get('open_meteo_url')
        url = open_meteo_url.format(latitude=latitude,
                                    longitude=longitude,
                                    weather_data_types=self.weather_data_types,
                                    forecast_days=self.forecast_days,
                                    timezone=self.timezone)
        resp = requests.get(url)
        return resp.json()
