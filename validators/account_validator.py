from utils.read_config import ReadConfig
from utils.logger import Logger
from validators.base_validator import BaseValidator
from utils.utils import Utils


locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class AccountValidator(BaseValidator):

    @staticmethod
    def validate_account_info(actual, expected):
        result = True
        return result

    @staticmethod
    def validate_drop_down_cart_displayed(cart_page):
        result = True
        if cart_page.is_element_present("Cart_Page", "drop down cart") is None:
            result = False
        return result
