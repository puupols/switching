from enum import Enum
from datetime import datetime

class SwitchDataType(Enum):
    RELAY_STATUS = "RELAY_STATUS"
    TEMPERATURE = "TEMPERATURE"


class SwitchDataModel:
    """
    SwitchDataModel class is a model class for the switch data object.
    """

    id: int
    switch_id: int
    data_type: SwitchDataType
    log_cre_date: datetime
    value_text: str
    value_number: float

    def __init__(self, id: int = None, switch_id: int = None, data_type: SwitchDataType = None, log_cre_date: datetime = None, value_text: str = None,
                 value_number: float = None):
        """
        Initializes the SwitchDataModel with the provided values.

        Args:
            id (int): The id of the switch data.
            switch_id (int): The id of the switch.
            data_type (DataType): The type of the data.
            value_text (str): The text value of the data.
            value_number (float): The number value of the data.
        """
        self.id = id
        self.switch_id = switch_id
        self.data_type = data_type
        self.log_cre_date = log_cre_date
        self.value_text = value_text
        self.value_number = value_number
