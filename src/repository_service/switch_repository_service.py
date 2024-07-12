from sqlalchemy.exc import IntegrityError
from src.repository_service.base_repository_service import BaseRepositoryService
from src.switch_service.models.switch_model import SwitchModel
from src.place_service.models.place_model import PlaceModel


class SwitchRepositoryService(BaseRepositoryService):
    """
    Repository service for storing and retrieving switch data from the database.
    """

    def store_switch_data(self, switch):
        """
        Stores a switch object into the database.

        Args: switch (SwitchModel): SwitchModel object to be stored in the database.

        Returns:
            None, raises an IntegrityError if the switch already exists in the database.
        """
        try:
            with self.session_maker() as session:
                session.add(switch)
                session.commit()
        except IntegrityError:
            self.logger.error(f"Switch with name {switch.name} already exists in the database.")
            raise
        except Exception as e:
            self.logger.error(f"Error storing switch data into database. Error = {e}")
            raise

    def update_switch_data(self, switch, user_id):
        """
        Updates an existing switch object in the database.

        Args:
            switch (SwitchModel): SwitchModel object to be updated in the database.
            user_id (str): The user id of the user who owns the switch.

        Returns:
            None, raises a ValueError if the switch does not exist in the database.
        """
        try:
            with self.session_maker() as session:
                try:
                    existing_switch = self.get_switch_for_user(switch.uuid, user_id)
                except ValueError as ve:
                    self.logger.error(f"ValueError in get_switch: {ve}")
                    raise ve
                existing_switch.status_calculation_logic = switch.status_calculation_logic
                existing_switch.name = switch.name
                existing_switch.place_id = switch.place_id
                session.add(existing_switch)
                session.commit()
        except Exception as e:
            self.logger.error(f"Error updating switch data into database. Error = {e}")
            raise e

    def get_switch(self, uuid):
        """
        Retrieves a switch object from the database based on the switch name.

        Args:
            uuid (str): The uuid of the switch to be retrieved.

        Returns:
            SwitchModel: SwitchModel object retrieved from the database. ValueError is raised if the switch does not exist.
        """
        with self.session_maker() as session:
            existing_switch = session.query(SwitchModel).filter(SwitchModel.uuid == uuid).first()
            if existing_switch:
                return existing_switch
            else:
                raise ValueError(f"Switch with uuid {uuid} does not exist in the database.")

    def get_switch_for_user(self, uuid, user_id):
        """
        Retrieves a switch object from the database based on the switch uuid and user id.

        Args:
            uuid (str): The uuid of the switch to be retrieved.
            user_id (str): The user id of the user who owns the switch.

        Returns:
            SwitchModel: SwitchModel object retrieved from the database. ValueError is raised if the switch does not exist.
        """
        with self.session_maker() as session:
            user_places = session.query(PlaceModel).filter(PlaceModel.user_id == user_id).all()
            for place in user_places:
                existing_switch = session.query(SwitchModel).filter(SwitchModel.uuid == uuid,
                                                                    SwitchModel.place_id == place.id).first()
                if existing_switch:
                    return existing_switch
            raise ValueError(f"Switch with uuid {uuid} does not exist for the user in the database.")

    def delete_switch(self, uuid, user_id):
        """
        Deletes a switch object from the database.

        Args:
            uuid (str): The uuid of the switch to be deleted.
            user_id (str): The user id of the user who owns the switch.

        Returns:
            None, raises a ValueError if the switch does not exist in the database.
        """
        try:
            with self.session_maker() as session:
                existing_switch = self.get_switch_for_user(uuid, user_id)
                session.delete(existing_switch)
                session.commit()
        except ValueError as ve:
            self.logger.error(f"ValueError in get_switch: {ve}")
            raise ve
        except Exception as e:
            self.logger.error(f"Error deleting switch data from database. Error = {e}")
            raise e
