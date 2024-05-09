class ElectricityPriceModel:
    """
    A model class to represent electricity price data at a specific datetime.

    Attributes:
        datetime (datetime): The specific date and time the price data applies to.
        price (float): The cost of electricity per unit at the specified datetime.

    Methods:
        None: This model class is primarily used for storing and accessing electricity price data.
    """

    def __init__(self, datetime, price):
        """
        Initializes a new instance of ElectricityPriceModel with the provided datetime and price.

        Args:
            datetime (datetime): The specific date and time the price data applies to.
            price (float): The cost of electricity per unit at the specified datetime.
        """
        self.datetime = datetime
        self.price = price
