import time
from utils.read_config import ReadConfig
from utils.logger import Logger
from pages.base_page import BasePage
from data_types.credit_card import CreditCard
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class PaymentMethod(BasePage):

    cart_items = []

    def __init__(self, driver):
        self.driver = driver
        self.refresh()

    def refresh(self):
        self.refresh_cart_items()

    def refresh_cart_items(self):
        pass

    def pay_with_credit_card(self, cc_info):
        all_elements = self.find_all_elements("Checkout_Page", "address_locators", 3)
        cc_form_elements = [
            all_elements[5],
            all_elements[6],
            all_elements[7]
        ]

    def pay_with_paypal(self, user):
#        self.switch_v2_co_iframe()
        radio_buttons = self.find_all_elements("Payment_Method", "payment type radio buttons", max_wait_time//15)
        self.click_on_element_obj(radio_buttons[1])
        time.sleep(1)
        pay_pall_buttons = self.find_all_elements("Payment_Method", "checkout with paypal buttons", max_wait_time//15)
        self.click_on_element_obj(pay_pall_buttons[0])
        time.sleep(max_wait_time//2)
        try:
            WebDriverWait(self.driver, max_wait_time).until(EC.number_of_windows_to_be(2))
        except Exception as e:
            Logger.log_error("Expected paypal signin modal not shown")
            raise Exception("Expected paypal signin modal not shown")
        switchback_window = self.driver.window_handles[0]
        self.driver.switch_to_window(self.driver.window_handles[1])
        time.sleep(1)
        self.input_text("Payment_Method", "paypal email input", user.email, 30, max_wait_time//15)
        self.click_on_element("Payment_Method", "paypal next button", max_wait_time//2)
        time.sleep(max_wait_time//8)
        self.input_text("Payment_Method", "paypal password", user.password, 20, max_wait_time//15)
        self.click_on_element("Payment_Method", "paypal login button", max_wait_time//2)
        time.sleep(max_wait_time//8)
        self.click_page_down(2)
        self.click_on_element("Payment_Method", "paypal pay now button", max_wait_time//2)
        time.sleep(max_wait_time//2)
        self.driver.switch_to_window(switchback_window)
        time.sleep(1)

