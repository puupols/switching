from location_service.base_location_service import BaseLocationService
from configuration.base_configuration import BaseConfiguration

class ConfigurationBasedLocationService(BaseLocationService):

    def __init__(self, configuration: BaseConfiguration):
        super().__init__()
        self.configuration = configuration

    def get_location(self):
        latitude = self.configuration.get('location_latitude')
        longitude = self.configuration.get('location_longitude')
        return latitude, longitude
