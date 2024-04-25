from repository_service.base_repository_service import BaseRepositoryService
from weather_service.models.weather_model import WeatherModel
from electricity_price_service.models.electricity_price_model import ElectricityPriceModel
import sqlite3


class SQLLiteRepositoryService(BaseRepositoryService):

    def __init__(self):
        super().__init__()
        self.initialize_database()

    def initialize_database(self):
        connection = sqlite3.connect('repository_service/sql_lite_db/switching.db')
        cursor = connection.cursor()
        init_query = self._load_sql_query('repository_service/sql_lite_db/sql/initialize/initialize_database.sql')
        cursor.executescript(init_query)
        connection.commit()
        connection.close()

    def _load_sql_query(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()


    def store_weather_data(self, weather_data: [WeatherModel]):
        connection = sqlite3.connect('repository_service/sql_lite_db/switching.db')
        cursor = connection.cursor()
        insert_statement = self._load_sql_query('repository_service/sql_lite_db/sql/weather/insert_weather.sql')
        update_statement = self._load_sql_query('repository_service/sql_lite_db/sql/weather/update_weather.sql')
        for weather in weather_data:
            cursor.execute(insert_statement, (weather.datetime, weather.cloud_cover, weather.temperature, weather.datetime))
            cursor.execute(update_statement, (weather.cloud_cover, weather.temperature, weather.datetime))
        connection.commit()
        connection.close()

    def store_electricity_price_data(self, electricity_prices: [ElectricityPriceModel]):
        connection = sqlite3.connect('repository_service/sql_lite_db/switching.db')
        cursor = connection.cursor()
        insert_statement = self._load_sql_query('repository_service/sql_lite_db/sql/electricity_price/insert_electricity_price.sql')
        update_statement = self._load_sql_query('repository_service/sql_lite_db/sql/electricity_price/update_electricity_price.sql')
        for electricity_price in electricity_prices:
            cursor.execute(insert_statement,
                           (electricity_price.datetime, electricity_price.price, electricity_price.datetime))
            cursor.execute(update_statement, (electricity_price.price, electricity_price.datetime))
        connection.commit()
        connection.close()

    def get_weather_data_after_date(self, date):
        connection = sqlite3.connect('repository_service/sql_lite_db/switching.db')
        cursor = connection.cursor()
        select_statement = self._load_sql_query(
            'repository_service/sql_lite_db/sql/weather/get_weather_data_after_date.sql')
        cursor.execute(select_statement, (date,))
        result = cursor.fetchall()
        connection.close()
        return result
