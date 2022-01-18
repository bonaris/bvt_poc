from utils.utils import Utils
from utils.read_config import ReadConfig
from utils.logger import Logger

max_wait_time = ReadConfig.get_max_wait_time()


class BaseValidator:

    @staticmethod
    def is_visible_clickable(driver, by, locator, wait=max_wait_time):
        result = True
        try:
            Utils.visible_clickable(driver=driver, condition=(by, locator), wait=wait)
        except Exception as e:
            result = False
        return result

    @staticmethod
    def is_visible(driver, locator, by, wait=max_wait_time):
        result = True
        try:
            Utils.visible(driver=driver, condition=(by, locator), wait=wait)
        except Exception as e:
            result = False
        return result

    @staticmethod
    def validate_values(actual, expected, field_name):
        result = True
        Logger.log_validation(actual=actual, expected=expected, field=field_name)
        if actual != expected:
            result = False
            Logger.log_validation_error(field=field_name)
        else:
            Logger.log_info("\nPASS")
        return result

    @staticmethod
    def validate_not_empty(value, field_name):
        expected = f'{field_name}: {value}'
        actual = f'{field_name}: {value}'
        Logger.log_info(f'Field value: {value}')
        if len(value) <= 0:
            actual = f'{field_name} is empty'
        result = BaseValidator.validate_values(actual=actual, expected=expected, field_name=field_name)
        return result

