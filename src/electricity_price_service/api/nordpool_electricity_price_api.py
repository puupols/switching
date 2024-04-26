from src.electricity_price_service.api.base_electricity_price_api import BaseElectricityPriceAPI
import requests

class NordpoolElectricityPriceAPI(BaseElectricityPriceAPI):

    def get_electricity_price(self):
        resp = requests.get('https://www.nordpoolgroup.com/api/marketdata/page/59')
        return resp.json()
