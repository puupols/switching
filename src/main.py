
import inject
from src.job_service.job_service import JobService
from src.rest_api.flask_rest_api import FlaskRESTAPI


class Main:

    @inject.autoparams()
    def __init__(self, job_service: JobService, rest_api: FlaskRESTAPI):
        self.job_service = job_service
        self.rest_api = rest_api

    def run(self):
        self.job_service.plan_jobs()
        self.rest_api.run_app()

