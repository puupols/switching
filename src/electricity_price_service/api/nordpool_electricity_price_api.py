from src.electricity_price_service.api.base_electricity_price_api import BaseElectricityPriceAPI
import requests


class NordpoolElectricityPriceAPI(BaseElectricityPriceAPI):
    NORDPOOL_URL_CONFIG_NAME = 'nordpool_url'

    def get_electricity_price(self):
        nordpool_url = self.configuration.get(self.NORDPOOL_URL_CONFIG_NAME)
        resp = requests.get(nordpool_url)
        return resp.json()
