import time
from utils.read_config import ReadConfig
from utils.logger import Logger
from data_types.product import Product
from pages.base_page import BasePage
from pages.cart import Cart

locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class PdpPage(BasePage):

    product = None
    add_to_cart_button = None
    description_button = None
    find_in_store_button = None
    item_selection_button = None

    def __init__(self, driver, product=Product()):
        self.driver = driver
        self.product = product
        self.refresh()

    def refresh(self):
        try:
            self.add_to_cart_button = self.visible_clickable_new("PDP_Page", "add to cart button", 1)
            self.description_button = self.visible_clickable_new("PDP_Page", "description button", 1)
            self.find_in_store_button = self.visible_clickable_new("PDP_Page", "find in store button", 1)
            self.item_selection_button = self.visible_clickable_new("PDP_Page", "item selection button", 1)
        except Exception:
            Logger.log_warning(" PDP PAGE: COULD NOT LOAD CONTROLS   ****************************")
        self.refresh_product()

    def refresh_product(self):
        try:
            product_info_elements = self.find_all_elements("PDP_Page", "product_info", 1)
            if product_info_elements is not None:
                self.product.map_from_pdp_element(product_info_elements)
                extra_info_elements = self.find_all_elements("PDP_Page", "additional info click", 1)
                extra_info_elements[2].click()
                time.sleep(1)
                extra_info_elements[4].click()
                time.sleep(1)
                extra_info_content = self.find_all_elements("PDP_Page", "additional info content", 1)
                self.product.description = extra_info_content[0].text
                self.product.details_dimensions = extra_info_content[1].text
                self.product.other_info = extra_info_content[2].text
            else:
                self.product.sku = self.visible_clickable_new("PDP_Page", "sku", 1).text
            self.product.original_price = self.visible_clickable_new("PDP_Page", "original price", 1).text
            try:
                self.product.sale_price = self.visible_clickable_new("PDP_Page", "sale price", 1).text
            except Exception:
                pass
            # ToDo: Add star rating and reviews here star rating class already in
            #  locators in PDP_Page tab, key = 'star rating'
        except Exception:
            Logger.log_warning("PDP Page: Could not update Product info. ")

    def input_quantity(self, quantity):
        self.input_text(
            tab_name="PDP_Page",
            key="quantity",
            text=str(quantity),
            field_length=2,
            wait=max_wait_time//10
        )

    def add_to_cart(self):
        self.click_page_up()
        if self.add_to_cart_button is None:
            self.add_to_cart_button = self.visible_clickable_new("PDP_Page", "add to cart button")
        self.click_on_element(self.add_to_cart_button)
        time.sleep(max_wait_time//5)
        cart = Cart(driver=self.driver, product=self.product)
        return cart
