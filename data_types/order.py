from utils.utils import Utils
from utils.logger import Logger


class Order:

    number = None
    date = None
    status = None
    shipping_status = None
    total = None
    billing_address = None
    shipping_address = None
    pickup_address = None

    def __init__(self):
        self.number = None

    def total_to_number(self):
        return Utils.price_to_number(self.total)

    def to_string(self):
        data_dictionary = {
            "number": self.number,
            "date": self.date,
            "status": self.status,
            "shipping_status": self.shipping_status,
            "total": self.total
        }
        return data_dictionary

    def map_my_account_page(self, order_string):
        values = order_string.split(' ')
        try:
            self.number = values[0]
            self.date = f'{values[1]} {values[2]} {values[3]} {values[4]}'
            next_index = 6
            if len(values) == 8:
                self.status = values[5]
            elif len(values) == 9:
                self.status = f'{values[5]} {values[6]}'
                next_index = 7
            self.shipping_status = values[next_index]
            self.total = values[next_index + 1]
        except Exception:
            Logger.log_warning(f"MY ACCOUNT ORDER RECORD COULD NOT BE PARSED: {order_string}")
