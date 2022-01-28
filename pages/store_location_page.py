import time
from pages.base_page import BasePage
from pages.cart import Cart
from utils.read_config import ReadConfig
from utils.logger import Logger

locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class StoreLocation(BasePage):
    element = None
    product = None
    displayed_name = None
    displayed_quantity = None
    zip_code = None
    distance = None
    locations = []

    def __init__(self, driver, product=None):
        self.driver = driver
        self.products = product
        self.refresh()

    def refresh(self):
        self.displayed_name = self.visible_clickable_new("Store_Location_Page", "product name", max_wait_time//15)
        self.displayed_quantity = self.visible_clickable_new("Store_Location_Page", "quantity", max_wait_time//15)

    def search_for_location(self, zip_code, distance):
        self.input_text("Store_Location_Page", "zip code", zip_code, 2, max_wait_time//15)
        self.select_from_dropdown("Store_Location_Page", "distance", distance, max_wait_time//15)
        time.sleep(max_wait_time//15)
        self.click_on_element("Store_Location_Page", "search button", max_wait_time//20)
        time.sleep(max_wait_time//15)
        locations_elements = self.find_all_elements("Store_Location_Page", 'store found', max_wait_time//15)
        if locations_elements and len(locations_elements) > 0:
            for elm in locations_elements:
                self.locations.append(elm.text)

    def select_first_location(self):
        if len(self.locations) > 0:
            self.click_on_element("Store_Location_Page", "select button", max_wait_time//15)
            time.sleep(max_wait_time//6)

    def view_cart(self):
        self.click_on_element("Store_Location_Page", "view cart", max_wait_time//15)
        time.sleep(max_wait_time//10)
        return Cart(self.driver, self.product)
