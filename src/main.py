import inject
from src.job_service.job_service import JobService
from src.rest_api.flask_rest_api import FlaskRESTAPI
from src.repository_service.base_repository_service import BaseRepositoryService


class Main:
    """
    The main controller class that manages the startup and coordination of background jobs, REST API services,
    and repository service.

    This class is responsible for initializing and running essential services of the application. It ensures that
    the job scheduling service, the REST API, and the repository service are started properly to enable full functionality
    of the system.

    Attributes:
        job_service (JobService): The service responsible for managing and scheduling background jobs.
        rest_api (FlaskRESTAPI): The REST API service that handles HTTP requests.
        repository_service (BaseRepositoryService): The service responsible for managing database interactions.
    """

    @inject.autoparams()
    def __init__(self, job_service: JobService, rest_api: FlaskRESTAPI, repository_service: BaseRepositoryService):
        """
        Initializes the Main class with a job service, REST API service, and repository service.

        Args:
            job_service (JobService): An instance of JobService to manage background job scheduling.
            rest_api (FlaskRESTAPI): An instance of FlaskRESTAPI to handle and respond to RESTful requests.
            repository_service (BaseRepositoryService): An instance of RepositoryService to manage database interactions.
        """
        self.job_service = job_service
        self.rest_api = rest_api
        self.repository_service = repository_service

    def return_app(self):
        """
        Prepares the application by creating the database and returns the Flask app instance.

        This method ensures the database is set up and ready before returning the Flask app instance for handling
        HTTP requests.

        Returns:
            Flask: The Flask app instance configured to handle RESTful requests.
        """
        self.repository_service.create_database()
        return self.rest_api.app

    def run_jobs(self):
        """
        Starts the job service and the REST API service.

        This method orchestrates the startup of the job service to begin executing scheduled jobs,
        ensures the database is created.
        """
        self.repository_service.create_database()
        self.job_service.plan_jobs()
