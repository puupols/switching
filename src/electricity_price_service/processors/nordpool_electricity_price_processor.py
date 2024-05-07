from src.electricity_price_service.processors.base_electricity_price_processor import BaseElectricityPriceProcessor
from datetime import datetime
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel


class NordpoolElectricityPriceProcessor(BaseElectricityPriceProcessor):
    NORDPOOL_DATE_FORMAT = '%d-%m-%YT%H'

    def process_data(self, raw_data):
        electricity_prices = []
        for i in range(24):
            raw_time = raw_data['data']['Rows'][i]['Name']
            raw_date = raw_data['data']['Rows'][i]['Columns'][0]['Name']
            price = float(raw_data['data']['Rows'][i]['Columns'][0]['Value'].replace(',', '.'))
            price_date_string = raw_date + 'T' + raw_time[:2:]
            price_date = datetime.strptime(price_date_string, self.NORDPOOL_DATE_FORMAT)
            electricity_price = ElectricityPriceModel(price_date, price)
            electricity_prices.append(electricity_price)
        return electricity_prices
