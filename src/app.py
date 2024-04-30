import inject
from main import Main
from logger import logger_config
from injections.injections import app_injection_configuration

if __name__ == '__main__':
    logger_config.setup_logger()
    inject.configure(app_injection_configuration)
    main_app = Main()
    main_app.run()
