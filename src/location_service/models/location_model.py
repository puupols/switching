class LocationModel:

    id: int
    latitude: float
    longitude: float

    def __init__(self, latitude: float, longitude: float, id=None):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
