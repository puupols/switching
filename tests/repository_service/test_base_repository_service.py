import unittest
from unittest.mock import MagicMock
from sqlalchemy import inspect
from sqlalchemy.orm import clear_mappers
from src.configuration.base_configuration import BaseConfiguration
from src.repository_service.base_repository_service import BaseRepositoryService


class TestRepositoryService(unittest.TestCase):

    def setUp(self):
        self.mock_configuration = MagicMock(spec=BaseConfiguration)
        self.mock_configuration.get.return_value = "sqlite:///:memory:"
        self.repository_service = BaseRepositoryService(configuration=self.mock_configuration)
        self.repository_service.create_database()

    def tearDown(self):
        self.repository_service.metadata.drop_all(self.repository_service.engine)
        clear_mappers()
        self.repository_service.engine.dispose()

    def test_create_database(self):
        # Setup
        inspector = inspect(self.repository_service.engine)

        # Asserts
        self.assertTrue(inspector.has_table('weather'))
        self.assertTrue(inspector.has_table('electricity_price'))
