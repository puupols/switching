import logging
import inject
from src.configuration.base_configuration import BaseConfiguration
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, Table, Column, MetaData, Integer, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import sessionmaker, registry
from src.weather_service.models.weather_model import WeatherModel
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel


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
        Initializes the RepositoryService with the given configuration.

        Args:
            configuration (BaseConfiguration): Configuration object for retrieving service settings.
        """
        self.configuration = configuration
        self.logger = logging.getLogger(__name__)
        self.engine = create_engine(configuration.get(self.DATABASE_STRING_CONFIG_NAME))
        self.session_maker = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.mapper_registry = registry()
        self._define_tables()

    def _define_tables(self):
        """
        Defines the database tables for weather and electricity price data.
        """
        self.weather_table = Table(
            'weather', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('datetime', DateTime, index=True),
            Column('cloud_cover', Float),
            Column('temperature', Float),
            Column('latitude', Float, index=True),
            Column('longitude', Float, index=True),
            Column('sunshine_duration', Float),
            UniqueConstraint('datetime', 'latitude', 'longitude', name='uix_datetime_lat_long')
        )
        self.electricity_price_table = Table(
            'electricity_price', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('datetime', DateTime, index=True),
            Column('price', Float),
            UniqueConstraint('datetime', name='uix_datetime')
        )

    def create_database(self):
        """
        Creates the database and maps the WeatherModel and ElectricityPriceModel to the respective tables.
        """
        self.mapper_registry.map_imperatively(WeatherModel, self.weather_table)
        self.mapper_registry.map_imperatively(ElectricityPriceModel, self.electricity_price_table)
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
