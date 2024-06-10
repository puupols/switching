import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import clear_mappers
from sqlalchemy.exc import IntegrityError
from src.configuration.base_configuration import BaseConfiguration
from src.repository_service.switch_repository_service import SwitchRepositoryService
from src.switch_service.models.switch_model import SwitchModel


class TestRepositoryService(unittest.TestCase):

    def setUp(self):
        self.mock_configuration = MagicMock(spec=BaseConfiguration)
        self.mock_configuration.get.return_value = "sqlite:///:memory:"
        self.switch_repository_service = SwitchRepositoryService(configuration=self.mock_configuration)
        self.switch_repository_service.create_database()

    def tearDown(self):
        self.switch_repository_service.metadata.drop_all(self.switch_repository_service.engine)
        clear_mappers()
        self.switch_repository_service.engine.dispose()

    def test_store_switch_data(self):
        # Setup
        switch = SwitchModel(name="Switch 1", status_calculation_logic="status_calculation_logic")
        expected_name = switch.name
        # Actions
        self.switch_repository_service.store_switch_data(switch)
        with self.switch_repository_service.session_maker() as session:
            stored_data = session.query(SwitchModel).all()

        # Asserts
        self.assertEqual(len(stored_data), 1)
        self.assertEqual(stored_data[0].name, expected_name)

    def test_store_switch_data_if_already_exists(self):
        # Setup
        switch = SwitchModel(name="Switch 1", status_calculation_logic="status_calculation_logic")
        duplicate_switch = SwitchModel(name="Switch 1", status_calculation_logic="new_status_calculation_logic")

        # Actions
        self.switch_repository_service.store_switch_data(switch)

        # Asserts
        with self.assertRaises(IntegrityError):
            self.switch_repository_service.store_switch_data(duplicate_switch)

    def test_update_switch_data(self):
        # Setup
        switch = SwitchModel(name="Switch 1", status_calculation_logic="status_calculation_logic")
        updated_switch = SwitchModel(name="Switch 1", status_calculation_logic="new_status_calculation_logic")

        # Actions
        self.switch_repository_service.store_switch_data(switch)
        self.switch_repository_service.update_switch_data(updated_switch)
        changed_switch = self.switch_repository_service.get_switch("Switch 1")

        # Asserts
        self.assertEqual(changed_switch.status_calculation_logic, "new_status_calculation_logic")

    def test_update_switch_data_if_not_exists(self):
        # Setup
        switch = SwitchModel(name="Switch 1", status_calculation_logic="status_calculation_logic")
        updated_switch = SwitchModel(name="Switch 2", status_calculation_logic="new_status_calculation_logic")

        # Actions
        self.switch_repository_service.store_switch_data(switch)

        # Asserts
        with self.assertRaises(ValueError):
            self.switch_repository_service.update_switch_data(updated_switch)

    def test_get_switch(self):
        # Setup
        switch = SwitchModel(name="Switch 1", status_calculation_logic="status_calculation_logic")
        expected_name = switch.name

        # Actions
        self.switch_repository_service.store_switch_data(switch)
        result = self.switch_repository_service.get_switch("Switch 1")

        # Asserts
        self.assertEqual(result.name, expected_name)

    def test_get_switch_if_not_exists(self):
        # Setup
        switch = SwitchModel(name="Switch 1", status_calculation_logic="status_calculation_logic")

        # Actions
        self.switch_repository_service.store_switch_data(switch)

        # Asserts
        with self.assertRaises(ValueError):
            self.switch_repository_service.get_switch("Switch 2")
