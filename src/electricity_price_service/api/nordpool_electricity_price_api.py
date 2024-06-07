from src.electricity_price_service.api.base_electricity_price_api import BaseElectricityPriceAPI
from requests.exceptions import RequestException
import requests


class NordpoolElectricityPriceAPI(BaseElectricityPriceAPI):
    """
    Implementation of BaseElectricityPriceAPI for fetching electricity prices from the Nordpool market.

    Attributes:
        NORDPOOL_URL_CONFIG_NAME (str): Configuration key used to retrieve the Nordpool API URL from the configuration.

    Methods:
        get_electricity_price: Overrides the abstract method to fetch electricity prices using the Nordpool API.
    """
    NORDPOOL_URL_CONFIG_NAME = 'nordpool_url'

    def get_electricity_price(self):
        """
        Fetches the current electricity prices from the Nordpool market using the configured URL.

        Returns:
            dict: A JSON dictionary containing the latest electricity price data fetched from Nordpool.
            Returns None if the request fails or the response cannot be parsed.
        """
        try:
            nordpool_url = self.configuration.get(self.NORDPOOL_URL_CONFIG_NAME)
            self.logger.debug(f'Fetching electricity price from Nordpool: {nordpool_url}')
            resp = requests.get(nordpool_url)
        except RequestException as e:
            self.logger.error(f'Failed to fetch electricity price from Nordpool: {e}')
            return None
        except Exception as e:
            self.logger.error(f'Failed to fetch electricity price from Nordpool: {e}')
            return None
        try:
            electricity_price_data = resp.json()
        except ValueError as e:
            self.logger.error(f'Failed to parse JSON response from Nordpool: {e}')
            return None
        return electricity_price_data
