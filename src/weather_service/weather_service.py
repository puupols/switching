from src.weather_service.api.base_weather_api import BaseWeatherAPI
from src.weather_service.processors.base_weather_processor import BaseWeatherProcessor
from src.repository_service.base_repository_service import BaseRepositoryService
from src.location_service.base_location_service import BaseLocationService

class WeatherService:

    def __init__(self, weather_api: BaseWeatherAPI, weather_processor: BaseWeatherProcessor,
                 repository_service: BaseRepositoryService,
                 location_service: BaseLocationService):
        self.weather_api = weather_api
        self.weather_processor = weather_processor
        self.repository_service = repository_service
        self.location_service = location_service

    def regenerate_weather_data(self):
        latitude, longitude = self.location_service.get_location()
        data = self.weather_api.get_weather_data(latitude, longitude)
        processed_data = self.weather_processor.process_raw_data(data)
        self.repository_service.store_weather_data(processed_data)

    def get_weather_data_after_date(self, date):
        return self.repository_service.get_weather_data_after_date(date)
