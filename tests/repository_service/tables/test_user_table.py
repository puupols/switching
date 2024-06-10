from unittest import TestCase
from src.repository_service.tables import user_table
from sqlalchemy import MetaData, Table


class TestUserTable(TestCase):

    def test_should_create_table_with_correct_columns_and_constraints(self):
        # Setup
        mock_metadata = MetaData()
        expected_table_name = 'user'

        # Actions
        created_table = user_table.create_user_table(mock_metadata)

        # Assert
        self.assertIsInstance(created_table, Table)
        self.assertEqual(created_table.name, expected_table_name)
        self.assertIn('id', created_table.columns)
        self.assertIn('user_name', created_table.columns)
        self.assertIn('user_email', created_table.columns)
        self.assertIn('password', created_table.columns)
        self.assertTrue(created_table.columns['id'].primary_key)
        self.assertTrue(created_table.columns['user_name'].unique)



