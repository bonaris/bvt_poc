import time
from utils.logger import Logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    driver = None

    def switch_v2_co_iframe(self, by='xpath', locator="//*[@id='checkoutV2']", wait=40):
        try:
            WebDriverWait(self.driver, wait).until(EC.frame_to_be_available_and_switch_to_it((by, locator)))
        except Exception as e:
            Logger.log_error("failed to find path: " + locator + ", so trying switch to default_context")
            self.driver.switch_to.default_content()
            v2_iframes = self.driver.find_elements_by_xpath(locator)
            if len(v2_iframes) > 0:
                self.driver.switch_to.frame(v2_iframes[0])

    def visible_clickable(self, condition, wait=30):
        elem = WebDriverWait(self.driver, wait).until(EC.presence_of_element_located(condition))
        try:
            elem = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(condition))
        except Exception as e:
            Logger.log_warning(f"element_to_be_clickable failed for condition {str(condition)}")
        time.sleep(3)
        return elem

    @staticmethod
    def visible(driver, condition, wait=30):
        elem = WebDriverWait(driver, wait).until(EC.presence_of_element_located(condition))
        return elem

