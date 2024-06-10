from src.repository_service.base_repository_service import BaseRepositoryService
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel
from sqlalchemy.exc import IntegrityError


class ElectricityPriceRepositoryService(BaseRepositoryService):
    """
    Service class responsible for managing database operations for electricity price data.
    """

    def store_electricity_price_data(self, electricity_prices):
        """
        Stores a list of electricity price records into the database.
        Handles integrity errors by updating existing records.

        Args:
            electricity_prices (list): List of ElectricityPriceModel objects to be stored in the database.
        """
        with self.session_maker() as session:
            for electricity_price in electricity_prices:
                try:
                    session.add(electricity_price)
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    self._update_electricity_price_data(session, electricity_price)
                except Exception as e:
                    session.rollback()
                    self.logger.error(f"Error storing electricity price data into database. Error = {e}")

    def _update_electricity_price_data(self, session, electricity_price):
        """
        Updates existing electricity price data in the database.

        Args:
            session (sqlalchemy.orm.session.Session): SQLAlchemy session for database operations.
            electricity_price (ElectricityPriceModel): ElectricityPriceModel object containing updated price data.
        """
        existing_electricity_price = session.query(ElectricityPriceModel).filter(
            ElectricityPriceModel.datetime == electricity_price.datetime).first()
        if existing_electricity_price:
            existing_electricity_price.price = electricity_price.price
            session.commit()

    def get_electricity_price_data_after_date(self, date):
        """
        Retrieves electricity price data records from the database that are after the specified date.

        Args:
            date (datetime): The date after which the electricity price data records are to be retrieved.

        Returns:
            list: List of ElectricityPriceModel objects retrieved from the database.
        """
        with self.session_maker() as session:
            return session.query(ElectricityPriceModel).filter(ElectricityPriceModel.datetime > date).all()
