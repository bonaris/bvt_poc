import time
from pages.base_page import BasePage
from pages.payment_method import PaymentMethod
from data_types.address import Address
from utils.read_config import ReadConfig


locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class CheckoutPage(BasePage):

    payment = None

    def __init__(self, driver):
        self.driver = driver
        self.payment = PaymentMethod(driver)
        self.refresh()

    def checkout_as_guest(self, email):
        self.switch_v2_co_iframe(wait=max_wait_time/15)
        time.sleep(1)
        self.input_text("Checkout_Page", "guest email", email, 50, max_wait_time//2)
        self.click_on_element("Checkout_Page", "guest checkout button")
        time.sleep(max_wait_time//5)

    def enter_shipping_address(self, address):
#        self.switch_v2_co_iframe()
        all_elements = self.find_all_elements("Checkout_Page", "address_locators", 3)
        shipping_address = Address()
        shipping_address.map_test_data(address)
        form_elements = []
        start_index = len(all_elements) - 8  # there are 8 last elements in the list that are for shipping address form
        end_index = len(all_elements)
        for i in range(start_index, end_index):
            form_elements.append(all_elements[i])
        form_values = shipping_address.get_shipping_details_form_values()
        self.fill_form(form_elements, form_values, 2)
        self.click_on_element("Checkout_Page", "shipping submit button", max_wait_time//15)
        time.sleep(max_wait_time//5)

    def switch_to_checkout_frame(self):
        self.switch_to_frame("Checkout_Page", "checkout iframe", max_wait_time//6)

    def refresh(self):
        pass

    def pay_with_pay_pal(self, paypal_data):
        self.payment.pay_with_paypal(paypal_data)
