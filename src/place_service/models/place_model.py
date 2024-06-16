class PlaceModel:
    id: int
    user_id: int
    location_id: int
    name: str
    description: str
    switches: list
    location: dict

    def __init__(self, user_id, location_id, name, description, id=None, switches=None, location=None):
        self.id = id
        self.user_id = user_id
        self.location_id = location_id
        self.name = name
        self.description = description
        self.switches = switches
        self.location = location
