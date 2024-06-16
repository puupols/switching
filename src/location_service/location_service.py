from src.repository_service.location_repository_service import LocationRepositoryService
import inject


class LocationService:

    @inject.autoparams()
    def __init__(self, location_repository_service: LocationRepositoryService):
        self.location_repository_service = location_repository_service

    def store_location_data(self, location):
        self.location_repository_service.store_location_data(location)

    def get_location(self, latitude, longitude):
        return self.location_repository_service.get_location(latitude, longitude)

    def get_all_locations(self):
        return self.location_repository_service.get_all_locations()
