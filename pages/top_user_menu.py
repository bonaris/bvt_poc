from pages.base_page import BasePage
from utils.logger import Logger


class TopUserMenu(BasePage):

    def __init__(self, driver):
        self.driver = driver

    def click_on_cart(self):
        Logger.log_info("TOP USER MENU CART CLICK")
        self.click_on_element("Menu", "user_cart", 3)

    def click_on_sign_in(self):
        Logger.log_info("TOP USER MENU SIGN IN CLICK")
        self.click_on_element("Menu", "user_sign_in", 3)

    def click_on_my_account(self):
        Logger.log_info("TOP USER MENU MY ACCOUNT CLICK")
        self.click_on_element("Menu", "user_my_account", 3)
