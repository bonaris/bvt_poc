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
        product_info_elements = self.find_all_elements("PDP_Page", "product_info", 3)
        quantity = self.visible_clickable_new("PDP_Page", "quantity", 3)
        self.product.map_from_pdp_element(product_info_elements, quantity)