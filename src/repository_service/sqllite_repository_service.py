from contextlib import contextmanager
from src.repository_service.base_repository_service import BaseRepositoryService
from src.weather_service.models.weather_model import WeatherModel
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel
import sqlite3


class SQLLiteRepositoryService(BaseRepositoryService):

    def __init__(self):
        super().__init__()
        self.db_path = 'src/repository_service/sql_lite_db/switching.db'
        self.base_sql_path = 'src/repository_service/sql_lite_db/sql/'
        self.initialize_database()

    def initialize_database(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        init_query = self._load_sql_query(self.base_sql_path + 'initialize/initialize_database.sql')
        cursor.executescript(init_query)
        connection.commit()
        connection.close()

    def _load_sql_query(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    @contextmanager
    def db_connection(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row
        try:
            yield cursor
        except Exception as e:
            print(f'An error occurred during the database request, the error: {e}')
        finally:
            connection.commit()
            connection.close()

    def store_weather_data(self, weather_data: [WeatherModel]):
        insert_statement = self._load_sql_query(self.base_sql_path + 'weather/insert_weather.sql')
        update_statement = self._load_sql_query(self.base_sql_path + 'weather/update_weather.sql')

        def get_params(weather):
            return {'datetime': weather.datetime, 'cloud_cover': weather.cloud_cover,
                    'temperature': weather.temperature, 'latitude': weather.latitude,
                    'longitude': weather.longitude}

        params_list = [get_params(weather) for weather in weather_data]

        with self.db_connection() as cursor:
            cursor.executemany(insert_statement, params_list)
            cursor.executemany(update_statement, params_list)

    def store_electricity_price_data(self, electricity_prices: [ElectricityPriceModel]):

        insert_statement = self._load_sql_query(
            self.base_sql_path + 'electricity_price/insert_electricity_price.sql')
        update_statement = self._load_sql_query(
            self.base_sql_path + 'electricity_price/update_electricity_price.sql')

        def get_params(electricity_price):
            return {
                'datetime': electricity_price.datetime,
                'price': electricity_price.price
            }

        electricity_params_list = [get_params(electricity_price) for electricity_price in electricity_prices]

        with self.db_connection() as cursor:
            cursor.executemany(insert_statement, electricity_params_list)
            cursor.executemany(update_statement, electricity_params_list)

    def get_weather_data_after_date(self, date):
        select_statement = self._load_sql_query(
            self.base_sql_path + 'weather/get_weather_data_after_date.sql')

        params = {'datetime': date}

        with self.db_connection() as cursor:
            cursor.execute(select_statement, params)
            rows = cursor.fetchall()
        result = [WeatherModel(row['datetime'], row['cloud_cover'], row['temperature'], row['latitude'], row['longitude']) for row in rows]
        return result

    def get_electricity_price_data_after_date(self, date):
        select_statement = self._load_sql_query(
            self.base_sql_path + 'electricity_price/get_electricity_price_after_date.sql')

        params = {'datetime': date}

        with self.db_connection() as cursor:
            cursor.execute(select_statement, params)
            rows = cursor.fetchall()
        result = [ElectricityPriceModel(row['datetime'], row['price']) for row in rows]
        return result
