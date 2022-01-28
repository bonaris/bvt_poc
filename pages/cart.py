import time
from utils.read_config import ReadConfig
from data_types.product import Product
from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage
from data_types.cart_item import CartItem
import utils.excel_data_utils as test_data
from utils.logger import Logger

locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()
test_data_filename = ReadConfig.get_test_data_filename()


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
        if not self.visible_clickable_new("Store_Location_Page", "view cart", max_wait_time//15):
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
        try:
            products_elements = self.find_all_elements("Cart_Page", "drop down products", max_wait_time//15)
            quantity_elements = self.find_all_elements("Cart_Page", "quantity input", max_wait_time//15)
            update_elements = self.find_all_elements("Cart_Page", "update buttons", max_wait_time//15)
            delete_elements = self.find_all_elements("Cart_Page", "delete buttons", max_wait_time//15)
            item_subtotals = self.find_all_elements("Cart_Page", "item subtotals", max_wait_time//15)
            main_cart = False

            if self.visible_clickable_new("Cart_Page", "checkout button top", max_wait_time//15):
                subtotal_index = 0
                main_cart = True
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
                if main_cart:
                    product.map_from_main_cart(products_elements[i])
                else:
                    product.map_from_drop_down_cart(products_elements[i])
                cart_item = CartItem(
                    driver=self.driver,
                    product_info=product.name,
                    quantity_element=quantity_elements[i],
                    update_element=update_elements[i],
                    delete_element=delete_elements[i]
                )
                try:
                    store_pick_up_msg = test_data.find_test_data(test_data_filename, "Constants", "STORE PICK UP MESSAGE")
                    if store_pick_up_msg.get('value') in products_elements[i].text:
                        cart_item.map_store_address(products_elements[i])
                except Exception:
                    pass
                cart_item.product = product
                subtotals = item_subtotals[subtotal_index].text.split('\n')
                cart_item.subtotal = subtotals[0]
                if len(subtotals) > 1:
                    cart_item.sale_subtotal = subtotals[1]

                self.cart_items.append(cart_item)
                subtotal_index += step
        except Exception:
            pass

    def view_cart(self):
        self.click_on_element("Cart_Page", "view cart button", max_wait_time//15)
        time.sleep(max_wait_time//6)

    def apply_promo_code(self, promo_code):
        self.click_on_element("Cart_Page", "open promo code", max_wait_time//15)
        self.input_text("Cart_Page", "promo code input", promo_code, 30, max_wait_time//15)
        self.click_on_element("Cart_Page", "apply promo button", max_wait_time//15)
        time.sleep(1)
        #Check for Error Pop Up. In case one is up - log an error and click on Ok
        if self.visible_clickable_new("Cart_Page", "apply promo error modal", max_wait_time//15):
            Logger.log_warning(f"CART PAGE: Could not apply promo code {promo_code}")
            self.click_on_element("Cart_Page", "promo error ok button", max_wait_time//15)

    def click_on_checkout(self, top_button=True):
        if top_button:
            self.click_on_element("Cart_Page", "checkout button top")
        else:
            self.click_on_element("Cart_Page", "checkout button bottom")
        time.sleep(max_wait_time//3)
        return CheckoutPage(self.driver)

