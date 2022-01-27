import time
from utils.utils import Utils
from pages.base_page import BasePage


class CartItem(BasePage):
    product_name = None
    quantity = None
    subtotal = None
    sale_subtotal = None

    quantity_element = None
    update_element = None
    delete_element = None

    def __init__(self, driver, product_name, quantity_element, update_element, delete_element):
        self.driver = driver
        self.product_name = product_name
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
            "quantity": self.quantity,
            "subtotal": str(self.subtotal),
            "sale_subtotal": str(self.sale_subtotal)
        }
        return data_dictionary

    def update_quantity(self, quantity):
        self.input_text_element(self.quantity_element, quantity, 2)
        self.click_on_element_obj(self.update_element)
        time.sleep(3)

    def delete_item(self):
        self.click_on_element_obj(self.update_element)
        time.sleep(3)
