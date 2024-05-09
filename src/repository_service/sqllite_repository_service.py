from contextlib import contextmanager
from src.repository_service.base_repository_service import BaseRepositoryService
from src.weather_service.models.weather_model import WeatherModel
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel
from typing import List
import sqlite3
import logging


class SQLLiteRepositoryService(BaseRepositoryService):
    """
    Concrete implementation of BaseRepositoryService that utilizes an SQLite database for storage and retrieval of weather and electricity price data.

    This class manages connections to an SQLite database, providing methods to insert, update, and retrieve structured data using SQL scripts loaded from external files.

    Attributes:
        DB_PATH (str): Database file path.
        BASE_SQL_PATH (str): Base path for SQL script files.
    """
    DB_PATH = 'src/repository_service/sql_lite_db/switching.db'
    BASE_SQL_PATH = 'src/repository_service/sql_lite_db/sql/'

    def __init__(self):
        """
        Initializes the SQLLiteRepositoryService, setting up the database and configuring logging.
        """
        super().__init__()
        self.initialize_database()
        self.logger = logging.getLogger(__name__)

    def initialize_database(self):
        """
        Sets up the database by creating the necessary tables and structures using an SQL script.
        """
        connection = sqlite3.connect(self.DB_PATH)
        cursor = connection.cursor()
        init_query = self._load_sql_query(self.BASE_SQL_PATH + 'initialize/initialize_database.sql')
        cursor.executescript(init_query)
        connection.commit()
        connection.close()

    def _load_sql_query(self, file_path):
        """
        Loads an SQL query from a file.

        Args:
            file_path (str): The path to the SQL file.

        Returns:
            str: The SQL query string.
        """
        with open(file_path, 'r') as file:
            return file.read()

    @contextmanager
    def db_connection(self):
        """
        Context manager that establishes and yields a database cursor, and ensures that the database connection is properly managed.

        Yields:
            sqlite3.Cursor: A cursor for performing database operations.
        """
        connection = sqlite3.connect(self.DB_PATH)
        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row
        try:
            yield cursor
        except Exception as e:
            self.logger.exception(f'An error occurred during the database request, the error: {e}')
        finally:
            connection.commit()
            connection.close()

    def store_weather_data(self, weather_data: List[WeatherModel]):
        """
        Stores weather data into the SQLite database.

        This method handles both insertion and updating of weather records. It loads SQL statements for both actions from files and executes them based on the provided weather data list.

        Args:
            weather_data (List[WeatherModel]): A list of WeatherModel instances containing weather data to be stored.

        Effects:
            Writes or updates weather data records in the SQLite database.
        """
        insert_statement = self._load_sql_query(self.BASE_SQL_PATH + 'weather/insert_weather.sql')
        update_statement = self._load_sql_query(self.BASE_SQL_PATH + 'weather/update_weather.sql')

        def get_params(weather):
            return {'datetime': weather.datetime, 'cloud_cover': weather.cloud_cover,
                    'temperature': weather.temperature, 'latitude': weather.latitude,
                    'longitude': weather.longitude, 'sunshine_duration': weather.sunshine_duration}

        params_list = [get_params(weather) for weather in weather_data]

        with self.db_connection() as cursor:
            cursor.executemany(update_statement, params_list)
            cursor.executemany(insert_statement, params_list)

    def store_electricity_price_data(self, electricity_prices: List[ElectricityPriceModel]):
        """
        Stores electricity price data into the SQLite database.

        Executes SQL statements for both inserting and updating electricity price data. These SQL scripts are loaded from external files, and the method processes each ElectricityPriceModel in the given list.

        Args:
            electricity_prices (List[ElectricityPriceModel]): A list of ElectricityPriceModel instances to store.

        Effects:
            Writes or updates electricity price records in the SQLite database.
        """
        insert_statement = self._load_sql_query(
            self.BASE_SQL_PATH + 'electricity_price/insert_electricity_price.sql')
        update_statement = self._load_sql_query(
            self.BASE_SQL_PATH + 'electricity_price/update_electricity_price.sql')

        def get_params(electricity_price):
            return {
                'datetime': electricity_price.datetime,
                'price': electricity_price.price
            }

        electricity_params_list = [get_params(electricity_price) for electricity_price in electricity_prices]

        with self.db_connection() as cursor:
            cursor.executemany(update_statement, electricity_params_list)
            cursor.executemany(insert_statement, electricity_params_list)

    def get_weather_data_after_date(self, date):
        """
        Retrieves weather data records from the SQLite database that were stored after a specified date.

        This method uses an SQL query to select records based on the datetime parameter, returning them as a list of WeatherModel instances.

        Args:
            date (datetime): The date to filter records; only records after this date are retrieved.

        Returns:
            List[WeatherModel]: A list of WeatherModel instances representing the weather data after the specified date.
        """
        select_statement = self._load_sql_query(
            self.BASE_SQL_PATH + 'weather/get_weather_data_after_date.sql')

        params = {'datetime': date}

        with self.db_connection() as cursor:
            cursor.execute(select_statement, params)
            rows = cursor.fetchall()
        result = [WeatherModel(row['datetime'], row['cloud_cover'], row['temperature'], row['latitude'], row['longitude'], row['sunshine_duration']) for row in rows]
        return result

    def get_electricity_price_data_after_date(self, date):
        """
        Retrieves electricity price records from the SQLite database that were stored after a specified date.

        Uses an SQL query loaded from an external file to select records. Returns the records as a list of ElectricityPriceModel instances.

        Args:
            date (datetime): The date to filter records; only records after this date are retrieved.

        Returns:
            List[ElectricityPriceModel]: A list of ElectricityPriceModel instances representing the electricity prices after the specified date.
        """
        select_statement = self._load_sql_query(
            self.BASE_SQL_PATH + 'electricity_price/get_electricity_price_after_date.sql')

        params = {'datetime': date}

        with self.db_connection() as cursor:
            cursor.execute(select_statement, params)
            rows = cursor.fetchall()
        result = [ElectricityPriceModel(row['datetime'], row['price']) for row in rows]
        return result
