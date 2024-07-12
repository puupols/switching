from sqlalchemy import Table, Column, String, DateTime, Integer, Float, UniqueConstraint, ForeignKey, Enum
from src.switch_service.models.switch_data_model import SwitchDataType

def create_switch_data_table(metadata):
    """
    Create a table for switch data

    Arguments:
        metadata: SQLAlchemy MetaData object
    """
    return Table(
        'switch_data', metadata,
        Column('id', Integer, primary_key=True),
        Column('switch_id', Integer, ForeignKey('switch.id'), nullable=False),
        Column('data_type', Enum(SwitchDataType), nullable=False),
        Column('log_cre_date', DateTime, nullable=False),
        Column('value_text', String(50)),
        Column('value_number', Float),
        UniqueConstraint('switch_id', 'data_type', 'log_cre_date', name='switch_data_unique_constraint')
    )
