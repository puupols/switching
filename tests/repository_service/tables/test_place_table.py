from unittest import TestCase
from src.repository_service.tables import place_table
from sqlalchemy import MetaData, Table


class TestPlaceTable(TestCase):

    def test_should_create_table_with_correct_columns_and_constraints(self):
        # Setup
        mock_metadata = MetaData()
        expected_table_name = 'place'

        # Actions
        created_table = place_table.create_place_table(mock_metadata)

        # Assert
        self.assertIsInstance(created_table, Table)
        self.assertEqual(created_table.name, expected_table_name)
        self.assertEqual(len(created_table.columns), 5)
        self.assertEqual(len(created_table.constraints), 4)
        self.assertIn('id', created_table.columns)
        self.assertIn('user_id', created_table.columns)
        self.assertIn('location_id', created_table.columns)
        self.assertIn('name', created_table.columns)
        self.assertIn('description', created_table.columns)
        self.assertTrue(created_table.columns['id'].primary_key)
        self.assertFalse(created_table.columns['name'].nullable)

