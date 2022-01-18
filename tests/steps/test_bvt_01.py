import time
from pytest_bdd import scenarios,  when, then, given
from utils.read_config import ReadConfig
import utils.excel_data_utils as test_data
from utils.logger import Logger
from validators.plp_validator import Validator
from pages.plp import PlpPage
from utils.utils import Utils


scenarios('../features', features_base_dir='tests/features')

default_wait_time = ReadConfig.get_max_wait_time()
store_url = ReadConfig.get_url()
test_data_filename = ReadConfig.get_test_data_filename()


@given('Z Gallerie website should be up and running')
def open_home_page(driver, context):
    Logger.log_info(f"Navigating to {store_url} ***")
    driver.get(store_url)
    context['driver'] = driver


@when('user provides Meganav to get to a PLP, for example "Tabletop > Serveware & Flatware"')
def open_url(context):
    meganav_path = test_data.find_test_data(filename=test_data_filename, tab_name="Meganav", search_key="Tabletop > Serveware & Flatware").get("Path")
    full_url = store_url + meganav_path
    Logger.log_info(f"Navigating to {full_url} ***")
    context['driver'].get(full_url)
    time.sleep(default_wait_time//20)


@then('PLP is displayed as per selection')
def validate_plp_header(context):
    context['plp_page'] = PlpPage(context['driver'])
    Utils.save_screenshot(context['driver'], tc_name='plp_page', frame_name='header')
    Validator.validate_header(actual=context['plp_page'].get_header_text(), expected=context['plp_page'].expected_header)


@then('Product Grid is displayed on the page')
def validate_plp_grid(context):
    plp_page = context['plp_page']
    Utils.save_screenshot(context['driver'], tc_name='plp_page', frame_name='product_grid')
    Validator.validate_values(len(plp_page.product_grid_elements), int(plp_page.initial_products_in_grid), "Total products in grid on start")


@then(u'each product has a name, price and a "Quick Look" link')
def validate_products(context):
    plp_page = context['plp_page']
    Validator.validate_products(plp_page.product_list)


@then(u'there are filters like: color, price range')
def validate_filters(context):
    plp_page = context['plp_page']
    Validator.validate_filters(plp_page.filter_label.text, plp_page.filter_list)


@then(u'there is a dropdown for color filter to select best match')
def filter_drop_down(context):
    plp_page = context['plp_page']
    Validator.validate_values((plp_page.filter_list_elements[0] is not None), True, "Color Filter is available")
    return plp_page


@when(u'user selects one of the colors in a filter')
def select_color(context):
    plp_page = context['plp_page']
    plp_page.select_color_filter(plp_page.filter_colors.get("Black"))


@then(u'Product List is updated based on the best match')
def validate_drop(context):
    assert True
#
# @when(u'user scrolls down a page or two and selects a product by clicking on it')
# def step_impl(context):
#    plp_page.select_color_filter(PlpPage.filter_colors.get("Black"))
#     context.a - context.b
#
#
# @when(u'expected SKU of the product is known')
# def step_impl(context):
#     context.a - context.b
#
#
# @then(u'an overlay should be displayed confirming the qty of product(s) added to cart')
# def step_impl(context):
#     assert True
#
#
# @then(u'price and total should be displayed and calculated as expected')
# def step_impl(context):
#     assert True
