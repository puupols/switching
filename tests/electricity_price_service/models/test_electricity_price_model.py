from src.electricity_price_service.models.electricity_price_model import ElectricityPriceModel
import datetime
import unittest

class TestElectricityPriceModel(unittest.TestCase):

    def test_initialisation(self):

        # Setup
        date = datetime.datetime.now()
        price = 81.3

        # Action
        model = ElectricityPriceModel(date, price)

        # Assert
        self.assertEqual(model.datetime, date)
        self.assertEqual(model.price, price)
