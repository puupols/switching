import inject
from apscheduler.schedulers.background import BackgroundScheduler
from src.electricity_price_service.electricity_price_service import ElectricityPriceService
from src.weather_service.weather_service import WeatherService
from src.configuration.base_configuration import BaseConfiguration


class JobService:
    """
    Service class to manage and schedule periodic data regeneration jobs for weather and electricity price data.

    This class uses the APScheduler's BackgroundScheduler to schedule and run jobs that periodically
    invoke data regeneration methods in the weather and electricity price services.

    Attributes:
        weather_service (WeatherService): Service responsible for managing weather data operations.
        electricity_price_service (ElectricityPriceService): Service responsible for managing electricity price data operations.
        configuration (BaseConfiguration): Configuration instance to fetch job scheduling parameters.
        scheduler (BackgroundScheduler): APScheduler's scheduler to manage background jobs.
    """
    WEATHER_DATA_REGENERATION_JOB_INTERVAL_IN_MINUTES_CONFIG_NAME = 'weather_data_regeneration_job_interval_in_minutes'
    ELECTRICITY_PRICE_DATA_REGENERATION_JOB_INTERVAL_IN_MINUTES_CONFIG_NAME = 'electricity_price_data_regeneration_job_interval_in_minutes'

    @inject.autoparams()
    def __init__(self, weather_service: WeatherService,
                 electricity_price_service: ElectricityPriceService,
                 configuration: BaseConfiguration):
        """
        Initializes the JobService with the necessary services and configuration.

        The services and configuration are injected automatically using the inject.autoparams() decorator.

        Args:
            weather_service (WeatherService): The service that handles weather data regeneration.
            electricity_price_service (ElectricityPriceService): The service that handles electricity price data regeneration.
            configuration (BaseConfiguration): Configuration service for retrieving job intervals.
        """
        self.weather_service = weather_service
        self.electricity_price_service = electricity_price_service
        self.configuration = configuration
        self.scheduler = BackgroundScheduler()

    def _plan_weather_data_regeneration_job(self):
        """
        Plans and schedules the job to regenerate weather data at intervals specified in the configuration.
        """
        interval_in_minutes = int(self.configuration.get(self.WEATHER_DATA_REGENERATION_JOB_INTERVAL_IN_MINUTES_CONFIG_NAME))
        self.scheduler.add_job(self.weather_service.regenerate_weather_data,
                               'interval', minutes=interval_in_minutes)

    def _plan_electricity_price_data_regeneration_job(self):
        """
        Plans and schedules the job to regenerate electricity price data at intervals specified in the configuration.
        """
        interval_in_minutes = int(self.configuration.get(self.ELECTRICITY_PRICE_DATA_REGENERATION_JOB_INTERVAL_IN_MINUTES_CONFIG_NAME))
        self.scheduler.add_job(self.electricity_price_service.regenerate_electricity_price_data,
                               'interval', minutes=interval_in_minutes)

    def plan_jobs(self):
        """
        Schedules all planned jobs and starts the scheduler. This method should be called after the service instantiation to begin job execution.
        """
        self._plan_weather_data_regeneration_job()
        self._plan_electricity_price_data_regeneration_job()
        self.scheduler.start()
