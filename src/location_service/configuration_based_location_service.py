from src.location_service.base_location_service import BaseLocationService
from src.configuration.base_configuration import BaseConfiguration


class ConfigurationBasedLocationService(BaseLocationService):
    LOCATION_LATITUDE_CONFIG_NAME = 'location_latitude'
    LOCATION_LONGITUDE_CONFIG_NAME = 'location_longitude'

    def __init__(self, configuration: BaseConfiguration):
        super().__init__()
        self.configuration = configuration

    def get_location(self):
        latitude = self.configuration.get(self.LOCATION_LATITUDE_CONFIG_NAME)
        longitude = self.configuration.get(self.LOCATION_LONGITUDE_CONFIG_NAME)
        return latitude, longitude
