import utils.excel_data_utils as locators
from utils.read_config import ReadConfig
from utils.logger import Logger
from validators.base_validator import BaseValidator
from utils.utils import Utils
from data_types.product import Product
from pages.base_page import BasePage


locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class Cart(BasePage):
    product = None

    def __init__(self, driver, product=Product()):
        self.driver = driver
        self.product = product
#        self.switch_to_frame("Cart_Page", "cart preview dropdown")
        self.refresh()

    def update_quantity(self, quantity):
        self.product.quantity = quantity
        self.input_text(
            tab_name="Cart_Page",
            key="quantity input",
            text=str(quantity),
            field_length=3,
            wait=3
        )

    def refresh(self):
        return None
