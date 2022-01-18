import utils.excel_data_utils as locators
from utils.read_config import ReadConfig
from utils.logger import Logger
from validators.base_validator import BaseValidator
from utils.utils import Utils
from data_types.product import Product
from pages.base_page import BasePage


locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class PlpPage(BasePage):

    expected_header = None
    header_text = None
    product_grid_elements = None
    product_list = []
    filter_list_elements = []
    filter_list = []
    filter_label = None
    filter_colors = {'Black': 'select Black', 'Gold': 'select Gold', 'Pink': 'select Pink', 'Grey': 'select Grey', 'White': 'select White'}

    def __init__(self, driver):
        self.driver = driver
        self.refresh()

    def get_header_text(self):
        self.header_text = ""
        try:
            self.header_text = self.visible_clickable_new("PLP_Page", "header", 5).text
        except Exception:
            Logger.log_warning("PLP Page: could not read header")
        return self.header_text

    def is_header(self):
        header_locator_info = locators.find_test_data(locators_file, "PLP_Page", "header")
        return BaseValidator.is_visible(
            driver=self.driver,
            locator=header_locator_info.get("locator"),
            by=header_locator_info.get("By"),
            wait=max_wait_time
        )

    def get_product_grid(self):
        self.product_list = []
        try:
            self.product_grid_elements = self.find_all_elements("PLP_Page", "productList", 5)
            for product_element in self.product_grid_elements:
                product = Product()
                product.map_from_plp_element(product_element)
                self.product_list.append(product)
        except Exception:
            Logger.log_warning("PLP Page: could not read header")
        return self.product_grid_elements

    def get_filters(self):
        self.filter_label = self.visible_clickable_new("PLP_Page", "filterLabel", 5)
        total_elements = self.find_all_elements("PLP_Page", "filters")
        self.filter_list = []
        self.filter_list_elements = []
        for el in total_elements:
            if len(el.text) > 0:
                self.filter_list.append(el.text)
                self.filter_list_elements.append(el)

    def select_color_filter(self, color):
        try:
            Logger.log_info(f'selecting color filter: {color}')
            self.filter_list_elements[0].click()
            self.click_on_element("PLP_Page", color, 3)
        except Exception:
            Logger.log_warning(f"could not select {color}")

    def refresh(self):
        self.initial_products_in_grid = ReadConfig.get_value_by_keys("test-info", "initial_products_in_grid")
        self.expected_header = locators.find_test_data(locators_file, "PLP_Page", "header").get("expected")
        self.get_header_text()
        self.get_product_grid()
        self.get_filters()
