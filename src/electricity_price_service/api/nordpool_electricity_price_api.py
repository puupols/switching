from src.electricity_price_service.api.base_electricity_price_api import BaseElectricityPriceAPI
import requests

class NordpoolElectricityPriceAPI(BaseElectricityPriceAPI):

    def get_electricity_price(self):
        nordpool_url = self.configuration.get('nordpool_url')
        resp = requests.get(nordpool_url)
        return resp.json()
