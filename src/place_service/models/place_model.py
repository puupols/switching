
class PlaceModel:

    def __init__(self, user_id, name, description, id=None, switches=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.switches = switches
