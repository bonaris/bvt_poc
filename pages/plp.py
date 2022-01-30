import time
import utils.excel_data_utils as locators
from utils.read_config import ReadConfig
from utils.logger import Logger
from validators.base_validator import BaseValidator
from utils.utils import Utils
from data_types.product import Product
from pages.base_page import BasePage
from pages.pdp import PdpPage
from random import randint


locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()
test_data_filename = ReadConfig.get_test_data_filename()


class PlpPage(BasePage):

    expected_header = None
    header_text = None
    product_grid_elements = None
    product_list = []
    filter_list_elements = []
    filter_list = []
    filter_label = None

    def __init__(self, driver):
        self.driver = driver
        self.initial_products_in_grid = ReadConfig.get_value_by_keys("test-info", "initial_products_in_grid")
        self.expected_header = locators.find_test_data(locators_file, "PLP_Page", "header").get("expected")
        self.refresh()

    def get_header_text(self):
        self.header_text = ""
        try:
            self.header_text = self.visible_clickable_new("PLP_Page", "header", 2).text
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

    def refresh_product_list(self):
        self.product_list = []
        try:
            quick_view_elements = self.get_quick_look_elements()
            self.product_grid_elements = self.find_all_elements("PLP_Page", "productList", 2)
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
            self.filter_label = self.visible_clickable_new("PLP_Page", "filterLabel", 2)
            total_elements = self.find_all_elements("PLP_Page", "filters", 2)
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
        self.refresh_product_list()
        self.get_filters()
        self.get_breadcrumbs_links()

    def get_current_filter(self):
        current_filter_elements = []
        try:
            all_elements = self.find_all_elements("PLP_Page", "current filter", 2)
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

    def select_available_product(self, sale=None, attempts=3, gift_wrapping=False):
        attempts_counter = 1
        selected_product = None
        filtered_product_list = []

        for product in self.product_list:
            if sale is None:
                filtered_product_list.append(product)
            elif sale is True and product.sale_price is not None:
                filtered_product_list.append(product)
            elif sale is False and product.sale_price is None:
                filtered_product_list.append(product)

        for i in range(attempts):
            index = randint(0, len(filtered_product_list) - 1)
            product = filtered_product_list[index]
            self.click_on_quick_look(product=product)
            time.sleep(max_wait_time//20)
            product_info = self.visible_clickable_new("PDP_Page", "ql product info").text
            out_of_stock = locators.find_test_data(test_data_filename, "Constants", "OUT OF STOCK").get('value')
            if out_of_stock not in product_info:
                selected_product = product
                self.click_on_element("PLP_Page", "ql close button", 1)
                break
            else:
                self.click_on_element("PLP_Page", "ql close button", 1)
            if attempts_counter <= attempts:
                attempts_counter += 1
            else:
                break
        time.sleep(max_wait_time//max_wait_time)
        return selected_product

    def select_bopis_item(self, sale=None, attempts=12):
        attempts_counter = 1
        selected_product = None
        filtered_product_list = []

        for product in self.product_list:
            if sale is None:
                filtered_product_list.append(product)
            elif sale is True and product.sale_price is not None:
                filtered_product_list.append(product)
            elif sale is False and product.sale_price is None:
                filtered_product_list.append(product)

        for i in range(attempts):
            index = randint(0, len(filtered_product_list) - 1)
            product = filtered_product_list[index]
            self.click_on_quick_look(product=product)
            time.sleep(max_wait_time//20)
            if self.visible_clickable_new("PDP_Page", "find in store button", 1):
                selected_product = product
                self.click_on_element("PLP_Page", "ql close button", 1)
                break
            else:
                self.click_on_element("PLP_Page", "ql close button", 1)
            if attempts_counter <= attempts:
                attempts_counter += 1
            else:
                break
        time.sleep(max_wait_time//max_wait_time)
        return selected_product

    def get_quick_look_elements(self):
        quick_look_elements = []
        all_elements = self.find_all_elements("PLP_Page", "quick look elements", 1)
        for element in all_elements:
            if element.text == 'Quick Look':
                quick_look_elements.append(element)
        return quick_look_elements

    def click_on_quick_look(self, product):
        self.click_on_element_obj(element=product.quick_look_element)
        time.sleep(2)
        ql_modal = PdpPage(driver=self.driver, product=product)
        return ql_modal

    def sort_products(self, sort_by):
        self.select_from_dropdown('PLP_Page', 'sort', sort_by, 3)
        time.sleep(max_wait_time//6)
