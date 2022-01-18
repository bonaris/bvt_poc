class CreditCard:
    def __init__(self, find_by_list, values):
        self.find_by_list = find_by_list
        self.cc_data = values
        self.card_number = None
        self.expiry_date = None
        self.cvv = None
        self.card_number_find_by = None
        self.expiry_date_find_by = None
        self.cvv_code_find_by = None
        self.mapped_keys_find_by = None
        self.mapped_keys = None
        self.map_keys()
        self.map_form_data()

    def map_keys(self):
        self.card_number = self.cc_data.get("num")
        self.expiry_date = self.cc_data.get("expiry")
        self.cvv = self.cc_data.get("cvv")

        self.card_number_find_by = self.find_by_list.get("card_number")
        self.expiry_date_find_by = self.find_by_list.get("expiry_date")
        self.cvv_code_find_by = self.find_by_list.get("cvs")

    def mapp_form_data(self):
        self.mapped_keys = [(self.card_number_find_by, self.card_number),
                            (self.last_name_find_by, self.last_name),
                            (self.expiry_date_find_by, self.expiry_date),
                            (self.cvv_code_find_by, self.cvv)]
