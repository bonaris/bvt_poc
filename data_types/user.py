from utils.read_config import ReadConfig
import utils.excel_data_utils as test_data
from utils.utils import Utils
from random import randint


test_data_filename = ReadConfig.get_test_data_filename()
RANDOM_KEY = test_data.find_test_data(test_data_filename, 'Constants', 'RANDOM KEY')
FIRST_NAME_LIST = test_data.find_test_data(test_data_filename, 'Constants', 'FIRST NAMES')
LAST_NAME_LIST = test_data.find_test_data(test_data_filename, 'Constants', 'LAST NAMES')
EMAIL_SUFFIX = test_data.find_test_data(test_data_filename, 'Constants', 'EMAIL SUFFIX')


class User:

    first_name = None
    last_name = None
    email = None
    password = None
    new_password = None
    rep_password = None
    phone = None
    user_record = None

    first_name_element = None
    last_name_element = None
    email_element = None
    password_element = None
    new_password_element = None
    rep_password_element = None
    phone_element = None
    user_record_element = None
    elements_list = []

    def __init__(self, user_record=None):
        if user_record is not None:
            self.map_from_test_record(user_record)

    def map_from_test_record(self, user_record):
        if user_record.get('first name') is RANDOM_KEY:
            self.first_name = Utils.get_random_list_element(FIRST_NAME_LIST)
        else:
            self.first_name = user_record.get('first name')
        if user_record.get('last name') is RANDOM_KEY:
            self.last_name = Utils.get_random_list_element(LAST_NAME_LIST)
        else:
            self.last_name = user_record.get('last name')
        if user_record.get('email') is RANDOM_KEY:
            random_index = randint(0, 1000)
            self.email = f'{self.first_name}_{str(random_index)}@{EMAIL_SUFFIX}'
        else:
            self.email = user_record.get('email')
        if user_record.get('password') is RANDOM_KEY:
            self.password = Utils.get_random_string(10)
        else:
            self.password = user_record.get('password')
        if user_record.get('re password') is RANDOM_KEY:
            self.rep_password = Utils.get_random_string(10)
        else:
            self.rep_password = user_record.get('re password')
        if user_record.get('phone') is RANDOM_KEY:
            self.phone = Utils.get_random_numeric_string(10)
        else:
            self.phone = user_record.get('phone')

    def map_from_my_account(self, elements_list):
        if len(elements_list) > 7:
            self.first_name_element = elements_list[0]
            self.first_name = self.first_name_element.get_attribute("value")
            self.elements_list.append(elements_list[0])
            self.last_name_element = elements_list[1]
            self.last_name = self.last_name_element.get_attribute("value")
            self.elements_list.append(elements_list[1])
            self.email_element = elements_list[2]
            self.email = self.email_element.get_attribute("value")
            self.elements_list.append(elements_list[2])
            self.phone_element = elements_list[3]
            self.phone = self.phone_element.get_attribute("value")
            self.elements_list.append(elements_list[3])
            self.password_element = elements_list[4]
            self.elements_list.append(elements_list[4])
            self.new_password_element = elements_list[5]
            self.elements_list.append(elements_list[5])
            self.rep_password_element = elements_list[6]
            self.elements_list.append(elements_list[6])

    def to_string(self):
        data_dictionary = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "new_password": self.new_password,
            "rep_password": self.rep_password,
            "phone": self.phone
        }
        return str(data_dictionary)

    def get_form_values(self):
        values_list = [
            self.first_name,
            self.last_name,
            self.email,
            self.phone,
            self.password,
            self.new_password,
            self.rep_password
        ]
        return values_list
