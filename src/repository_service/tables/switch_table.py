from sqlalchemy import Table, Column, String, Integer


def create_switch_table(metadata):
    """
    Create a table for switch data

    Arguments:
        metadata: SQLAlchemy MetaData object
    """
    return Table(
        'switch', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(80), unique=True, nullable=False),
        Column('status', String(80)),
        Column('status_calculation_logic', String(2000))
    )
