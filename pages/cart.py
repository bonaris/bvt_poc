from utils.read_config import ReadConfig
from data_types.product import Product
from pages.base_page import BasePage

locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class Cart(BasePage):
    displayed_products = []
    added_products = []
    products_elements = []
    cart_total = 0.0

    def __init__(self, driver, product=Product()):
        self.driver = driver
        #        self.switch_to_frame("Cart_Page", "cart preview dropdown")
        self.added_products.append(product)
        self.refresh()

    def update_quantity(self, quantity):
        self.product.quantity = quantity
        self.input_text(
            tab_name="Cart_Page",
            key="quantity input",
            text=str(quantity),
            field_length=3,
            wait=3
        )

    def refresh(self):
        self.get_products_info()

    def get_products_info(self):
        self.products_elements = self.find_all_elements("Cart_Page", "drop down products")
        self.cart_total = 0.0
        for element in self.products_elements:
            product = Product()
            product.map_from_drop_down_cart(element)
            product.element = element
            self.cart_total += float(product.cart_total.replace('$', ''))
            self.displayed_products.append(product)
