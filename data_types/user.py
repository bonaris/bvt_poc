from utils.read_config import ReadConfig
import utils.excel_data_utils as test_data


test_data_filename = ReadConfig.get_test_data_filename()


class User:

    first_name = None
    last_name = None
    email = None
    password = None
    rep_password = None
    phone = None
    user_record = None

    first_name_element = None
    last_name_element = None
    email_element = None
    password_element = None
    rep_password_element = None
    phone_element = None
    user_record_element = None

    def __init__(self, user_key, tab_name='Users'):
        self.user_record = test_data.find_test_data(test_data_filename, tab_name, user_key)
        self.first_name = self.user_record.get('first name')
        self.last_name = self.user_record.get('last name')
        self.email = self.user_record.get('email')
        self.password = self.user_record.get('password')
        self.rep_password = self.user_record.get('re password')
        self.phone = self.user_record.get('phone')

    def to_string(self):
        data_dictionary = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "rep_password": self.rep_password,
            "phone": self.phone
        }
        return str(data_dictionary)


