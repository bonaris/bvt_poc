class Address:
    test_data_record = None
    first_name = None
    last_name = None
    line_one = None
    line_two = None
    city = None
    state = None
    zip = None
    phone = None
    company_name = None
    full_state = None

    address_header = None

    first_name_element = None
    last_name_element = None
    address_one_element = None
    city_element = None
    state_element = None
    zip_element = None
    phone_element = None

    element_list = []

    def __init__(self, elements=None, test_data_record=None):
        if elements is not None:
            self.map_form_data()
        elif test_data_record is not None:
            self.test_data_record = test_data_record
            self.map_test_data(test_data_record)

    def map_test_data(self, test_data_record):
        self.first_name = test_data_record.get("first_name")
        self.last_name = test_data_record.get("last_name")
        self.line_one = test_data_record.get("line_1")
        self.line_two = test_data_record.get("line_2")
        self.city = test_data_record.get("city")
        self.state = test_data_record.get("state")
        self.full_state = test_data_record.get("full_state")
        self.zip = test_data_record.get("zip")
        self.phone = test_data_record.get("phone")

    def map_form_data(self):
        pass

    def map_account_shipping_address(self, address_string):
        fields = address_string.split('\n')
        self.first_name = fields[0].split(' ')[0]
        self.last_name = fields[0].split(' ')[1]
        if len(fields[0].split(' ')) > 2:
            self.last_name = ' ' + fields[0].split(' ')[2]
        self.line_one = fields[1]
        self.city = fields[2].split(' ')[0]
        self.state = fields[2].split(' ')[1]
        self.zip = fields[2].split(' ')[2]
        self.phone = fields[3]

    def map_checkout_billing_address(self, address_string):
        fields = address_string.split('\n')
        self.first_name = fields[0].split(' ')[0]
        self.last_name = fields[0].split(' ')[1]
        if len(fields[0].split(' ')) > 2:
            self.last_name = ' ' + fields[0].split(' ')[2]
        self.line_one = fields[1]
        self.city = fields[2].split(',')[0]
        self.state = fields[2].split(',')[1]
        self.zip = fields[2].split(',')[2]


    def get_form_values(self):
        return [
            self.first_name,
            self.last_name,
            self.company_name,
            self.line_one,
            self.line_two,
            self.city,
            self.state,
            self.zip,
            self.phone
        ]

    def get_shipping_details_form_values(self):
        return [
            self.first_name,
            self.last_name,
            self.line_one,
            self.line_two,
            self.city,
            self.state,
            self.zip,
            self.phone
        ]


    def to_string(self):
        data_dictionary = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "line_one": self.line_one,
            "line_two": self.line_two,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "phone": self.phone
        }
        return str(data_dictionary)
