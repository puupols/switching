import inject
from src.weather_service.api.base_weather_api import BaseWeatherAPI
from src.weather_service.processors.base_weather_processor import BaseWeatherProcessor
from src.repository_service.repository_service import RepositoryService
from src.location_service.base_location_service import BaseLocationService


class WeatherService:
    """
    A service class that orchestrates the flow of fetching, processing, and storing weather data.

    This service utilizes a weather API to retrieve raw weather data based on the current location,
    processes this data into a usable format, and then stores it using a repository service.
    It also provides functionality to retrieve stored weather data after a specified date.

    Attributes:
        weather_api (BaseWeatherAPI): The API client for fetching raw weather data.
        weather_processor (BaseWeatherProcessor): The processor for converting raw data into structured data.
        repository_service (RepositoryService): The service for storing and retrieving processed weather data.
        location_service (BaseLocationService): The service for obtaining the current geographic location.
    """

    @inject.autoparams()
    def __init__(self, weather_api: BaseWeatherAPI, weather_processor: BaseWeatherProcessor,
                 repository_service: RepositoryService,
                 location_service: BaseLocationService):
        """
        Initializes the WeatherService with the necessary components for managing weather data.

        Args:
            weather_api (BaseWeatherAPI): The API client to fetch weather data.
            weather_processor (BaseWeatherProcessor): The processor to handle and convert raw weather data.
            repository_service (BaseRepositoryService): The repository to store and retrieve weather data.
            location_service (BaseLocationService): The service to obtain geographical location data.
        """
        self.weather_api = weather_api
        self.weather_processor = weather_processor
        self.repository_service = repository_service
        self.location_service = location_service

    def regenerate_weather_data(self):
        """
        Fetches, processes, and stores current weather data.

        Retrieves the current location, fetches weather data for this location, processes the data, and
        stores it in the repository. This method is typically used to update the stored weather data with
        the most recent information.
        """
        latitude, longitude = self.location_service.get_location()
        data = self.weather_api.get_weather_data(latitude, longitude)
        processed_data = self.weather_processor.process_raw_data(data)
        self.repository_service.store_weather_data(processed_data)

    def get_weather_data_after_date(self, date):
        """
        Retrieves weather data stored in the repository that was collected after a specified date.

        Args:
            date (datetime): The date after which to retrieve weather data.

        Returns:
            list: A list of WeatherModel instances representing the weather data collected after the specified date.
        """
        return self.repository_service.get_weather_data_after_date(date)
