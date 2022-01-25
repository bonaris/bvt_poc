import time
from utils.read_config import ReadConfig
from data_types.product import Product
from pages.base_page import BasePage
from pages.sign_in_page import SignInPage
from pages.top_user_menu import TopUserMenu
from pages.account_page import AccountPage

locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class HomePage(BasePage):

    def __init__(self, driver):
        self.driver = driver

    def top_user_menu_sign_in(self):
        TopUserMenu(self.driver).click_on_sign_in()
        time.sleep(max_wait_time//6)
        return SignInPage(driver=self.driver)

    def top_user_menu_my_account(self):
        TopUserMenu(self.driver).click_on_my_account()
        time.sleep(max_wait_time//3)
        return AccountPage(driver=self.driver)
