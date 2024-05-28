from datetime import datetime


class WeatherModel:
    """
    A model class to represent detailed weather data at a specific datetime and location.

    This class encapsulates various weather parameters such as cloud cover, temperature, and sunshine duration
    for a given geographical location at a particular point in time. It is designed to store and facilitate
    the retrieval of weather attributes, which are typically fetched from an external weather service.

    Attributes:
        datetime (datetime): The specific date and time the weather data applies to.
        cloud_cover (float): The percentage of the sky occluded by clouds.
        temperature (float): The air temperature in degrees Celsius at the specified datetime and location.
        latitude (float): The latitude of the location for which the weather data is applicable.
        longitude (float): The longitude of the location for which the weather data is applicable.
        sunshine_duration (float): The duration of sunshine in hours for the day on which this data point applies.
    """
    datetime: datetime
    cloud_cover: float
    temperature: float
    latitude: float
    longitude: float
    sunshine_duration: float

    def __init__(self, datetime, cloud_cover, temperature, latitude, longitude, sunshine_duration):
        self.datetime = datetime
        self.cloud_cover = cloud_cover
        self.temperature = temperature
        self.latitude = latitude
        self.longitude = longitude
        self.sunshine_duration = sunshine_duration
