class Address:
    def __init__(self, find_by_list=None, values=None):
        if values:
            self.values = values
            self.first_name = None
            self.last_name = None
            self.address_one = None
            self.city = None
            self.state = None
            self.zip = None
            self.phone = None
        if find_by_list:
            self.find_by_list = find_by_list
            self.first_name_xpath = None
            self.last_name_xpath = None
            self.address_one_xpath = None
            self.city_xpath = None
            self.state_xpath = None
            self.zip_xpath = None
            self.phone_xpath = None
            self.mapped_keys_xpath = None
            self.mapped_keys = None
        self.map_keys()
        self.map_form_data()

    def map_keys(self):
        if self.values:
            self.first_name = self.values.get("first_name")
            self.last_name = self.values.get("last_name")
            self.address_one = self.values.get("address_one")
            self.city = self.values.get("city")
            self.state = self.values.get("state")
            self.zip = self.values.get("zip")
            self.phone = self.values.get("phone")

        if self.find_by_list:
            self.first_name_xpath = self.find_by_list.get("first_name")
            self.last_name_xpath = self.find_by_list.get("last_name")
            self.address_one_xpath = self.find_by_list.get("address_one")
            self.city_xpath = self.find_by_list.get("city")
            self.state_xpath = self.find_by_list.get("state")
            self.zip_xpath = self.find_by_list.get("zip")
            self.phone_xpath = self.find_by_list.get("phone")

    def map_form_data(self):
        if self.values and self.find_by_list:
            self.mapped_keys = [(self.first_name_xpath, self.first_name),
                       (self.last_name_xpath, self.last_name),
                       (self.address_one_xpath, self.address_one),
                       (self.city_xpath, self.city),
                       (self.state_xpath, self.state),
                       (self.zip_xpath, self.zip),
                       (self.phone_xpath, self.phone)]

