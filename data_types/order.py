from utils.utils import Utils


class Order:

    number = None
    date = None
    status = None
    shipping_status = None
    total = None

    def total_to_number(self):
        return Utils.price_to_number(self.total)

    def to_string(self):
        data_dictionary = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "rep_password": self.rep_password,
            "phone": self.phone
        }
        return data_dictionary

    def map_from_account_page(self, element):
        pass
