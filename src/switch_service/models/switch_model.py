
class SwitchModel:
    """
    SwitchModel class is a model class for the switch object.
    """

    SWITCH_VALUE_IF_ERROR_OCCURRED = 'ERROR'
    SWITCH_VALUE_IF_SWITCH_NOT_IMPLEMENTED = 'NOT_FOUND'

    name: str
    place_id: int
    status: str
    status_calculation_logic: str

    def __init__(self, name, place_id, status_calculation_logic, status=None, id=None):
        self.id = id
        self.name = name
        self.place_id = place_id
        self.status_calculation_logic = status_calculation_logic
        self.status = status
