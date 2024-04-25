from weather_service.api.base_weather_api import BaseWeatherAPI
import requests

class OpenMeteoWeatherAPI(BaseWeatherAPI):

    weather_data_types = 'cloud_cover,temperature'
    forecast_days = '3'
    timezone = 'EET'
    url_base = 'https://api.open-meteo.com/v1/forecast?'

    def get_weather_data(self, latitude, longitude):
        position = f'latitude={latitude}&longitude={longitude}'
        data_types = f'hourly={self.weather_data_types}'
        days = f'forecast_days={self.forecast_days}'
        zone = f'timezone={self.timezone}'
        url = self.url_base + position + '&' + data_types + '&' + days + '&' + zone
        resp = requests.get(url)
        return resp.json()
