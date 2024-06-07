import logging
import inject
from src.configuration.base_configuration import BaseConfiguration
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, registry
from src.weather_service.models.weather_model import WeatherModel
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel
from src.switch_service.models.switch_model import SwitchModel
from src.repository_service.tables.registry import initialize_tables


class RepositoryService:
    """
    Service class responsible for managing database operations for weather and electricity price data.

    This class provides methods to create the database schema, store weather and electricity price data,
    and retrieve data based on specific criteria.

    Attributes:
        DATABASE_STRING_CONFIG_NAME (str): Configuration key for the database connection string.
        configuration (BaseConfiguration): Configuration object providing access to necessary settings.
        logger (logging.Logger): Logger for recording activity and errors within the service.
        engine (sqlalchemy.engine.Engine): SQLAlchemy engine for database connection.
        session_maker (sqlalchemy.orm.session.sessionmaker): SQLAlchemy session maker for creating sessions.
        metadata (sqlalchemy.MetaData): SQLAlchemy MetaData object for schema definition.
        mapper_registry (sqlalchemy.orm.registry): SQLAlchemy registry for mapping classes to tables.
    """

    DATABASE_STRING_CONFIG_NAME = "database_string"

    @inject.autoparams()
    def __init__(self, configuration: BaseConfiguration):
        """
        Initializes the RepositoryService with the provided configuration.
        Creates the SQLAlchemy engine, session maker, and metadata objects.
        Initializes the database tables.
        """
        self.configuration = configuration
        self.logger = logging.getLogger(__name__)
        self.engine = create_engine(configuration.get(self.DATABASE_STRING_CONFIG_NAME))
        self.session_maker = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.mapper_registry = registry()
        self.tables = initialize_tables(self.metadata)

    def create_database(self):
        """
        Creates the database and maps the WeatherModel, ElectricityPriceModel and SwitchModel to the respective tables.
        """
        self.mapper_registry.map_imperatively(WeatherModel, self.tables['weather'])
        self.mapper_registry.map_imperatively(ElectricityPriceModel, self.tables['electricity_price'])
        self.mapper_registry.map_imperatively(SwitchModel, self.tables['switch'])
        self.metadata.create_all(self.engine)

    def store_weather_data(self, weather_data):
        """
        Stores a list of weather data records into the database.
        Handles integrity errors by updating existing records.

        Args:
            weather_data (list): List of WeatherModel objects to be stored in the database.
        """
        with (self.session_maker() as session):
            for weather in weather_data:
                try:
                    session.add(weather)
                    session.commit()
                except IntegrityError as e:
                    session.rollback()
                    self._update_weather_data(session, weather)
                except Exception as e:
                    session.rollback()
                    self.logger.error(f"Error storing weather data into database. Error - {e}")

    def _update_weather_data(self, session, weather):
        """
        Updates existing weather data in the database.

        Args:
            session (sqlalchemy.orm.session.Session): SQLAlchemy session for database operations.
            weather (WeatherModel): WeatherModel object containing updated weather data.
        """
        existing_weather = session.query(WeatherModel).filter(
            WeatherModel.datetime == weather.datetime,
            WeatherModel.latitude == weather.latitude,
            WeatherModel.longitude == weather.longitude
        ).first()
        if existing_weather:
            existing_weather.temperature = weather.temperature
            existing_weather.cloud_cover = weather.cloud_cover
            existing_weather.sunshine_duration = weather.sunshine_duration
            session.commit()

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

    def get_weather_data_after_date(self, date):
        """
        Retrieves weather data records from the database that are after the specified date.

        Args:
            date (datetime): The date after which the weather data records are to be retrieved.

        Returns:
            list: List of WeatherModel objects retrieved from the database.
        """
        with self.session_maker() as session:
            return session.query(WeatherModel).filter(WeatherModel.datetime > date).all()

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

    def update_switch_data(self, switch):
        """
        Updates an existing switch object in the database.

        Args:
            switch (SwitchModel): SwitchModel object to be updated in the database.

        Returns:
            None, raises a ValueError if the switch does not exist in the database.
        """
        try:
            with self.session_maker() as session:
                try:
                    existing_switch = self.get_switch(switch.name)
                except ValueError as ve:
                    self.logger.error(f"ValueError in get_switch: {ve}")
                    raise ve
                existing_switch.status_calculation_logic = switch.status_calculation_logic
                session.add(existing_switch)
                session.commit()
        except Exception as e:
            self.logger.error(f"Error updating switch data into database. Error = {e}")
            raise e

    def get_switch(self, name):
        """
        Retrieves a switch object from the database based on the switch name.

        Args:
            name (str): The name of the switch to be retrieved.

        Returns:
            SwitchModel: SwitchModel object retrieved from the database. ValueError is raised if the switch does not exist.
        """
        with self.session_maker() as session:
            existing_switch = session.query(SwitchModel).filter(SwitchModel.name == name).first()
            if existing_switch:
                return existing_switch
            else:
                raise ValueError(f"Switch with name {name} does not exist in the database.")
