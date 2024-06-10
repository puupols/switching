from src.repository_service.base_repository_service import BaseRepositoryService
from src.weather_service.models.weather_model import WeatherModel
from sqlalchemy.exc import IntegrityError


class WeatherRepositoryService(BaseRepositoryService):
    """
    Service class responsible for managing database operations for weather data.
    """

    def store_weather_data(self, weather_data):
        """
        Stores a list of weather data records into the database.
        Handles integrity errors by updating existing records.

        Args:
            weather_data (list): List of WeatherModel objects to be stored in the database.
        """
        with (self.session_maker() as session):
            for weather in weather_data:
                try:
                    session.add(weather)
                    session.commit()
                except IntegrityError as e:
                    session.rollback()
                    self._update_weather_data(session, weather)
                except Exception as e:
                    session.rollback()
                    self.logger.error(f"Error storing weather data into database. Error - {e}")

    def _update_weather_data(self, session, weather):
        """
        Updates existing weather data in the database.

        Args:
            session (sqlalchemy.orm.session.Session): SQLAlchemy session for database operations.
            weather (WeatherModel): WeatherModel object containing updated weather data.
        """
        existing_weather = session.query(WeatherModel).filter(
            WeatherModel.datetime == weather.datetime,
            WeatherModel.latitude == weather.latitude,
            WeatherModel.longitude == weather.longitude
        ).first()
        if existing_weather:
            existing_weather.temperature = weather.temperature
            existing_weather.cloud_cover = weather.cloud_cover
            existing_weather.sunshine_duration = weather.sunshine_duration
            session.commit()

    def get_weather_data_after_date(self, date):
        """
        Retrieves weather data records from the database that are after the specified date.

        Args:
            date (datetime): The date after which the weather data records are to be retrieved.

        Returns:
            list: List of WeatherModel objects retrieved from the database.
        """
        with self.session_maker() as session:
            return session.query(WeatherModel).filter(WeatherModel.datetime > date).all()
