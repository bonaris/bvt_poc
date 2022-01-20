import time

import utils.excel_data_utils as locators
from utils.read_config import ReadConfig
from utils.logger import Logger
from validators.base_validator import BaseValidator
from utils.utils import Utils
from data_types.product import Product
from pages.base_page import BasePage


locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class PdpPage(BasePage):

    product = None

    def __init__(self, driver, product=Product()):
        self.driver = driver
        self.product = product
        self.refresh()

    def refresh(self):
        self.update_product()

    def update_product(self):
        try:
            product_info_elements = self.find_all_elements("PDP_Page", "product_info", 3)
            self.product.map_from_pdp_element(product_info_elements)
            extra_info_elements = self.find_all_elements("PDP_Page", "additional info click", 3)
            extra_info_elements[2].click()
            time.sleep(1)
            extra_info_elements[4].click()
            time.sleep(1)
            extra_info_content = self.find_all_elements("PDP_Page", "additional info content", 3)
            self.product.description = extra_info_content[0].text
            self.product.details_dimensions = extra_info_content[1].text
            self.product.other_info = extra_info_content[2].text
            self.product.original_price = self.visible_clickable_new("PDP_Page", "original price", 3).text
            self.product.sale_price = self.visible_clickable_new("PDP_Page", "sale price", 3).text
            # ToDo: Add star rating and reviews here star rating class already in
            #  locators in PDP_Page tab, key = 'star rating'
        except Exception:
            Logger.log_warning("PDP Page: Could not update Product info. ")

    def input_quantity(self, quantity):
        self.input_text(
            tab_name="PDP_Page",
            key="quantity",
            text=str(quantity),
            field_length=1,
            wait=max_wait_time//10
        )
