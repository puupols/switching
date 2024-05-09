import unittest
from unittest.mock import Mock
from src.main import Main


class TestMain(unittest.TestCase):

    def setUp(self):
        self.mock_job_service = Mock()
        self.mock_rest_api = Mock()
        self.mock_main = Main(self.mock_job_service, self.mock_rest_api)

    def test_init(self):
        # Asserts
        self.assertEqual(self.mock_main.rest_api, self.mock_rest_api)
        self.assertEqual(self.mock_job_service, self.mock_job_service)

    def test_run(self):
        # Actions
        self.mock_main.run()

        # Asserts
        self.mock_job_service.plan_jobs.assert_called_once()
        self.mock_rest_api.run_app.assert_called_once()
