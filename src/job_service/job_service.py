from apscheduler.schedulers.background import BackgroundScheduler
from src.electricity_price_service.electricity_price_service import ElectricityPriceService
from src.weather_service.weather_service import WeatherService
from src.configuration.base_configuration import BaseConfiguration


class JobService:

    def __init__(self, weather_service: WeatherService,
                 electricity_price_service: ElectricityPriceService,
                 configuration: BaseConfiguration):
        self.weather_service = weather_service
        self.electricity_price_service = electricity_price_service
        self.configuration = configuration
        self.scheduler = BackgroundScheduler()

    def _plan_weather_data_regeneration_job(self):
        interval_in_minutes = self.configuration.get('weather_data_regeneration_job_interval_in_minutes')
        self.scheduler.add_job(self.weather_service.regenerate_weather_data,
                               'interval', minutes=interval_in_minutes)

    def _plan_electricity_price_data_regeneration_job(self):
        interval_in_minutes = self.configuration.get('electricity_price_data_regeneration_job_interval_in_minutes')
        self.scheduler.add_job(self.electricity_price_service.regenerate_electricity_price_data,
                               'interval', minutes=interval_in_minutes)

    def plan_jobs(self):
        self._plan_weather_data_regeneration_job()
        self._plan_electricity_price_data_regeneration_job()
        self.scheduler.start()