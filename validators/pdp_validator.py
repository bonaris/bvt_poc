import utils.excel_data_utils as locators
from utils.read_config import ReadConfig
from utils.logger import Logger
from validators.base_validator import BaseValidator
from pytest_html_reporter import attach


locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class PdpValidator(BaseValidator):

    @staticmethod
    def validate_product_original_values(pdp_product, plp_product, driver=None):
        result = True
        if not BaseValidator.validate_values(pdp_product.name, plp_product.name, "Product Name"):
            result = False
        if not BaseValidator.validate_values(pdp_product.original_price, plp_product.original_price, "Original Price"):
            result = False
        if plp_product.sale_price is not None:
            if not BaseValidator.validate_values(pdp_product.sale_price, plp_product.sale_price, "Sale Price"):
               result = False
        return result

    @staticmethod
    def validate_filters(label, filters, driver=None):
        result = True
        expected_filter_label = locators.find_test_data(locators_file, "PLP_Page", "filterLabel").get("expected")
        if not BaseValidator.validate_values(actual=label, expected=expected_filter_label, field_name="Filter Label"):
            result = False
        if not BaseValidator.validate_values(actual=filters[0], expected='Color', field_name="Filter by Color"):
            result = False
        if not BaseValidator.validate_values(actual=filters[1], expected='Price Range', field_name="Filter by Price Range"):
            result = False
        if driver and not result:
            attach(data=driver.get_screenshot_as_png())
        return result

    @staticmethod
    def validate_breadcrumbs(actual_list, expected, separator='/', driver=None):
        result = True
        expected_list = expected.split(separator)

        if BaseValidator.validate_values(len(actual_list), len(expected_list), "Total breadcrumbs items"):
            if not BaseValidator.validate_values(str(actual_list), str(expected_list), "Breadcrumbs items"):
                result = False
        else:
            if driver:
                attach(data=driver.get_screenshot_as_png())
            result = False
        return result
