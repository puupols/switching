from src.location_service.base_location_service import BaseLocationService
from src.configuration.base_configuration import BaseConfiguration


class ConfigurationBasedLocationService(BaseLocationService):
    """
    A concrete implementation of BaseLocationService that retrieves geographic location information from configuration.

    This class uses a configuration service to fetch location data (latitude and longitude) defined in a configuration source.

    Attributes:
        LOCATION_LATITUDE_CONFIG_NAME (str): Configuration key used to retrieve the latitude value.
        LOCATION_LONGITUDE_CONFIG_NAME (str): Configuration key used to retrieve the longitude value.
    """
    LOCATION_LATITUDE_CONFIG_NAME = 'location_latitude'
    LOCATION_LONGITUDE_CONFIG_NAME = 'location_longitude'

    def __init__(self, configuration: BaseConfiguration):
        """
        Initializes the ConfigurationBasedLocationService with the necessary configuration.

        Args:
            configuration (BaseConfiguration): The configuration object that contains location settings.
        """
        super().__init__()
        self.configuration = configuration

    def get_location(self):
        """
        Retrieves the geographic location from the configuration.

        Fetches the latitude and longitude settings from the configuration and returns them as a tuple.

        Returns:
            tuple: A tuple containing the latitude and longitude as (latitude, longitude).
        """
        latitude = self.configuration.get(self.LOCATION_LATITUDE_CONFIG_NAME)
        longitude = self.configuration.get(self.LOCATION_LONGITUDE_CONFIG_NAME)
        return latitude, longitude
