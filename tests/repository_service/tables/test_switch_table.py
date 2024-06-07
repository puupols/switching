from unittest import TestCase
from src.repository_service.tables import switch_table
from sqlalchemy import MetaData, Table


class TestSwitchTable(TestCase):

    def test_should_create_table_with_correct_columns_and_constraints(self):
        # Setup
        mock_metadata = MetaData()
        expected_table_name = 'switch'

        # Actions
        created_table = switch_table.create_switch_table(mock_metadata)

        # Assert
        self.assertIsInstance(created_table, Table)
        self.assertEqual(created_table.name, expected_table_name)
        self.assertEqual(len(created_table.columns), 4)
        self.assertEqual(len(created_table.constraints), 2)
        self.assertIn('id', created_table.columns)
        self.assertIn('name', created_table.columns)
        self.assertIn('status', created_table.columns)
        self.assertIn('status_calculation_logic', created_table.columns)
        self.assertTrue(created_table.columns['id'].primary_key)
        self.assertTrue(created_table.columns['name'].unique)
        self.assertFalse(created_table.columns['name'].nullable)

