import utils.excel_data_utils as locators
from utils.read_config import ReadConfig
from utils.logger import Logger
from validators.base_validator import BaseValidator
from utils.utils import Utils


locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class Validator(BaseValidator):

    @staticmethod
    def validate_header(actual, expected):
        result = True
        if not BaseValidator.validate_values(actual, expected, field_name="PLP Header Text"):
            result = False
        return result

    @staticmethod
    def validate_products(product_list):
        result = True

        if not BaseValidator.validate_not_empty(product_list, 'Products on the list'):
            Logger.log_validation_error('Products on the list')
            result = False
        else:
            for product in product_list:
                if not BaseValidator.validate_not_empty(product.name, "Product Name"):
                    result = False
                if not BaseValidator.validate_not_empty(product.original_price, "Product Original Price"):
                    result = False
                if not BaseValidator.validate_not_empty(product.quick_look, "Quick View Link"):
                    result = False
        return result

    @staticmethod
    def validate_filters(label, filters):
        result = True
        expected_filter_label = locators.find_test_data(locators_file, "PLP_Page", "filterLabel").get("expected")
        if not BaseValidator.validate_values(actual=label, expected=expected_filter_label, field_name="Filter Label"):
            result = False
        if not BaseValidator.validate_values(actual=filters[0], expected='Color', field_name="Filter by Color"):
            result = False
        if not BaseValidator.validate_values(actual=filters[1], expected='Price Range', field_name="Filter by Price Range"):
            result = False
        return result
