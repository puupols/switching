import inject
from src.main import Main
from src.logger import logger_config
from src.injections.injections import app_injection_configuration


def create_app():
    """
    The main entry point of the REST API.

    This function configures the application's logging, sets up dependency injection,
    and starts the main application process. It serves as the central launching point
    for the application's execution.

    Steps:
    1. Sets up the logging configuration to capture and log application activities.
    2. Configures global dependency injections to manage and instantiate services and components throughout the application.
    3. Initializes the main application
    4. Returns Flask application from main application
    """
    logger_config.setup_logger()
    inject.configure(app_injection_configuration)
    main_app = Main()
    return main_app.return_app()
