import time
from utils.utils import Utils
from pages.base_page import BasePage
from data_types.address import Address


class CartItem(BasePage):
    product_info = None
    quantity = None
    subtotal = None
    sale_subtotal = None
    product = []

    quantity_element = None
    update_element = None
    delete_element = None
    store_pick_up = False
    store_address = None

    def __init__(self, driver, product_info, quantity_element, update_element, delete_element):
        self.driver = driver
        self.product_info = product_info
        self.quantity = quantity_element.get_attribute('value')
        self.quantity_element = quantity_element
        self.update_element = update_element
        self.delete_element = delete_element

    def subtotal_to_number(self):
        return Utils.price_to_number(self.subtotal)

    def sale_subtotal_to_number(self):
        return Utils.price_to_number(self.sale_subtotal)

    def to_string(self):
        data_dictionary = {
            "product": self.product.to_string(),
            "quantity": self.product.quantity,
            "subtotal": str(self.subtotal),
            "sale_subtotal": str(self.sale_subtotal)
        }
        return data_dictionary

    def update_quantity(self, quantity):
        self.input_text_element(self.quantity_element, quantity, 2)
        self.click_on_element_obj(self.update_element)
        self.product.quantity = quantity
        time.sleep(3)

    def delete_item(self):
        self.click_on_element_obj(self.update_element)
        time.sleep(3)

    def map_store_address(self, element):
        self.store_address = Address()
        values = element.text.split('\n')
        self.store_address.line_one = values[6].replace('\\', "")
        self.store_address.city = values[7].split(",")[0]
        self.store_address.state = values[7].split(",")[1].strip()
        self.store_address.zip = values[7].split(",")[2].strip()
        self.store_address.phone = values[8].split(":")[1].strip()
