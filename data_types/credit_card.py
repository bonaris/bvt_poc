class CreditCard:

    cc_data = None
    card_number = None
    expiry_date = None
    cvv = None
    driver = None

    def __init__(self, driver, test_data_record=None):
        self.driver = driver
        if test_data_record:
            self.map_test_data()

    def map_test_data(self):
        self.card_number = self.cc_data.get("num")
        self.expiry_date = self.cc_data.get("expiry")
        self.cvv = self.cc_data.get("cvv")
        #
        # self.card_number_find_by = self.find_by_list.get("card_number")
        # self.expiry_date_find_by = self.find_by_list.get("expiry_date")
        # self.cvv_code_find_by = self.find_by_list.get("cvs")

    # def mapp_form_data(self):
    #     self.mapped_keys = [(self.card_number_find_by, self.card_number),
    #                         (self.last_name_find_by, self.last_name),
    #                         (self.expiry_date_find_by, self.expiry_date),
    #                         (self.cvv_code_find_by, self.cvv)]
