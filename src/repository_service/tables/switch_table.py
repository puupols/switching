from sqlalchemy import Table, Column, String, Integer, UniqueConstraint, ForeignKey


def create_switch_table(metadata):
    """
    Create a table for switch data

    Arguments:
        metadata: SQLAlchemy MetaData object
    """
    return Table(
        'switch', metadata,
        Column('id', Integer, primary_key=True),
        Column('uuid', String(80), nullable=False, unique=True),
        Column('place_id', Integer, ForeignKey('place.id'), nullable=False),
        Column('name', String(80), nullable=False),
        Column('status', String(80)),
        Column('status_calculation_logic', String(2000)),
        UniqueConstraint('place_id', 'uuid', name='uix_place_id_uuid')
    )
