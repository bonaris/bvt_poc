import time
from utils.read_config import ReadConfig
from pages.base_page import BasePage
from data_types.user import User
from data_types.address import Address
from data_types.order import Order
from utils.logger import Logger

locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class AccountPage(BasePage):

    account_info = None
    shipping_address_list = []
    order_list = []

    def __init__(self, driver):
        self.driver = driver
        self.account_info = User()
        self.refresh()

    def refresh(self):
        self.refresh_account_info()
        self.refresh_shipping_address()
        self.refresh_orders()

    def refresh_account_info(self):
        account_info_elements = self.find_all_elements('My_Account_Page', 'account info')
        self.account_info.map_from_my_account(account_info_elements)

    def refresh_shipping_address(self):
        shipping_address_header_elements = self.find_all_elements('My_Account_Page', 'address headers', 5)
        map_account_shipping_address = self.find_all_elements('My_Account_Page', 'address info container', 5)
        self.shipping_address_list = []
        try:
            for i in range(len(shipping_address_header_elements)):
                address = Address()
                address.map_account_shipping_address(map_account_shipping_address[i].text)
                address.address_header = shipping_address_header_elements[i].text
                self.shipping_address_list.append(address)
        except Exception:
            Logger.log_warning("ACCOUNT SHIPPING ADDRESS COULD NOT MAP  *******************")

    def refresh_orders(self):
        orders_records = self.visible_clickable_new('My_Account_Page', 'order table', 3).text.split('\n')
        self.order_list = []
        for i in range(3, len(orders_records) - 3):
            order = Order()
            order.map_my_account_page(orders_records[i])
            self.order_list.append(order)

    def update_account_info(self, new_account_info):
        Logger.log_info(" ACCOUNT INFO UPDATE ************************")
        self.fill_form(self.account_info.elements_list, new_account_info.get_form_values())
        self.click_on_element("My_Account_Page", "update account button")
        time.sleep(max_wait_time//6)

    def get_account_updated_msg(self):
        msg = None
        try:
            msg = self.visible_clickable_new('My_Account_Page', 'account saved text', 3).text
        except Exception:
            pass
        return msg
