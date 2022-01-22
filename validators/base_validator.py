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
        if value is None:
            actual = f'{field_name} is empty'
        result = BaseValidator.validate_values(actual=actual, expected=expected, field_name=field_name)
        return result

    @staticmethod
    def validate_is_not_equal(value_1, value_2, field_name):
        result = True
        Logger.log_not_equal_validation(value_1=value_1, value_2=value_2, field=field_name)
        if value_1 == value_2:
            result = False
            Logger.log_validation_error(field=field_name)
        else:
            Logger.log_info("\nPASS")
        return result

    @staticmethod
    def validate_list(actual_list, expected_list, list_name, sort_first=False):
        result = True
        if sort_first:
            actual_list.sort()
            expected_list.sort()

        if BaseValidator.validate_values(len(actual_list), len(expected_list), f"Total items in {list_name}"):
            for i in range(len(actual_list)-1):
                if BaseValidator.validate_values(actual_list[i], expected_list[i], f"List element: {str(i)}"):
                    result = False
        else:
            result = False
        return result

    @staticmethod
    def validate_breadcrumbs(actual_list, expected, separator='/'):
        result = True
        expected_list = expected.split(separator)

        if BaseValidator.validate_values(len(actual_list), len(expected_list), "Total breadcrumbs items"):
            if not BaseValidator.validate_values(str(actual_list), str(expected_list), "Breadcrumbs items"):
                result = False
        else:
            result = False
        return result
