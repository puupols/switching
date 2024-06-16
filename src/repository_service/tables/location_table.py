from sqlalchemy import Table, Column, UniqueConstraint, Float, Integer


def create_location_table(metadata):
    """
    Create a table for location data

    Arguments:
        metadata: SQLAlchemy MetaData object
    """
    return Table(
        'location', metadata,
        Column('id', Integer, primary_key=True),
        Column('latitude', Float, nullable=False),
        Column('longitude', Float, nullable=False),
        UniqueConstraint('latitude', 'longitude', name='uix_location_lat_lon')
    )
