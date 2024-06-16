from sqlalchemy import Table, Column, Integer, Float, DateTime, UniqueConstraint, ForeignKey


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
        Column('location_id', Integer, ForeignKey('location.id'), nullable=True),
        Column('sunshine_duration', Float),
        UniqueConstraint('datetime', 'latitude', 'longitude', name='uix_datetime_lat_long'),
        UniqueConstraint('datetime', 'location_id', name='uix_datetime_location_id')
    )
