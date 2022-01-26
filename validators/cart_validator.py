import utils.excel_data_utils as locators
from utils.read_config import ReadConfig
from utils.logger import Logger
from validators.base_validator import BaseValidator
from utils.utils import Utils


locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class CartValidator(BaseValidator):

    @staticmethod
    def validate_drop_down_cart(cart_page):
        result = True
        for i in range(len(cart_page.displayed_products)):
            if not BaseValidator.validate_values(
                            cart_page.displayed_products[i].name,
                            cart_page.added_products[i].name,
                            "Product Name"):
                result = False

            if not BaseValidator.validate_values(
                            Utils.price_to_number(cart_page.displayed_products[i].cart_total),
                            cart_page.added_products[i].get_expected_total(),
                            "Product Total"):
                result = False

        return result

    @staticmethod
    def validate_drop_down_cart_displayed(cart_page):
        result = True
        if cart_page.is_element_present("Cart_Page", "drop down cart") is None:
            result = False
        return result
