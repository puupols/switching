from sqlalchemy import Table, Column, Integer, Float, DateTime, UniqueConstraint


def create_weather_table(metadata):
    """
    Create a table for weather data

    Arguments:
        metadata: SQLAlchemy MetaData object
    """
    return Table(
        'weather', metadata,
        Column('id', Integer, primary_key=True),
        Column('datetime', DateTime, index=True),
        Column('cloud_cover', Float),
        Column('temperature', Float),
        Column('latitude', Float, index=True),
        Column('longitude', Float, index=True),
        Column('sunshine_duration', Float),
        UniqueConstraint('datetime', 'latitude', 'longitude', name='uix_datetime_lat_long')
    )
