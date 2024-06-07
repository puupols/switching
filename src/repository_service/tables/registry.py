from src.repository_service.tables.weather_table import create_weather_table
from src.repository_service.tables.electricity_price_table import create_electricity_price_table
from src.repository_service.tables.switch_table import create_switch_table


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
        'switch': create_switch_table(metadata)
    }
    return tables
