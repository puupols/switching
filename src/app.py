import inject
from src.main import Main
from src.logger import logger_config
from src.injections.injections import app_injection_configuration


def main():
    logger_config.setup_logger()
    inject.configure(app_injection_configuration)
    main_app = Main()
    main_app.run()


if __name__ == '__main__':
    main()
