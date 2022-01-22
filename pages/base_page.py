import time
import utils.excel_data_utils as locators
from utils.logger import Logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utils.read_config import ReadConfig
from selenium.common.exceptions import TimeoutException
from utils.utils import Utils

locators_file = ReadConfig.get_locators_filename()
max_wait_time = ReadConfig.get_max_wait_time()


class BasePage:

    driver = None
    breadcrumbs_list = []
    breadcrumbs_list_elements = {}


    def switch_v2_co_iframe(self, by='xpath', locator="//*[@id='checkoutV2']", wait=max_wait_time):
        try:
            WebDriverWait(self.driver, wait).until(EC.frame_to_be_available_and_switch_to_it((by, locator)))
        except Exception as e:
            Logger.log_error("failed to find path: " + locator + ", so trying switch to default_context")
            self.driver.switch_to.default_content()
            v2_iframes = self.driver.find_elements_by_xpath(locator)
            if len(v2_iframes) > 0:
                self.driver.switch_to.frame(v2_iframes[0])

    def visible_clickable(self, condition, wait=max_wait_time):
        elem = WebDriverWait(self.driver, wait).until(EC.presence_of_element_located(condition))
        try:
            elem = WebDriverWait(self.driver, wait).until(EC.element_to_be_clickable(condition))
        except Exception as e:
            Logger.log_warning(f"element_to_be_clickable failed for condition {str(condition)}")
        time.sleep(3)
        return elem

    def visible(self, condition, wait=30):
        elem = WebDriverWait(self.driver, wait).until(EC.presence_of_element_located(condition))
        return elem

    def click_on_element(self, tab_name, key, wait=max_wait_time):
        try:
            element = self.visible_clickable_new(tab_name=tab_name, key=key, wait=wait)
            element.click()
        except Exception:
            try:
                element = self.visible_clickable_new(tab_name=tab_name, key=key, wait=wait)
                self.driver.execute_script("arguments[0].click();", element)
            except Exception:
                Logger.log_warning(f'Could not click on {key} from {tab_name}')

    def click_on_element(self, element):
        try:
            element.click()
        except Exception:
            try:
                self.driver.execute_script("arguments[0].click();", element)
            except Exception:
                Logger.log_warning(f'Could not click on {element}, with text {element.text}')

    def visible_clickable_new(self, tab_name, key, wait=max_wait_time):
        element_info_list = locators.find_all_records(locators_file, tab_name, key)
        element = None
        for element_info in element_info_list:
            try:
                element = self.visible_clickable(condition=(element_info.get("By"), element_info.get("locator")), wait=wait)
                if element is not None:
                    break
            except Exception:
                Logger.log_warning(f'Could not find element by {element_info.get("By")} and locator {element_info.get("locator")}. Update {key} data in {tab_name} table')
        return element

    def find_all_elements(self, tab_name, key, wait=max_wait_time):
        element_info_list = locators.find_all_records(locators_file, tab_name, key)
        elements = None
        for element_info in element_info_list:
            try:
                if self.visible_clickable(condition=(element_info.get("By"), element_info.get("locator")), wait=wait):
                   elements = self.driver.find_elements(element_info.get("By"), element_info.get("locator"))
                if elements is not None:
                    break
            except Exception:
                Logger.log_warning(f'Could not find element by {element_info.get("By")} and locator {element_info.get("locator")}. Update {key} data in {tab_name} table')
        return elements

    def click_page_down(self, pages=1):
        element = self.driver.find_element_by_tag_name("body")
        for i in range(pages):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

    def click_page_up(self, pages=1):
        element = self.driver.find_element_by_tag_name("body")
        for i in range(pages):
            element.send_keys(Keys.PAGE_UP)
            time.sleep(1)

    def input_text(self, tab_name, key, text, field_length=1, wait=max_wait_time):
        try:
            element = self.visible_clickable_new(tab_name=tab_name, key=key, wait=wait)
            for i in range(field_length):
                element.send_keys(Keys.BACKSPACE)
            element.send_keys(text)
        except Exception:
            Logger.log_warning(
                f'Could not find element {key} in tab {tab_name}. Update {key} data in {tab_name} table')

    def get_breadcrumbs_links(self):
        elements = self.find_all_elements("Page", "breadcrumb")
        self.breadcrumbs_list = []
        for element in elements:
            if len(element.text) > 0:
                self.breadcrumbs_list_elements.update({element.text.strip(): element})
                self.breadcrumbs_list.append(element.text.strip())
        return self.breadcrumbs_list_elements

    def click_breadcrumb(self, name):
        self.breadcrumbs_list_elements.get(name).click()

    def switch_to_frame(self, tab_name, key, wait=max_wait_time):
        element_info_list = locators.find_all_records(locators_file, tab_name, key)
        for element_info in element_info_list:
            try:
                self.switch_v2_co_iframe(
                    by=element_info.get("By"),
                    locator=element_info.get("locator"),
                    wait=wait)
                break
            except Exception:
                Logger.log_warning(f"Frame {key} is not found. Check tab {tab_name} in locator file {locators_file}")

    def is_element_present(self, tab_name, key, wait=max_wait_time):
        element_info_list = locators.find_all_records(locators_file, tab_name, key)
        element = None
        for element_info in element_info_list:
            pass
        try:
            element = self.visible(condition=(element_info.get("By"), element_info.get("locator")), wait=wait)
        except TimeoutException:
            Logger.log_error(f'Element {key} from tab {tab_name} is not present.')
        return element

    @staticmethod
    def get_random_valid_zip_code():
        return Utils.get_random_list_element(ReadConfig.get_value_by_keys("Constants", 'ZIP CODES'))
