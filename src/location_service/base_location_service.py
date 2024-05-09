from abc import ABC, abstractmethod


class BaseLocationService(ABC):
    """
    Abstract base class defining the interface for a location service.

    This class provides a framework for location services that return geographic locations,
    intended to be extended by concrete implementations that provide specific location retrieval methods.

    Methods:
        get_location: Abstract method that should be implemented to return the geographic location.
    """
    def __init__(self):
        pass

    @abstractmethod
    def get_location(self):
        """
        Abstract method to get the geographic location.

        This method must be implemented by subclasses to return the current geographic location.

        Returns:
            The geographic location, typically as a (latitude, longitude) tuple.
        """
        pass
