import time

from pages.base_page import BasePage
from data_types.address import Address
from utils.read_config import ReadConfig


locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class CheckoutPage(BasePage):

    def __init__(self, driver):
        self.driver = driver
        self.refresh()

    def checkout_as_guest(self, email):
        self.switch_to_checkout_frame()
        self.input_text("Checkout_Page", "guest email", email, 50, max_wait_time//2)
        self.click_on_element("Checkout_Page", "guest checkout button")
        time.sleep(max_wait_time//8)
        self.driver.switch_to.default_content()

    def enter_shipping_address(self, address):
        all_elements = self.find_all_elements("Checkout_Page", "address_locators")
        shipping_address = Address()
        shipping_address.map_test_data(address)
        form_elements = []
        for i in range(6, 13):
            form_elements.append(all_elements[i])
        form_values = address.get_form_values()
        self.fill_form(form_elements, form_values)
        self.click_on_element("Checkout_Page", "shipping submit button")
        time.sleep(max_wait_time//10)

    def switch_to_checkout_frame(self):
        self.switch_to_frame("Checkout_Page", "checkout iframe", max_wait_time//6)

    def refresh(self):
        pass

