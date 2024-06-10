from sqlalchemy import Table, Column, String, Integer


def create_user_table(metadata):
    """
    Create a table for user data

    Arguments:
        metadata: SQLAlchemy MetaData object
    """
    return Table(
        'user', metadata,
        Column('id', Integer, primary_key=True),
        Column('user_name', String(80), unique=True, nullable=False),
        Column('password', String(250), nullable=False),
        Column('user_email', String(80))
    )

