import time
from utils.read_config import ReadConfig
from utils.logger import Logger
from pages.base_page import BasePage
from data_types.user import User

locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class SignInPage(BasePage):

    user = None

    def __init__(self, driver):
        self.driver = driver

    def login(self, user_record):
        self.user = User(user_record)
        self.__login()

    def login_credentials(self, email, password):
        self.user = User()
        self.user.email = email
        self.user.password = password
        self.__login()

    def __login(self):
        self.input_text('Sign In', 'email', self.user.email, 0, 2)
        self.input_text('Sign In', 'password', self.user.password, 0, 2)
        self.click_on_element('Sign In', 'sign in button', 2)

    def new_user(self, user_record):
        pass

