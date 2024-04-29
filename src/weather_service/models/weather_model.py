
class WeatherModel:
    def __init__(self, datetime, cloud_cover, temperature, latitude, longitude, sunshine_duration):
        self.datetime = datetime
        self.cloud_cover = cloud_cover
        self.temperature = temperature
        self.latitude = latitude
        self.longitude = longitude
        self.sunshine_duration = sunshine_duration
