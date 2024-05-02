import unittest
from unittest.mock import Mock, patch
from src.job_service.job_service import JobService


class TestJobService(unittest.TestCase):

    @patch('src.job_service.job_service.BackgroundScheduler')
    def setUp(self, mock_scheduler):
        self.mock_weather_service = Mock()
        self.mock_electricity_price_service = Mock()
        self.mock_configuration = Mock()
        self.mock_job_service = JobService(self.mock_weather_service, self.mock_electricity_price_service,
                                           self.mock_configuration)
        self.mock_job_service.scheduler = mock_scheduler()

        self.mock_configuration.get.side_effect = lambda key: {
            'weather_data_regeneration_job_interval_in_minutes': 30,
            'electricity_price_data_regeneration_job_interval_in_minutes': 45
        }[key]

    def test_weather_data_regeneration_job_is_scheduled_correctly(self):
        # Action
        self.mock_job_service._plan_weather_data_regeneration_job()

        # Assert job is added correctly
        self.mock_job_service.scheduler.add_job.assert_called_once_with(
            self.mock_weather_service.regenerate_weather_data,
            'interval', minutes=30
        )

    def test_electricity_price_data_regeneration_job_is_scheduled_correctly(self):
        # Action
        self.mock_job_service._plan_electricity_price_data_regeneration_job()

        # Assert job is added correctly
        self.mock_job_service.scheduler.add_job.assert_called_once_with(
            self.mock_electricity_price_service.regenerate_electricity_price_data,
            'interval', minutes=45
        )

    @patch('src.job_service.job_service.JobService._plan_weather_data_regeneration_job')
    @patch('src.job_service.job_service.JobService._plan_electricity_price_data_regeneration_job')
    def test_plan_jobs_is_called_correctly(self, mock_plan_electricity, mock_plan_weather):
        # Action
        self.mock_job_service.plan_jobs()

        # Assert
        mock_plan_electricity.assert_called_once()
        mock_plan_weather.assert_called_once()
        self.mock_job_service.scheduler.start.assert_called_once()
