import time

import utils.excel_data_utils as locators
from utils.read_config import ReadConfig
from utils.logger import Logger
from validators.base_validator import BaseValidator
from utils.utils import Utils
from data_types.product import Product
from pages.base_page import BasePage
from pages.pdp import PdpPage


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
        self.initial_products_in_grid = ReadConfig.get_value_by_keys("test-info", "initial_products_in_grid")
        self.expected_header = locators.find_test_data(locators_file, "PLP_Page", "header").get("expected")
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

    def update_product_list(self):
        self.product_list = []
        try:
            quick_view_elements = self.get_quick_look_elements()
            self.product_grid_elements = self.find_all_elements("PLP_Page", "productList", 3)
            i = 0
            for product_element in self.product_grid_elements:
                product = Product()
                product.map_from_plp_element(product_element)
                product.quick_look_element = quick_view_elements[i]
                self.product_list.append(product)
                i += 1
        except Exception:
            Logger.log_warning("PLP Page: could not read header")
        return self.product_grid_elements

    def get_filters(self):
        try:
            self.filter_label = self.visible_clickable_new("PLP_Page", "filterLabel", 3)
            total_elements = self.find_all_elements("PLP_Page", "filters", 3)
            self.filter_list = []
            self.filter_list_elements = []
            for el in total_elements:
                if len(el.text) > 0:
                    self.filter_list.append(el.text)
                    self.filter_list_elements.append(el)
        except Exception:
            Logger.log_error("Could not find any filters on PLP Page")

    def select_color_filter(self, color):
        try:
            Logger.log_info(f'selecting color filter: {color}')
            self.filter_list_elements[0].click()
            self.click_on_element("PLP_Page", color, 5)
        except Exception:
            Logger.log_warning(f"could not select {color}")

    def select_price_filter(self, price_range):
        try:
            Logger.log_info(f'selecting price filter: {price_range}')
            self.filter_list_elements[1].click()
            self.click_on_element("PLP_Page", price_range, 5)
        except Exception:
            Logger.log_warning(f"could not select {price_range}")

    def refresh(self):
        self.get_header_text()
        self.update_product_list()
        self.get_filters()
        self.get_breadcrumbs_links()

    def get_current_filter(self):
        current_filter_elements = []
        try:
            all_elements = self.find_all_elements("PLP_Page", "current filter", 4)
            for element in all_elements:
                if len(element.text) > 0:
                    current_filter_elements.append(element)
        except Exception as e:
            Logger.log_warning(f"could not find current filters.")
        return current_filter_elements

    def click_on_random_product(self):
        product_selected = Utils.get_random_list_element(self.product_list)
        self.click_on_element_obj(product_selected.element)
        return PdpPage(driver=self.driver, product=product_selected)

    def find_and_click_on_available_product(self, attempts=3, gift_wrapping=False):
        pdp_page = None
        attempts_counter = 1
        for product in self.product_list:
            product.element.click()
            time.sleep(max_wait_time//4)
            pdp_page = PdpPage(driver=self.driver, product=product)
            if "In Stock" in pdp_page.product.availability:
                break
            elif "Delivered in" in pdp_page.product.availability:
                break
            else:
                pdp_page = None
                self.driver.back()
            if attempts_counter <= attempts:
                attempts_counter += 1
            else:
                break
        return pdp_page

    def get_quick_look_elements(self):
        quick_look_elements = []
        all_elements = self.find_all_elements("PLP_Page", "quick look elements", 3)
        for element in all_elements:
            if element.text == 'Quick Look':
                quick_look_elements.append(element)
        return quick_look_elements

    def click_on_quick_look(self, product):
        self.click_on_element_obj(element=product.quick_look_element)
        ql_modal = PdpPage(driver=self.driver, product=product)
        return ql_modal
