import unittest
from unittest.mock import Mock
from src.main import Main


class TestMain(unittest.TestCase):

    def setUp(self):
        self.mock_job_service = Mock()
        self.mock_rest_api = Mock()
        self.mock_repository_service = Mock()
        self.mock_main = Main(self.mock_job_service, self.mock_rest_api, self.mock_repository_service)

    def test_init(self):
        # Asserts
        self.assertEqual(self.mock_main.rest_api, self.mock_rest_api)
        self.assertEqual(self.mock_main.job_service, self.mock_job_service)
        self.assertEqual(self.mock_main.repository_service, self.mock_repository_service)

    def test_return_app(self):
        # Actions
        mock_return_value = self.mock_main.return_app()

        # Asserts
        self.mock_repository_service.create_database.assert_called_once()
        self.assertEqual(mock_return_value, self.mock_rest_api.app)

    def test_run_jobs(self):
        # Actions
        self.mock_main.run_jobs()

        # Asserts
        self.mock_repository_service.create_database.assert_called_once()
        self.mock_job_service.plan_jobs.assert_called_once()
