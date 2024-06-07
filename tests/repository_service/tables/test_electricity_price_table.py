from unittest import TestCase
from src.repository_service.tables import electricity_price_table
from sqlalchemy import MetaData, Table

class TestElectricityPriceTable(TestCase):


    def test_should_create_table_with_correct_columns_and_constraints(self):
        # Arrange
        mock_metadata = MetaData()
        expected_table_name = 'electricity_price'

        # Act
        created_table = electricity_price_table.create_electricity_price_table(mock_metadata)

        # Assert
        self.assertIsInstance(created_table, Table)
        self.assertEqual(created_table.name, expected_table_name)
        self.assertEqual(len(created_table.columns), 3)
        self.assertEqual(len(created_table.constraints), 2)
        self.assertIn('id', created_table.columns)
        self.assertIn('datetime', created_table.columns)
        self.assertIn('price', created_table.columns)
        self.assertTrue(created_table.c['id'].primary_key)
        self.assertTrue(created_table.c['datetime'].index)
        self.assertTrue(created_table.c['price'].nullable)
        self.assertTrue(created_table.c['datetime'].unique)
        for constraint in created_table.constraints:
            if constraint.name == 'pk_electricity_price':
                self.assertTrue(constraint.primary_key)
            if constraint.name == 'uq_electricity_price_datetime':
                self.assertTrue(constraint.unique)
                self.assertIn('datetime', constraint.columns)
