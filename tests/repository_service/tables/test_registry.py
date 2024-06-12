from src.repository_service.tables.registry import initialize_tables
from unittest import TestCase
from sqlalchemy import MetaData, Table


class TestRegistry(TestCase):

    def test_should_initialize_all_tables(self):
        # Setup
        metadata = MetaData()
        expected_table_names = ['weather', 'electricity_price', 'switch', 'user', 'place']

        # Actions
        tables = initialize_tables(metadata)

        # Asserts
        self.assertEqual(5, len(tables))
        for table_name in expected_table_names:
            self.assertIn(table_name, tables)
            self.assertEqual(table_name, tables[table_name].name)
            self.assertIsInstance(tables[table_name], Table)

