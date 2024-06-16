from unittest import TestCase
from src.repository_service.tables import location_table
from sqlalchemy import MetaData, Table


class TestPlaceTable(TestCase):

    def test_should_create_table_with_correct_columns_and_constraints(self):
        # Setup
        mock_metadata = MetaData()
        expected_table_name = 'location'

        # Actions
        created_table = location_table.create_location_table(mock_metadata)

        # Assert
        self.assertIsInstance(created_table, Table)
        self.assertEqual(created_table.name, expected_table_name)
        self.assertEqual(len(created_table.columns), 3)
        self.assertEqual(len(created_table.constraints), 2)
        self.assertIn('id', created_table.columns)
        self.assertIn('latitude', created_table.columns)
        self.assertIn('longitude', created_table.columns)
        self.assertTrue(created_table.columns['id'].primary_key)
        self.assertFalse(created_table.columns['latitude'].nullable)
        self.assertFalse(created_table.columns['longitude'].nullable)

