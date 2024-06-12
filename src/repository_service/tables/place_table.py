from sqlalchemy import Table, Column, String, Integer, UniqueConstraint, ForeignKey


def create_place_table(metadata):
    """
    Create a table for place data

    Arguments:
        metadata: SQLAlchemy MetaData object
    """
    return Table(
        'place', metadata,
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
        Column('name', String(80), nullable=False),
        Column('description', String(250), nullable=False),
        UniqueConstraint('user_id', 'name', name='uix_user_id_name')
    )
