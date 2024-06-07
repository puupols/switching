from unittest import TestCase
from src.repository_service.tables import weather_table
from sqlalchemy import MetaData, Table


class TestWeatherTable(TestCase):

    def test_should_create_table_with_correct_columns_and_constraints(self):
        # Setup
        metadata = MetaData()
        expected_table_name = 'weather'

        # Actions
        created_table = weather_table.create_weather_table(metadata)

        # Asserts
        self.assertIsInstance(created_table, Table)
        self.assertEqual(expected_table_name, created_table.name)
        self.assertEqual(7, len(created_table.columns))
        self.assertTrue(created_table.columns['id'].primary_key)
        self.assertTrue(created_table.columns['datetime'].index)
        self.assertTrue(created_table.columns['latitude'].index)
        self.assertTrue(created_table.columns['longitude'].index)
        for constraint in created_table.constraints:
            if constraint.name == 'uix_datetime_lat_long':
                self.assertEqual(3, len(constraint.columns))
                self.assertIn('datetime', constraint.columns)
                self.assertIn('latitude', constraint.columns)
                self.assertIn('longitude', constraint.columns)




