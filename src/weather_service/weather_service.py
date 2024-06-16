import inject
import logging
from src.weather_service.api.base_weather_api import BaseWeatherAPI
from src.weather_service.processors.base_weather_processor import BaseWeatherProcessor
from src.repository_service.weather_repository_service import WeatherRepositoryService
from src.location_service.location_service import LocationService


class WeatherService:
    """
    A service class that orchestrates the flow of fetching, processing, and storing weather data.

    This service utilizes a weather API to retrieve raw weather data based on the current location,
    processes this data into a usable format, and then stores it using a repository service.
    It also provides functionality to retrieve stored weather data after a specified date.

    Attributes:
        weather_api (BaseWeatherAPI): The API client for fetching raw weather data.
        weather_processor (BaseWeatherProcessor): The processor for converting raw data into structured data.
        repository_service (WeatherRepositoryService): The service for storing and retrieving processed weather data.
        location_service (BaseLocationService): The service for obtaining the current geographic location.
    """

    @inject.autoparams()
    def __init__(self, weather_api: BaseWeatherAPI, weather_processor: BaseWeatherProcessor,
                 repository_service: WeatherRepositoryService,
                 location_service: LocationService):
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
        self.logger = logging.getLogger(__name__)

    def regenerate_weather_data(self):
        """
        Regenerates weather data for all locations by fetching, processing, and storing new weather data.
        """
        locations = self.location_service.get_all_locations()
        for location in locations:
            location_id = location.id
            latitude = location.latitude
            longitude = location.longitude
            self.logger.info(
                f"Regenerating weather data for location ID {location_id} at coordinates ({latitude}, {longitude}).")

            try:
                data = self.weather_api.get_weather_data(latitude, longitude)
                self.logger.debug(f"Received raw weather data for location ID {location_id}: {data}")

                processed_data = self.weather_processor.process_raw_data(data, location_id)
                self.logger.debug(f"Processed weather data for location ID {location_id}: {processed_data}")

                self.repository_service.store_weather_data(processed_data)
                self.logger.info(f"Successfully stored weather data for location ID {location_id}.")

            except Exception as e:
                self.logger.error(
                    f"Failed to regenerate weather data for location ID {location_id} at coordinates ({latitude}, {longitude}). Error: {e}")

        self.logger.info("Completed the regeneration of weather data for all locations.")

    def get_weather_data_after_date(self, date):
        """
        Retrieves weather data stored in the repository that was collected after a specified date.

        Args:
            date (datetime): The date after which to retrieve weather data.

        Returns:
            list: A list of WeatherModel instances representing the weather data collected after the specified date.
        """
        return self.repository_service.get_weather_data_after_date(date)
