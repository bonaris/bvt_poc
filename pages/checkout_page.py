import time
from pages.base_page import BasePage
from pages.payment_method import PaymentMethod
from data_types.address import Address
from data_types.order import Order
from utils.logger import Logger
from utils.read_config import ReadConfig
from pytest_html_reporter import attach

locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class CheckoutPage(BasePage):

    payment = None
    cart_items = []
    order = None

    def __init__(self, driver, cart_items=None):
        self.driver = driver
        self.payment = PaymentMethod(driver)
        self.refresh()
        if cart_items:
            self.cart_items = cart_items

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

    def pay_with_pay_pal(self, user):
        try:
            self.payment.pay_with_paypal(user)
            time.sleep(max_wait_time)
            self.switch_to_frame("Checkout_Page", "order iframe", max_wait_time//6)
            self.order = Order()
            self.order.number = self.visible_clickable_new("Checkout_Page", "order number", wait=max_wait_time//15).text
            billing_address = Address()
            shipping_address = Address()
            pickup_address = Address()
            address_elements = self.find_all_elements("Checkout_Page", "billing address", wait=max_wait_time//15)
            if address_elements > 0:
                billing_address.map_checkout_billing_address(address_elements[0].text)
                self.order.billing_address = billing_address
            if address_elements > 1:
                shipping_address.map_order_address(address_elements[1].text)
                self.order.shipping_address = shipping_address
            if address_elements > 2:
                pickup_address.map_order_address(address_elements[2].text)
                self.order.pickup_address = pickup_address

        except Exception:
            attach(self.driver.get_screenshot_as_png())
            Logger.log_error("PAYPAL PAY: Order is not displayed.")

