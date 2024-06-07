
class SwitchModel:
    """
    SwitchModel class is a model class for the switch object.
    """

    SWITCH_VALUE_IF_ERROR_OCCURRED = 'ERROR'
    SWITCH_VALUE_IF_SWITCH_NOT_IMPLEMENTED = 'NOT_FOUND'

    name: str
    status: str
    status_calculation_logic: str

    def __init__(self, name, status_calculation_logic, status=None):
        self.name = name
        self.status_calculation_logic = status_calculation_logic
        self.status = status
