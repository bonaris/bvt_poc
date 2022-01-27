import time
from utils.read_config import ReadConfig
from data_types.product import Product
from pages.base_page import BasePage
from data_types.cart_item import CartItem
from utils.utils import Utils

locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class Cart(BasePage):
    displayed_products = []
    added_products = []
    products_elements = []
    cart_items = []
    cart_total = None
    cart_total_savings = None

    def __init__(self, driver, product=None):
        self.driver = driver
        #        self.switch_to_frame("Cart_Page", "cart preview dropdown")
        if product:
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
        products_elements = self.find_all_elements("Cart_Page", "drop down products", max_wait_time//15)
        quantity_elements = self.find_all_elements("Cart_Page", "quantity input", max_wait_time//15)
        update_elements = self.find_all_elements("Cart_Page", "update buttons", max_wait_time//15)
        delete_elements = self.find_all_elements("Cart_Page", "delete buttons", max_wait_time//15)
        item_subtotals = self.find_all_elements("Cart_Page", "item subtotals", max_wait_time//15)

        if self.visible_clickable_new("Cart_Page", "checkout button top", max_wait_time//15):
            subtotal_index = 0
            step = 1
        else:
            subtotal_index = 1
            step = 2

        self.cart_total = self.visible_clickable_new("Cart_Page", "cart total", 1).text

        try:
            self.cart_total_savings = self.visible_clickable_new("Cart_Page", "cart total savings", 1)
        except Exception:
            pass

        self.cart_items = []
        for i in range(len(products_elements)):
            product = Product()
            product.map_from_drop_down_cart(products_elements[i])
            cart_item = CartItem(
                driver=self.driver,
                product_name=product.name,
                quantity_element=quantity_elements[i],
                update_element=update_elements[i],
                delete_element=delete_elements[i]
            )
            subtotals = item_subtotals[subtotal_index].text.split('\n')
            cart_item.subtotal = subtotals[0]
            if len(subtotals) > 1:
                cart_item.sale_subtotal = subtotals[1]

            self.cart_items.append(cart_item)
            subtotal_index += step

    def view_cart(self):
        self.click_on_element("Cart_Page", "view cart button", max_wait_time//15)
        time.sleep(max_wait_time//6)
