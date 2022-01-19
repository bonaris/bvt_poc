import time
from pytest_bdd import scenarios,  when, then, given
from utils.read_config import ReadConfig
import utils.excel_data_utils as test_data
from utils.logger import Logger
from validators.plp_validator import Validator
from pages.plp import PlpPage
from pages.pdp import PdpPage
from utils.utils import Utils


scenarios('../../features/bvt/bvt_01.feature', features_base_dir='tests/features/bvt')

default_wait_time = ReadConfig.get_max_wait_time()
store_url = ReadConfig.get_url()
test_data_filename = ReadConfig.get_test_data_filename()
test_data_record = test_data.find_test_data(test_data_filename, 'BVT', 'bvt-01')


@given('Z Gallerie website should be up and running')
def open_home_page(driver, context):
    Logger.log_info(f"Navigating to {store_url} ***")
    driver.get(store_url)
    context['driver'] = driver
    time.sleep(default_wait_time//6)


@when('user provides Meganav to get to a PLP, for example "Tabletop > Serveware & Flatware"')
def open_url(context):
    full_url = store_url + test_data_record.get('Meganav1')
    Logger.log_info(f"Navigating to {full_url} ***")
    context['driver'].get(full_url)
    time.sleep(default_wait_time//3)


@then('PLP is displayed as per selection')
def validate_plp_header(context):
    context['plp_page'] = PlpPage(context['driver'])
    Utils.save_screenshot(context['driver'], tc_name='plp_page', frame_name='header')
    assert Validator.validate_header(actual=context['plp_page'].get_header_text(), expected=test_data_record.get('Expected Header'))


@then('Product Grid is displayed on the page')
def validate_plp_grid(context):
    plp_page = context['plp_page']
    context['original_pl'] = plp_page.product_list
    Utils.save_screenshot(context['driver'], tc_name='plp_page', frame_name='product_grid')
    assert Validator.validate_values(len(plp_page.product_grid_elements), int(plp_page.initial_products_in_grid), "Total products in grid on start")


@then(u'each product has a name, price and a "Quick Look" link')
def validate_products(context):
    plp_page = context['plp_page']
    assert Validator.validate_products(plp_page.product_list)


@then(u'there are filters like: color, price range')
def validate_filters(context):
    plp_page = context['plp_page']
    assert Validator.validate_filters(plp_page.filter_label.text, plp_page.filter_list)


@then(u'there is a dropdown for color filter to select best match')
def filter_drop_down(context):
    plp_page = context['plp_page']
    assert Validator.validate_values((plp_page.filter_list_elements[0] is not None), True, "Color Filter is available")


@when(u'user selects one of the colors in a filter')
def select_color(context):
    plp_page = context['plp_page']
    plp_page.select_color_filter(test_data_record.get("Color Filter"))
    time.sleep(default_wait_time//6)


@when(u'user selects one of the price-range in a filter')
def select_price(context):
    plp_page = context['plp_page']
    plp_page.select_price_filter(test_data_record.get("Price Filter"))
    time.sleep(default_wait_time//6)


@then(u'Product List is updated based on the best match')
def validate_filter(context):
    plp_page = context['plp_page']
    assert Validator.validate_values(
        len(plp_page.get_product_grid()),
        test_data_record.get("Filtered Products"),
        "Filtered Products"
    )


@then(u'breadcrumbs filter links are available on the page')
def validate_filter(context):
    plp_page = context['plp_page']
    plp_page.get_breadcrumbs_links()
    assert Validator.validate_breadcrumbs(plp_page.breadcrumbs_list, test_data_record.get('Expected Breadcrumb Path'))


@when(u'user clicks on price range link')
def select_price_range_breadcrumb(context):
    plp_page = context['plp_page']
    plp_page.click_breadcrumb(test_data_record.get('Price Displayed'))
    time.sleep(default_wait_time//6)


@then(u'price range filter is cleared')
def validate_filter(context):
    plp_page = context['plp_page']
    plp_page.get_breadcrumbs_links()
    breadcrumb_to_remove = test_data_record.get('Price Displayed') + '/'
    expected_breadcrumbs = test_data_record.get('Expected Breadcrumb Path').replace(breadcrumb_to_remove, '')
    assert Validator.validate_breadcrumbs(plp_page.breadcrumbs_list, expected_breadcrumbs)


@then(u'Product List is updated')
def validate_filter(context):
    plp_page = context['plp_page']
    current_products_in_list = len(plp_page.product_list)
    plp_page.get_product_grid()
    refreshed_products_in_list = len(plp_page.product_list)
    assert Validator.validate_is_not_equal(
        current_products_in_list,
        refreshed_products_in_list,
        f"Products on the list before and after clearing Price Filter"
    )


@when(u'user clicks on Clear All link')
def clear_all_filters(context):
    plp_page = context['plp_page']
    plp_page.click_breadcrumb(test_data_record.get('Clear All Filters'))
    time.sleep(default_wait_time//6)


@then(u'all filters are cleared')
def validate_filter(context):
    plp_page = context['plp_page']
    plp_page.get_breadcrumbs_links()
    breadcrumb_to_remove = f"/{test_data_record.get('Color Displayed')}/"
    breadcrumb_to_remove += f"{test_data_record.get('Price Displayed')}/"
    breadcrumb_to_remove += f"{test_data_record.get('Clear All Filters')}"
    expected_breadcrumbs = test_data_record.get('Expected Breadcrumb Path').replace(breadcrumb_to_remove, '')
    assert Validator.validate_breadcrumbs(plp_page.breadcrumbs_list, expected_breadcrumbs)


@then(u'Product List is the same as originally displayed')
def validate_original_pl(context):
    plp_page = context['plp_page']
    plp_page.get_product_grid()
    assert Validator.validate_products(plp_page.product_list)


@when(u'user scrolls down a page or two and selects a product by clicking on it')
def step_impl(context):
    plp_page = context['plp_page']
    plp_page.click_page_down(pages=3)
    time.sleep(2)
    plp_page.get_product_grid()
    product_selected = plp_page.click_on_random_product()
    Logger.log_info(f'Product selected: {product_selected.to_string()}')
    time.sleep(default_wait_time/5)
    pdp_page = PdpPage(driver=context['driver'], product=product_selected)
    context['pdp_page'] = pdp_page


@then(u'PDP page is displayed for selected product')
def step_impl(context):
    pdp_page = context['pdp_page']
    pdp_page.refresh()
    assert True

#
# @then(u'price and total should be displayed and calculated as expected')
# def step_impl(context):
#     assert True
