import logging

import inject
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, registry

from src.configuration.base_configuration import BaseConfiguration
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel
from src.repository_service.tables.registry import initialize_tables
from src.switch_service.models.switch_model import SwitchModel
from src.user_service.models.user_model import UserModel
from src.weather_service.models.weather_model import WeatherModel
from src.place_service.models.place_model import PlaceModel
from src.location_service.models.location_model import LocationModel
from src.switch_service.models.switch_data_model import SwitchDataModel


class BaseRepositoryService:
    DATABASE_STRING_CONFIG_NAME = "database_string"

    @inject.autoparams()
    def __init__(self, configuration: BaseConfiguration):
        """
        Initializes the RepositoryService with the provided configuration.
        Creates the SQLAlchemy engine, session maker, and metadata objects.
        Initializes the database tables.
        """
        self.configuration = configuration
        self.logger = logging.getLogger(__name__)
        self.engine = create_engine(configuration.get(self.DATABASE_STRING_CONFIG_NAME))
        self.session_maker = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.mapper_registry = registry()
        self.tables = initialize_tables(self.metadata)

    def create_database(self):
        """
        Creates the database and maps models to the respective tables.
        """
        self.mapper_registry.map_imperatively(WeatherModel, self.tables['weather'])
        self.mapper_registry.map_imperatively(ElectricityPriceModel, self.tables['electricity_price'])
        self.mapper_registry.map_imperatively(SwitchModel, self.tables['switch'])
        self.mapper_registry.map_imperatively(LocationModel, self.tables['location'])
        self.mapper_registry.map_imperatively(UserModel, self.tables['user'])
        self.mapper_registry.map_imperatively(PlaceModel, self.tables['place'])
        self.mapper_registry.map_imperatively(SwitchDataModel, self.tables['switch_data'])
        self.metadata.create_all(self.engine)
