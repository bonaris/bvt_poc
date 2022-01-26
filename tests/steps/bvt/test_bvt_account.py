import time
import utils.excel_data_utils as test_data
from pytest_bdd import scenarios,  when, then, given
from utils.read_config import ReadConfig
from utils.logger import Logger
from pages.home_page import HomePage
from validators.account_validator import AccountValidator
from utils.utils import Utils


scenarios('../../features/bvt/bvt_account.feature', features_base_dir='tests/features/bvt')

default_wait_time = ReadConfig.get_max_wait_time()
store_url = ReadConfig.get_url()
test_data_filename = ReadConfig.get_test_data_filename()
test_data_record = test_data.find_test_data(test_data_filename, 'User', 'e2e-15')


@given('Z Gallerie website should be up and running')
def open_home_page(driver, context):
    Logger.log_info(f"Navigating to {store_url} ***")
    driver.get(store_url)
    context['driver'] = driver


@when('user clicks on Sign In at a Top User Menu and signs in with valid credentials')
def sign_in(context):
    context['home_page'] = HomePage(context['driver'])
    sign_in_page = context['home_page'].top_user_menu_sign_in()
    sign_in_page.login(user_record=test_data_record)
    context['account_page'] = context['home_page'].top_user_menu_my_account()


@then('My Account Page is displayed')
def validate_account_page(context):
    assert context['account_page'] is not None
    assert context['account_page'].account_info is not None


@when('user updates Account information')
def account_info_update(context):
    current_info = context['account_page'].account_info
    current_info.password = test_data_record.get('password')
    context['account_page'].update_account_info(current_info)
    context['account_page'].refresh()


@then('information is updated successfully')
def validate_account_update(context):
    expected_message = test_data.find_test_data(test_data_filename, 'Constants', 'ACCOUNT SAVED').get('value')
    actual_message = context['account_page'].get_account_updated_msg()
    assert AccountValidator.validate_values(
        actual=actual_message,
        expected=expected_message,
        field_name="Account updated messages"
    )

