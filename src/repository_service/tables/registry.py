from src.repository_service.tables.weather_table import create_weather_table
from src.repository_service.tables.electricity_price_table import create_electricity_price_table
from src.repository_service.tables.switch_table import create_switch_table
from src.repository_service.tables.user_table import create_user_table
from src.repository_service.tables.place_table import create_place_table
from src.repository_service.tables.location_table import create_location_table
from src.repository_service.tables.switch_data_table import create_switch_data_table


def initialize_tables(metadata):
    """
    Initialize all tables

    Arguments:
        metadata: SQLAlchemy MetaData object

    Returns:
        tables: dict of tables
    """
    tables = {
        'weather': create_weather_table(metadata),
        'electricity_price': create_electricity_price_table(metadata),
        'switch': create_switch_table(metadata),
        'switch_data': create_switch_data_table(metadata),
        'user': create_user_table(metadata),
        'place': create_place_table(metadata),
        'location': create_location_table(metadata)
    }
    return tables
