from src.weather_service.processors.base_weather_processor import BaseWeatherProcessor
from src.weather_service.models.weather_model import WeatherModel
from datetime import datetime


class OpenMeteoWeatherProcessor(BaseWeatherProcessor):
    """
    Concrete implementation of BaseWeatherProcessor for processing weather data from Open Meteo.

    This processor transforms raw weather data fetched from the Open Meteo API into structured WeatherModel instances.
    Each model instance represents weather data for a specific time point including details like temperature,
    cloud cover, and sunshine duration at specified geographic coordinates.

    Attributes:
        OPEN_METEO_DATE_FORMAT (str): The date and time format used by the Open Meteo API.
    """
    OPEN_METEO_DATE_FORMAT = '%Y-%m-%dT%H:%M'

    def process_raw_data(self, raw_data, location_id):
        """
        Processes raw weather data from Open Meteo into WeatherModel instances.

        Parses the raw JSON data from Open Meteo, extracting relevant weather parameters
        and converting them into a list of WeatherModel instances.

        Args:
            raw_data (dict): The raw JSON data received from the Open Meteo API.
            location_id (int): The ID of the location associated with the weather data.

        Returns:
            list[WeatherModel]: A list of WeatherModel instances representing the processed weather data.
            Returns None if the data cannot be processed or is missing required fields.
        """
        weather_data = []

        try:
            latitude = raw_data['latitude']
            longitude = raw_data['longitude']
        except KeyError as e:
            self.logger.error(f'Failed to extract latitude and longitude from weather data: {e}')
            return None
        except Exception as e:
            self.logger.error(f'An unexpected error occurred: {e}')
            return None

        for i in range(len(raw_data['hourly']['time'])):
            try:
                date_string = raw_data['hourly']['time'][i]
                date_obj = datetime.strptime(date_string, self.OPEN_METEO_DATE_FORMAT)
                cloud_cover = raw_data['hourly']['cloud_cover'][i]
                temperature = raw_data['hourly']['temperature'][i]
                sunshine_duration = raw_data['hourly']['sunshine_duration'][i]
                weather = WeatherModel(date_obj, cloud_cover, temperature, latitude, longitude, sunshine_duration, location_id=location_id)
                weather_data.append(weather)
            except KeyError as e:
                self.logger.error(f'KeyError: Missing key {e} in raw_data[hourly] at index {i}')
                return None
            except ValueError as e:
                self.logger.error(f'ValueError: {e} in raw_data[hourly] at index {i}')
                return None
            except Exception as e:
                self.logger.error(f'An unexpected error occurred: {e} in raw_data[hourly] at index {i}')
                return None

        return weather_data
