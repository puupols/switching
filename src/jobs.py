import inject
from src.main import Main
from src.logger import logger_config
from src.injections.injections import app_injection_configuration


def start_jobs():
    """
    The main entry point for starting scheduled jobs within the application.

    This function configures the application's logging, sets up dependency injection,
    and initiates the main job execution process. It serves as the central launching
    point for the execution of scheduled jobs within the application.

    Steps:
    1. Sets up the logging configuration to capture and log application activities.
    2. Configures global dependency injections to manage and instantiate services
       and components throughout the application.
    3. Initializes the main application class and starts the execution of scheduled jobs.
    """
    logger_config.setup_logger()
    inject.configure(app_injection_configuration)
    main_app = Main()
    main_app.run_jobs()

