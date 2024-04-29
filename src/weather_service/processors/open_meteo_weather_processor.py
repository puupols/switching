from src.weather_service.processors.base_weather_processor import BaseWeatherProcessor
from src.weather_service.models.weather_model import WeatherModel
from datetime import datetime

class OpenMeteoWeatherProcessor(BaseWeatherProcessor):

    def process_raw_data(self, raw_data):
        weather_data = []
        latitude = raw_data['latitude']
        longitude = raw_data['longitude']

        for i in range(len(raw_data['hourly']['time'])):
            date_string = raw_data['hourly']['time'][i]
            date_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M')
            cloud_cover = raw_data['hourly']['cloud_cover'][i]
            temperature = raw_data['hourly']['temperature'][i]
            weather = WeatherModel(date_obj, cloud_cover, temperature, latitude, longitude)
            weather_data.append(weather)

        return weather_data

