from src.electricity_price_service.processors.base_electricity_price_processor import BaseElectricityPriceProcessor
from datetime import datetime, timedelta
from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel


class NordpoolElectricityPriceProcessor(BaseElectricityPriceProcessor):
    """
    A concrete processor class that implements BaseElectricityPriceProcessor for handling
    electricity price data from the Nordpool market.

    Attributes:
        NORDPOOL_DATE_FORMAT (str): The datetime format used to parse the date strings from Nordpool data.

    Methods:
        process_data: Implements the data processing to parse Nordpool specific raw data into a list of ElectricityPriceModel instances.
    """
    NORDPOOL_DATE_FORMAT = '%d-%m-%YT%H'

    def process_data(self, raw_data):
        """
         Processes raw electricity price data from the Nordpool market into structured ElectricityPriceModel instances.

         Iterates over each hour's data provided in the raw_data, extracts, and converts the date and price
         information into ElectricityPriceModel instances.

         Args:
             raw_data (dict): The raw data fetched from Nordpool containing date and price information in a specific structure.

         Returns:
             list[ElectricityPriceModel]: A list of ElectricityPriceModel instances representing hourly electricity prices.
         """
        electricity_prices = []
        for i in range(24):
            try:
                raw_time = raw_data['data']['Rows'][i]['Name']
                raw_date = raw_data['data']['Rows'][i]['Columns'][0]['Name']
                price = float(raw_data['data']['Rows'][i]['Columns'][0]['Value'].replace(',', '.'))
                price_date_string = raw_date + 'T' + raw_time[:2:]
                price_date = datetime.strptime(price_date_string, self.NORDPOOL_DATE_FORMAT)
                price_date_lv_timezone = price_date + timedelta(hours=1)
                electricity_price = ElectricityPriceModel(price_date_lv_timezone, price)
                electricity_prices.append(electricity_price)
            except (KeyError, ValueError, IndexError) as e:
                self.logger.error(f'Failed to process Nordpool electricity price data: {e}')
            except Exception as e:
                self.logger.error(f'An unexpected error occurred while processing Nordpool data: {e}')
        return electricity_prices
