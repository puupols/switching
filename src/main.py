
import inject
from src.job_service.job_service import JobService
from src.rest_api.flask_rest_api import FlaskRESTAPI
from src.repository_service.repository_service import RepositoryService


class Main:
    """
    The main controller class that manages the startup and coordination of background jobs and REST API services.

    This class is responsible for initializing and running essential services of the application. It ensures that
    both the job scheduling service and the REST API are started properly to enable full functionality of the system.

    Attributes:
        job_service (JobService): The service responsible for managing and scheduling background jobs.
        rest_api (FlaskRESTAPI): The REST API service that handles HTTP requests.
    """

    @inject.autoparams()
    def __init__(self, job_service: JobService, rest_api: FlaskRESTAPI, repository_service: RepositoryService):
        """
        Initializes the Main class with a job service and REST API service.

        Args:
            job_service (JobService): An instance of JobService to manage background job scheduling.
            rest_api (FlaskRESTAPI): An instance of FlaskRESTAPI to handle and respond to RESTful requests.
        """
        self.job_service = job_service
        self.rest_api = rest_api
        self.repository_service = repository_service

    def run(self):
        """
        Starts the job service and the REST API service.

        This method orchestrates the startup of the job service to begin executing scheduled jobs
        and launches the REST API to handle incoming HTTP requests.
        """
        self.repository_service.create_database()
        self.job_service.plan_jobs()
        self.rest_api.run_app()

