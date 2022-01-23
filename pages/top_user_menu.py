from pages.base_page import BasePage


class TopUserMenu(BasePage):

    def __init__(self, driver):
        self.driver = driver

    def click_on_cart(self):
        self.click_on_element("Menu", "user_cart", 3)

    def click_on_sign_in(self):
        self.click_on_element("Menu", "user_sign_in", 3)
