from logger import logger_config
from factory import factory
from src.configuration.file_configuration import FileConfiguration
from src.weather_service.weather_service import WeatherService
from src.electricity_price_service.electricity_price_service import ElectricityPriceService
from src.switch_service.switch_service import SwitchService
from src.job_service.job_service import JobService
from src.rest_api.flask_rest_api import FlaskRESTAPI


class Main:
    def __init__(self):
        logger_config.setup_logger()
        self.configuration = FileConfiguration()
        self.location_service = factory.get_location_service_from_config(self.configuration)
        self.weather_api = factory.get_weather_api_from_config(self.configuration)
        self.electricity_price_api = factory.get_electricity_price_api(self.configuration)
        self.electricity_price_processor = factory.get_electricity_price_processor(self.configuration)
        self.weather_processor = factory.get_weather_processor(self.configuration)
        self.repository_service = factory.get_repository_service(self.configuration)
        self.electricity_price_service = ElectricityPriceService(self.electricity_price_api, self.electricity_price_processor,
                                                            self.repository_service)
        self.weather_service = WeatherService(self.weather_api, self.weather_processor, self.repository_service, self.location_service)
        self.switch_service = SwitchService(self.configuration, self.weather_service, self.electricity_price_service)
        self.job_service = JobService(self.weather_service, self.electricity_price_service, self.configuration)
        self.rest_api = FlaskRESTAPI(self.switch_service, self.configuration)


    def run(self):
        self.job_service.plan_jobs()
        self.rest_api.run_app()


if __name__ == '__main__':
    main_app = Main()
    main_app.run()
