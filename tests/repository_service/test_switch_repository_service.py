import datetime
import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import clear_mappers
from sqlalchemy.exc import IntegrityError
from src.configuration.base_configuration import BaseConfiguration
from src.repository_service.switch_repository_service import SwitchRepositoryService
from src.switch_service.models.switch_model import SwitchModel
from src.place_service.models.place_model import PlaceModel
from src.switch_service.models.switch_data_model import SwitchDataType
from src.switch_service.models.switch_data_model import SwitchDataModel


class TestRepositoryService(unittest.TestCase):

    def setUp(self):
        self.mock_configuration = MagicMock(spec=BaseConfiguration)
        self.mock_configuration.get.return_value = "sqlite:///:memory:"
        self.switch_repository_service = SwitchRepositoryService(configuration=self.mock_configuration)
        self.switch_repository_service.create_database()
        self.place = PlaceModel(user_id=1, name="Place 1", description="Description 1", location_id=1, id=1)
        with self.switch_repository_service.session_maker() as session:
            session.add(self.place)
            session.commit()

    def tearDown(self):
        self.switch_repository_service.metadata.drop_all(self.switch_repository_service.engine)
        clear_mappers()
        self.switch_repository_service.engine.dispose()

    def test_get_switch_for_user(self):
        # Setup
        switch = SwitchModel(name="Switch 1", uuid='uuid_1', place_id='1', status_calculation_logic="status_calculation_logic")
        expected_name = switch.name
        # Actions
        self.switch_repository_service.store_switch_data(switch)
        result = self.switch_repository_service.get_switch_for_user("uuid_1", 1)

        # Asserts
        self.assertEqual(result.name, expected_name)

    def test_get_switch_for_user_if_not_exists(self):
        # Setup
        switch = SwitchModel(name="Switch 1", uuid='uuid_1', place_id='1', status_calculation_logic="status_calculation_logic")

        # Actions
        self.switch_repository_service.store_switch_data(switch)

        # Asserts
        with self.assertRaises(ValueError):
            self.switch_repository_service.get_switch_for_user("uuid_1", 2)

    def test_store_switch_data(self):
        # Setup
        switch = SwitchModel(name="Switch 1", uuid='uuid_1', place_id='1', status_calculation_logic="status_calculation_logic")
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
        switch = SwitchModel(name="Switch 1", uuid='uuid_1', place_id='1', status_calculation_logic="status_calculation_logic")
        duplicate_switch = SwitchModel(name="Switch 1", uuid='uuid_1', place_id='1', status_calculation_logic="new_status_calculation_logic")

        # Actions
        self.switch_repository_service.store_switch_data(switch)

        # Asserts
        with self.assertRaises(IntegrityError):
            self.switch_repository_service.store_switch_data(duplicate_switch)

    def test_update_switch_data(self):
        # Setup
        uuid = 'uuid_1'
        switch = SwitchModel(name="Switch 1", uuid=uuid, place_id='1', status_calculation_logic="status_calculation_logic")
        updated_switch = SwitchModel(name="Switch 1", uuid=uuid, place_id='1', status_calculation_logic="new_status_calculation_logic")

        # Actions
        self.switch_repository_service.store_switch_data(switch)
        self.switch_repository_service.update_switch_data(updated_switch, 1, uuid)
        changed_switch = self.switch_repository_service.get_switch("1")

        # Asserts
        self.assertEqual(changed_switch.status_calculation_logic, "new_status_calculation_logic")

    def test_update_switch_data_if_not_allowed_for_user(self):
        # Setup
        uuid = 'uuid_1'
        switch = SwitchModel(name="Switch 1", uuid=uuid, place_id='1', status_calculation_logic="status_calculation_logic")
        updated_switch = SwitchModel(name="Switch 1", uuid=uuid, place_id='1', status_calculation_logic="new_status_calculation_logic")

        # Actions
        self.switch_repository_service.store_switch_data(switch)

        # Asserts
        with self.assertRaises(ValueError):
            self.switch_repository_service.update_switch_data(updated_switch, 2, uuid)

    def test_update_switch_data_if_not_exists(self):
        # Setup
        uuid = 'uuid_1'
        uuid_2 = 'uuid_2'
        switch = SwitchModel(name="Switch 1", uuid=uuid, place_id='1', status_calculation_logic="status_calculation_logic")
        updated_switch = SwitchModel(name="Switch 2", uuid=uuid_2, place_id='1', status_calculation_logic="new_status_calculation_logic")

        # Actions
        self.switch_repository_service.store_switch_data(switch)

        # Asserts
        with self.assertRaises(ValueError):
            self.switch_repository_service.update_switch_data(updated_switch, 1, uuid_2)

    def test_get_switch(self):
        # Setup
        switch = SwitchModel(name="Switch 1", uuid='uuid_1', place_id='1', status_calculation_logic="status_calculation_logic")
        expected_name = switch.name

        # Actions
        self.switch_repository_service.store_switch_data(switch)
        result = self.switch_repository_service.get_switch("1")

        # Asserts
        self.assertEqual(result.name, expected_name)

    def test_get_switch_if_not_exists(self):
        # Setup
        switch = SwitchModel(name="Switch 1", uuid="uuid_1", place_id='1', status_calculation_logic="status_calculation_logic")

        # Actions
        self.switch_repository_service.store_switch_data(switch)

        # Asserts
        with self.assertRaises(ValueError):
            self.switch_repository_service.get_switch("uuid_2")

    def test_store_switch_operational_data(self):
        # Setup
        switch = SwitchModel(name="Switch 1", uuid='uuid_1', place_id='1', status_calculation_logic="status_calculation_logic")
        switch_data = SwitchDataModel(switch_id=1, data_type=SwitchDataType.RELAY_STATUS, log_cre_date=datetime.datetime.now(), value_text="ON")
        expected_value_text = switch_data.value_text

        # Actions
        self.switch_repository_service.store_switch_data(switch)
        self.switch_repository_service.store_switch_operational_data(switch_data)
        with self.switch_repository_service.session_maker() as session:
            stored_data = session.query(SwitchDataModel).all()

        # Asserts
        self.assertEqual(len(stored_data), 1)
        self.assertEqual(stored_data[0].value_text, expected_value_text)

