from src.repository_service.base_repository_service import BaseRepositoryService
from src.location_service.models.location_model import LocationModel
from sqlalchemy.exc import IntegrityError


class LocationRepositoryService(BaseRepositoryService):
    """
    Class to handle location interactions with the database.
    """

    def store_location_data(self, location):
        """
        Stores the location data into the database.

        Arguments:
            location (LocationModel): Location data to store into the database.

        Raises:
            Exception: If an error occurred while storing location data.
        """
        try:
            with self.session_maker() as session:
                session.add(location)
                session.commit()
        except IntegrityError:
            self.logger.info(f"Location with latitude {location.latitude} and longitude {location.longitude} already exists in the database.")
        except Exception as e:
            self.logger.error(f"Error storing location data into database. Error = {e}")
            raise

    def get_location(self, latitude, longitude):
        """
        Retrieves the location data from the database.

        Arguments:
            latitude (float): Latitude of the location.
            longitude (float): Longitude of the location.

        Returns:
            LocationModel: Location data.
            ValueError: If the location does not exist in the database.
        """
        with self.session_maker() as session:
            location = session.query(LocationModel).filter_by(latitude=latitude, longitude=longitude).first()
            if location is None:
                raise ValueError(
                    f"Location with latitude {latitude} and longitude {longitude} does not exist in the database.")
            return location

    def get_all_locations(self):
        """
        Retrieves all location data from the database.

        Returns:
            list[LocationModel]: List of location data.
        """
        with self.session_maker() as session:
            locations = session.query(LocationModel).all()
            return locations
