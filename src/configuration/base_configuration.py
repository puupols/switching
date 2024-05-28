from abc import ABC, abstractmethod


class BaseConfiguration(ABC):
    """
    Abstract base class for configuration handlers.

    Defines the interface for configuration handling that any subclass should implement.
    """
    @abstractmethod
    def get(self, key, default=None):
        """
        Abstract method to retrieve a configuration value by key.

        Implementing classes must provide functionality to access configuration data using a key.

        Args:
            key (str): The key for the configuration value to retrieve.

        Returns:
            The value associated with the given key. The return type can vary depending on the implementation.
        """
        pass

    @abstractmethod
    def get_as_list(self, key, default=None):
        pass
