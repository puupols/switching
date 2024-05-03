import unittest
from src.repository_service.sqllite_repository_service import SQLLiteRepositoryService
from unittest.mock import patch, Mock, call
from src.weather_service.models.weather_model import WeatherModel
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel


class TestSQLLiteRepositoryService(unittest.TestCase):

    def setUp(self):
        self.patch1 = patch('src.repository_service.sqllite_repository_service.sqlite3.connect')
        self.mock_sqlite3_connect = self.patch1.start()
        self.mock_connection = Mock()
        self.mock_sqlite3_connect.return_value = self.mock_connection
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    def tearDown(self):
        self.patch1.stop()

    @patch('src.repository_service.sqllite_repository_service.SQLLiteRepositoryService._load_sql_query')
    def test_initialization(self, load_query):
        load_query.return_value = 'query_to_execute'
        self.service = SQLLiteRepositoryService()
        self.mock_connection.cursor.assert_called_once()
        load_query.assert_called_once()
        self.mock_cursor.executescript.assert_called_once_with('query_to_execute')
        self.mock_connection.commit.assert_called_once()
        self.mock_connection.close.assert_called_once()

    @patch('src.repository_service.sqllite_repository_service.SQLLiteRepositoryService._load_sql_query')
    def test_store_weather_data(self, load_query):
        # Setup
        load_query.side_effect = ['initialize_scripts', 'insert_statement', 'update_statement']
        weather_data = [WeatherModel(datetime='2023-04-01', cloud_cover=50, temperature=22,
                                     latitude=34.05, longitude=-118.25, sunshine_duration=6)]

        # Actions
        self.service = SQLLiteRepositoryService()
        self.service.store_weather_data(weather_data)

        # Asserts
        calls = [call('update_statement', [{'datetime': '2023-04-01', 'cloud_cover': 50,
                                            'temperature': 22, 'latitude': 34.05,
                                            'longitude': -118.25, 'sunshine_duration': 6}]),
                 call('insert_statement', [{'datetime': '2023-04-01', 'cloud_cover': 50,
                                            'temperature': 22, 'latitude': 34.05,
                                            'longitude': -118.25, 'sunshine_duration': 6}])
                 ]
        self.mock_cursor.executemany.assert_has_calls(calls)
        self.mock_connection.cursor.assert_called()
        self.mock_connection.commit.assert_called()
        self.mock_connection.close.assert_called()

    @patch('src.repository_service.sqllite_repository_service.SQLLiteRepositoryService._load_sql_query')
    def test_store_electricity_data(self, load_query):
        # Setup
        load_query.side_effect = ['initialize_scripts', 'insert_statement', 'update_statement']
        electricity_price_data = [ElectricityPriceModel(datetime='2023-04-01', price=50),
                                  ElectricityPriceModel(datetime='2023-04-03', price=53)]

        # Actions
        self.service = SQLLiteRepositoryService()
        self.service.store_electricity_price_data(electricity_price_data)

        # Asserts
        calls = [call('update_statement', [{'datetime': '2023-04-01', 'price': 50},
                                           {'datetime': '2023-04-03', 'price': 53}]),
                 call('insert_statement', [{'datetime': '2023-04-01', 'price': 50},
                                           {'datetime': '2023-04-03', 'price': 53}])]
        self.mock_cursor.executemany.assert_has_calls(calls)
        self.mock_connection.cursor.assert_called()
        self.mock_connection.commit.assert_called()
        self.mock_connection.close.assert_called()

    @patch('src.repository_service.sqllite_repository_service.SQLLiteRepositoryService._load_sql_query')
    def test_get_weather_data_after_date(self, load_query):
        # Setup
        load_query.side_effect = ['initialize_scripts', 'get_data_query']
        date = '2023-04-01'
        self.mock_cursor.fetchall.return_value = [
            {'datetime': '2023-04-01', 'cloud_cover': 50, 'temperature': 30, 'latitude': 52.3, 'longitude': 24.6,
             'sunshine_duration': 3600}]
        expected_result = [WeatherModel(datetime='2023-04-01', cloud_cover=50, temperature=30,
                                        latitude=52.3, longitude=24.6, sunshine_duration=3600)]

        # Actions
        self.service = SQLLiteRepositoryService()
        result = self.service.get_weather_data_after_date(date)

        # Asserts
        self.mock_cursor.execute.assert_called_once_with('get_data_query', {'datetime': date})
        self.mock_cursor.fetchall.assert_called_once()
        for actual, expected in zip(result, expected_result):
            self.assertEqual(actual.datetime, expected.datetime)
            self.assertEqual(actual.cloud_cover, expected.cloud_cover)
            self.assertEqual(actual.temperature, expected.temperature)
            self.assertEqual(actual.latitude, expected.latitude)
            self.assertEqual(actual.longitude, expected.longitude)
            self.assertEqual(actual.sunshine_duration, expected.sunshine_duration)

    @patch('src.repository_service.sqllite_repository_service.SQLLiteRepositoryService._load_sql_query')
    def test_get_electricity_price_data_after_date(self, load_query):
        # Setup
        load_query.side_effect = ['initialize_scripts', 'get_data_query']
        date = '2023-04-01'
        self.mock_cursor.fetchall.return_value = [{'datetime': '2023-04-01', 'price': 50},
                                                  {'datetime': '2023-04-02', 'price': 52}]
        expected_result = [ElectricityPriceModel(datetime='2023-04-01', price=50),
                           ElectricityPriceModel(datetime='2023-04-02', price=52)]

        # Actions
        self.service = SQLLiteRepositoryService()
        result = self.service.get_electricity_price_data_after_date(date)

        # Asserts
        self.mock_cursor.execute.assert_called_once_with('get_data_query', {'datetime': date})
        self.mock_cursor.fetchall.assert_called_once()
        for actual, expected in zip(result, expected_result):
            self.assertEqual(actual.datetime, expected.datetime)
            self.assertEqual(actual.price, expected.price)
