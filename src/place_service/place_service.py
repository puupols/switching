import inject
from src.repository_service.place_repository_service import PlaceRepositoryService

class PlaceService:

    @inject.autoparams()
    def __init__(self, place_repository_service: PlaceRepositoryService):
        """
        Initializes the PlaceService with the provided PlaceRepositoryService.

        Arguments:
            place_repository_service (PlaceRepositoryService): Repository service class to interact
        """
        self.place_repository_service = place_repository_service

    def store_place_data(self, place):
        """
        Stores the place data into the database.

        Arguments:
            place (PlaceModel): PlaceModel object containing the place data.

        Returns:
            PlaceModel: PlaceModel object containing the place data.
        """
        self.place_repository_service.store_place_data(place)

    def get_place(self, place_id, user_id):
        """
        Retrieves the place data from the database.

        Arguments:
            place_id (int): The id of the place to be retrieved.
            user_id (int): The id of the user for the place.

        Returns:
            PlaceModel: PlaceModel object containing the place data.
        """
        return self.place_repository_service.get_place(place_id, user_id)

    def get_place_and_switches(self, place_id, user_id):
        """
        Retrieves the place data with switches from the database.

        Arguments:
            place_id (int): The id of the place to be retrieved.
            user_id (int): The id of the user for the place.

        Returns:
            PlaceModel: PlaceModel object containing the place data.
        """
        return self.place_repository_service.get_place_and_switches(place_id, user_id)

    def get_all_places_and_switches_for_user(self, user_id):
        """
        Retrieves all places and switches for a user.

        Arguments:
            user_id (int): The id of the user for the places.

        Returns:
            List[PlaceModel]: List of place objects retrieved from the database.
        """
        return self.place_repository_service.get_all_places_and_switches_for_user(user_id)

    def delete_place(self, place_id, user_id):
        """
        Deletes a place from the database.

        Arguments:
            place_id (int): The id of the place to be deleted.`
            user_id (int): The id of the user for the place.

        Returns:
              None
        """
        self.place_repository_service.delete_place(place_id, user_id)