from unittest import TestCase
from src.repository_service.tables import switch_data_table
from sqlalchemy import MetaData, Table


class TestSwitchDataTable(TestCase):

    def test_should_create_table_with_correct_columns_and_constraints(self):
        # Setup
        mock_metadata = MetaData()
        expected_table_name = 'switch_data'

        # Actions
        created_table = switch_data_table.create_switch_data_table(mock_metadata)

        # Assert
        self.assertIsInstance(created_table, Table)
        self.assertEqual(created_table.name, expected_table_name)
        self.assertEqual(len(created_table.columns), 6)
        self.assertEqual(len(created_table.constraints), 3)
        self.assertIn('id', created_table.columns)
        self.assertIn('switch_id', created_table.columns)
        self.assertIn('data_type', created_table.columns)
        self.assertIn('log_cre_date', created_table.columns)
        self.assertIn('value_text', created_table.columns)
        self.assertIn('value_number', created_table.columns)
        self.assertTrue(created_table.columns['id'].primary_key)
