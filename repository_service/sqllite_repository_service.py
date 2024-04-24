from repository_service.base_repository_service import BaseRepositoryService
from weather_service.models.weather_model import WeatherModel
import sqlite3


class SQLLiteRepositoryService(BaseRepositoryService):

    def __init__(self):
        super().__init__()
        self.initialize_database()

    def initialize_database(self):
        connection = sqlite3.connect('repository_service/sql_lite_db/switching.db')
        cursor = connection.cursor()
        init_query = self._load_sql_query('repository_service/sql_lite_db/queries/initialize/initialize_database.sql')
        cursor.execute(init_query)
        connection.commit()
        connection.close()

    def _load_sql_query(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()


    def store_weather_data(self, weather_data: [WeatherModel]):
        connection = sqlite3.connect('repository_service/sql_lite_db/switching.db')
        cursor = connection.cursor()
        insert_statement = self._load_sql_query('repository_service/sql_lite_db/queries/weather/insert_weather.sql')
        update_statement = self._load_sql_query('repository_service/sql_lite_db/queries/weather/update_weather.sql')
        for weather in weather_data:
            cursor.execute(insert_statement, (weather.datetime, weather.cloud_cover, weather.temperature, weather.datetime))
            cursor.execute(update_statement, (weather.cloud_cover, weather.temperature, weather.datetime))
        connection.commit()
        connection.close()

