from sqlalchemy import Table, Column, Integer, DateTime, Float, UniqueConstraint


def create_electricity_price_table(metadata):
    """
    Create a table for electricity price data

    Arguments:
        metadata: SQLAlchemy MetaData object
    """
    return Table(
        'electricity_price', metadata,
        Column('id', Integer, primary_key=True),
        Column('datetime', DateTime, index=True, unique=True),
        Column('price', Float),
        UniqueConstraint('datetime', name='uix_datetime')
    )
