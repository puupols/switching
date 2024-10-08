from src.repository_service.base_repository_service import BaseRepositoryService
from src.place_service.models.place_model import PlaceModel
from src.switch_service.models.switch_model import SwitchModel
from src.location_service.models.location_model import LocationModel
from sqlalchemy.exc import IntegrityError


class PlaceRepositoryService(BaseRepositoryService):

    def store_place_data(self, place):
        """
        Stores a place object into the database.

        Args: place (PlaceModel): PlaceModel object to be stored in the database.

        Returns:
            place_id: Id of the stored place
            Raises an IntegrityError if the place already exists in the database.
        """
        place_id = None
        try:
            with self.session_maker() as session:
                session.add(place)
                session.commit()
                place_id = int(place.id)
        except IntegrityError as ie:
            self.logger.error(f"Place with name {place.name} already exists in the database. Error = {ie}")
            raise
        except Exception as e:
            self.logger.error(f"Error storing place data into database. Error = {e}")
            raise
        return place_id

    def get_place(self, place_id, user_id):
        """
        Retrieves a place object from the database based on the place name and user id.

        Args:
            place_id (int): The id of the place to be retrieved.
            user_id (int): The id of the user for the place.

        Returns:
            PlaceModel: The place object retrieved from the database.
            ValueError: If the place does not exist in the database.
        """
        with self.session_maker() as session:
            place = session.query(PlaceModel).filter_by(id=place_id, user_id=user_id).first()
            if place is None:
                raise ValueError(f"Place with id {place_id} does not exist in the database.")
            return place

    def get_place_and_switches(self, place_id, user_id):
        """
        Retrieves a place object from the database based on the place name.

        Args:
            place_id (int): The id of the place to be retrieved.
            user_id (int): The id of the user for the place.

        Returns:
            PlaceModel: The place object retrieved from the database.
            ValueError: If the place does not exist in the database.
        """
        with self.session_maker() as session:
            place = session.query(PlaceModel).filter_by(id=place_id, user_id=user_id).first()
            if place is None:
                raise ValueError(f"Place with id {place_id} does not exist in the database.")
            switches = session.query(SwitchModel).filter_by(place_id=place.id).all()
            location = session.query(LocationModel).filter_by(id=place.location_id).first()
            place.switches = switches
            place.location = location
            return place

    def get_all_places_and_switches_for_user(self, user_id):
        """
        Retrieves all places and switches for a user.

        Args:
            user_id (int): The id of the user for the places.

        Returns:
            List[PlaceModel]: List of place objects retrieved from the database.
        """
        with self.session_maker() as session:
            places = session.query(PlaceModel).filter_by(user_id=user_id).all()
            if places is None:
                raise ValueError(f"There are no places for user with id {user_id} in the database.")
            for place in places:
                switches = session.query(SwitchModel).filter_by(place_id=place.id).all()
                place.switches = switches
                location = session.query(LocationModel).filter_by(id=place.location_id).first()
                place.location = location
            return places

    def delete_place(self, place_id, user_id):
        """
        Deletes a place object from the database based on the place name and user id.

        Args:
            place_id (int): The id of the place to be deleted.
            user_id (int): The id of the user for the place.

        Returns:
            None, raises a ValueError if the place does not exist in the database.
        """
        with self.session_maker() as session:
            place = session.query(PlaceModel).filter_by(id=place_id, user_id=user_id).first()
            if place is None:
                raise ValueError(f"Place with id {place_id} does not exist for user {user_id} in the database.")
            switches = session.query(SwitchModel).filter_by(place_id=place.id).all()
            for switch in switches:
                session.delete(switch)
            session.commit()
            session.delete(place)
            session.commit()
