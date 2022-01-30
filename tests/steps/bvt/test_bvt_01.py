import time
from pytest_bdd import scenarios,  when, then, given
from utils.read_config import ReadConfig
import utils.excel_data_utils as test_data
from utils.logger import Logger
from validators.plp_validator import PlpValidator
from validators.pdp_validator import PdpValidator
from validators.cart_validator import CartValidator
from pages.plp import PlpPage
from pages.cart import Cart
from pages.home_page import HomePage
from utils.utils import Utils
from pages.top_user_menu import TopUserMenu
from pytest_html_reporter import attach

scenarios('../../features/bvt/bvt_01.feature', features_base_dir='tests/features/bvt/')


default_wait_time = ReadConfig.get_max_wait_time()
store_url = ReadConfig.get_url()
test_data_filename = ReadConfig.get_test_data_filename()
test_data_record = test_data.find_test_data(test_data_filename, 'BVT', 'bvt-01')


@given('Z Gallerie website should be up and running')
def open_home_page(driver, context):
    Logger.log_info(f"Navigating to {store_url} ***")
    context['driver'] = driver
    context["home_page"] = HomePage(driver.get(store_url))
    context["home_page"].check_for_newsletter_popup()


@when('user provides Meganav to get to a PLP, for example "Tabletop > Serveware & Flatware"')
def open_url(context):
    full_url = store_url + test_data_record.get('Meganav1')
    Logger.log_info(f"Navigating to {full_url} ***")
    context['driver'].get(full_url)
    time.sleep(default_wait_time//5)


@then('PLP is displayed as per selection with expected header')
def validate_plp_header(context):
    context['plp_page'] = PlpPage(context['driver'])
    expected_header = context["plp_page"].breadcrumbs_list[-1]
    Utils.save_screenshot(context['driver'], tc_name='plp_page', frame_name='header')
    assert PlpValidator.validate_header(actual=context['plp_page'].get_header_text(), expected=expected_header)


@then('Product Grid is displayed on the page')
def validate_plp_grid(context):
    Utils.save_screenshot(context['driver'], tc_name='plp_page', frame_name='product_grid')
    assert PlpValidator.validate_values(
        len(context['plp_page'].product_grid_elements),
        int(context['plp_page'].initial_products_in_grid),
        "Total products in grid on start")


@then(u'each product has a name, price and a "Quick Look" link')
def validate_products(context):
    assert PlpValidator.validate_products(context['plp_page'].product_list)


@then(u'there are filters like: color, price range')
def validate_filters(context):
    assert PlpValidator.validate_filters(context['plp_page'].filter_label.text, context['plp_page'].filter_list)


@then(u'there is a dropdown for color filter to select best match')
def filter_drop_down(context):
    assert PlpValidator.validate_values((context['plp_page'].filter_list_elements[0] is not None), True, "Color Filter is available")


@when(u'user selects one of the colors in a filter')
def select_color(context):
    context['plp_page'].select_color_filter(test_data_record.get("Color Filter"))
    time.sleep(default_wait_time//6)


@when(u'user selects one of the price-range in a filter')
def select_price(context):
    context['plp_page'].select_price_filter(test_data_record.get("Price Filter"))
    time.sleep(default_wait_time//6)


@then(u'Product List is updated based on the best match')
def validate_filter(context):
    assert PlpValidator.validate_values(
        len(context['plp_page'].refresh_product_list()),
        test_data_record.get("Filtered Products"),
        "Filtered Products"
    )


@then(u'breadcrumbs filter links are available on the page')
def validate_filter(context):
    context['plp_page'].get_breadcrumbs_links()
    assert PlpValidator.validate_breadcrumbs(context['plp_page'].breadcrumbs_list, test_data_record.get('Expected Breadcrumb Path'))


@when(u'user clicks on price range link')
def select_price_range_breadcrumb(context):
    context['plp_page'].click_breadcrumb(test_data_record.get('Price Displayed'))
    time.sleep(default_wait_time//6)


@then(u'price range filter is cleared')
def validate_filter(context):
    context['plp_page'].get_breadcrumbs_links()
    breadcrumb_to_remove = test_data_record.get('Price Displayed') + '/'
    expected_breadcrumbs = test_data_record.get('Expected Breadcrumb Path').replace(breadcrumb_to_remove, '')
    assert PlpValidator.validate_breadcrumbs(context['plp_page'].breadcrumbs_list, expected_breadcrumbs)


@then(u'Product List is updated')
def validate_filter(context):
    current_products_in_list = len(context['plp_page'].product_list)
    context['plp_page'].refresh_product_list()
    refreshed_products_in_list = len(context['plp_page'].product_list)
    assert PlpValidator.validate_is_not_equal(
        current_products_in_list,
        refreshed_products_in_list,
        f"Products on the list before and after clearing Price Filter"
    )


@when(u'user clicks on Clear All link')
def clear_all_filters(context):
    context['plp_page'].click_breadcrumb(test_data_record.get('Clear All Filters'))
    time.sleep(default_wait_time//6)


@then(u'all filters are cleared')
def validate_filter(context):
    context['plp_page'].get_breadcrumbs_links()
    breadcrumb_to_remove = f"/{test_data_record.get('Color Displayed')}/"
    breadcrumb_to_remove += f"{test_data_record.get('Price Displayed')}/"
    breadcrumb_to_remove += f"{test_data_record.get('Clear All Filters')}"
    expected_breadcrumbs = test_data_record.get('Expected Breadcrumb Path').replace(breadcrumb_to_remove, '')
    assert PlpValidator.validate_breadcrumbs(context['plp_page'].breadcrumbs_list, expected_breadcrumbs)


@then(u'Product List is the same as originally displayed')
def validate_original_pl(context):
    context['plp_page'].refresh_product_list()
    assert PlpValidator.validate_products(context['plp_page'].product_list)


@when(u'user scrolls down a page or two and selects a product by clicking on it')
def scroll_select(context):
    context['plp_page'].click_page_down(pages=3)
    time.sleep(2)
    time.sleep(default_wait_time/5)
    context['plp_page'].click_page_down(2)
#    context['pdp_page'] = context['plp_page'].find_and_click_on_available_product()
    context['pdp_page'] = context['plp_page'].click_on_random_product()
    Logger.log_info(f'Product selected: {context["pdp_page"].product.to_string()}')
    context["selected_products"] = {"first": context['pdp_page'].product}


@then(u'PDP page is displayed for selected product')
def validate_pdp_page(context):
    context['pdp_page'].get_breadcrumbs_links()
    #    expected_breadcrumbs = f"{test_data_record.get('Expected Meganav Breadcrumb')}/{context['pdp_page'].product.name}"
    assert context['pdp_page'] is not None


@then(u'And it is the same product as selected from PLP')
def validate_correct_product_selected(context):
    expected_product = context["selected_products"].get("first")
    assert PdpValidator.validate_product_original_values(pdp_product=context['pdp_page'].product, plp_product=expected_product)


@then(u'SKU of selected product is displayed')
def validate_correct_product_selected(context):
    PdpValidator.validate_not_empty(value=context['pdp_page'].product.sku, field_name="SKU is not empty")


@when(u'user clicks button Add to Cart')
def add_to_cart(context):
    context['cart_page'] = context['pdp_page'].add_to_cart()
    Logger.log_info(f"Product {context['pdp_page'].product.to_string()} added to the cart")
    context['cart_page'].input_text(
        tab_name='Cart_Page',
        key='quantity input',
        text='2',
        field_length=3,
        wait=3
    )


@then(u'drop down cart frame is displayed')
def validate_drop_down_cart_displayed(context):
    assert CartValidator.validate_drop_down_cart_displayed(context['cart_page'])


@then(u'price and total should be displayed and calculated as expected')
def validate_drop_down_cart(context):
    cart_page = context['cart_page']
    CartValidator.validate_drop_down_cart(cart_page)


@when('user provides Meganav to get to a PLP, for example "Home > Collections > $30 & Under"')
def open_url(context):
    full_url = store_url + test_data_record.get('Meganav2')
    Logger.log_info(f"Navigating to {full_url} ***")
    context['driver'].get(full_url)
    time.sleep(default_wait_time//6)


@when(u'user selects a product that is not on sale and clicks on Quick Look')
def click_quick_look(context):
    context['plp_page'].click_page_down(2)
    context['plp_page'].refresh_product_list()
    selected_product = context['plp_page'].select_bopis_item(sale=False)
    Logger.log_info(f"Quick Look for product {selected_product.to_string()}.")
    context['quick_look'] = context['plp_page'].click_on_quick_look(product=selected_product)


@then(u'Quick Look modal window is displayed')
def quick_look_opened(context):
    assert context['quick_look']


@when(u'user clicks on Find in Store button')
def click_find_in_store(context):
    context["store_location"] = context['quick_look'].find_in_store()


@then(u'Find In Store popup is displayed')
def validate_find_in_store(context):
    assert context['store_location']


@when(u'user searches for pick up store location')
def store_search(context):
    zip_code = test_data_record.get('zip_code')
    distance = test_data_record.get('distance')
    context["store_location"].search_for_location(zip_code=zip_code, distance=distance)


@then(u'list of available stores is displayed')
def validate_find_location(context):
    len(context['store_location'].locations) > 0


@when(u'user selects location and adds product to the cart')
def store_search(context):
    context["store_location"].select_first_location()


@when(u'selects to continue shopping')
def keep_shopping(context):
    context["store_location"].continue_shopping()


@when(u'user performs incomplete search for the keyword and sorts products')
def keep_shopping(context):
    context["plp_page"].search(test_data_record.get('search_keyword'))
    context['plp_page'].sort_products(test_data_record.get('sort_by'))
    context['plp_page'].refresh()


@then(u'PLP with results are displayed')
def search_result(context):
    assert context['plp_page']


@when(u'user opens shopping mini cart and updates quantity for one of the products')
def open_mini_cart(context):
    TopUserMenu(context['driver']).click_on_cart()
    context['cart_page'] = Cart(context['driver'])
    context['cart_page'].cart_items[0].update_quantity(2)
    context['cart_page'].view_cart()


@when(u'clicks on View Cart button')
def open_mini_cart(context):
    context['cart_page'].view_cart()


@when(u'applies promo code')
def promo_code(context):
    valid_promo_code = test_data.find_test_data(test_data_filename, "Constants", "PROMO CODE").get('value')
    context['cart_page'].apply_promo_code(valid_promo_code)
#    context['cart_page'].refresh()


@when(u'clicks on Checkout button and checks out as a guest')
def click_checkout(context):
    context['checkout_page'] = context['cart_page'].click_on_checkout()
    context['checkout_page'].checkout_as_guest('bvt_guest@zgallerie.com')


@when(u'user enters valid shipping address')
def shipping_address(context):
    address_data = test_data.find_test_data(test_data_filename, "Address", "billing")
    context['checkout_page'].enter_shipping_address(address_data)
    context['checkout_page'].pay_with_pay_pal("paypal_data")


@then(u'Checkout dialog is displayed')
def checkout_dialog(context):
    attach(context['driver'].get_screenshot_as_png())
    assert context['checkout_page']








@when(u'user provides Meganav to get to a PLP, for example "Tabletop > Serveware & Flatware" tmp')
def tmp(context):
    full_url = store_url + test_data_record.get('Meganav1')
    Logger.log_info(f"Navigating to {full_url} ***")
    context['driver'].get(full_url)
    time.sleep(default_wait_time//5)
    context['plp_page'] = PlpPage(context['driver'])
    selected_product = context['plp_page'].select_available_product()
    Logger.log_info(f"Quick Look for product {selected_product.to_string()}.")
    context['quick_look'] = context['plp_page'].click_on_quick_look(product=selected_product)
    context['quick_look'].add_to_cart()
    context["quick_look"].continue_shopping()
