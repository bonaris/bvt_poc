import logging
import inspect
from utils.read_config import ReadConfig


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


class Logger():
    # only /tmp in aws lambda works for logging as other directories are treated readonly
    file_handler = logging.FileHandler("/tmp/automation.log", mode='a')

    @staticmethod
    def logger(logLevel=logging.DEBUG):
        logger = logging.getLogger(inspect.stack()[1][3])
        # By default, log all messages
        logger.setLevel(logging.DEBUG)
        Logger.file_handler.setLevel(logLevel)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
        Logger.file_handler.setFormatter(formatter)
        logger.addHandler(Logger.file_handler)
        return logger

    @staticmethod
    def log_info(string):
        LOGGER.info(Logger.get_log_string(string))

    @staticmethod
    def log_warning(string):
        LOGGER.warning(Logger.get_log_string(string))

    @staticmethod
    def log_error(string):
        LOGGER.error(Logger.get_log_string(string))

    @staticmethod
    def log_validation(actual, expected, field="values"):
        string = f'\nValidating {field}'
        string += f'\nExpected: {expected}'
        string += f'\nActual:   {actual}'
        LOGGER.info(Logger.get_log_string(string))

    @staticmethod
    def log_not_equal_validation(value_1, value_2, field="values"):
        string = f'\nValidating is not equal {field}'
        string += f'\nValue 1: {value_1}'
        string += f'\nValue 2: {value_2}'
        LOGGER.info(Logger.get_log_string(string))


    @staticmethod
    def log_validation_error(field="values"):
        string = f'\nValidation Failed {field}'
        LOGGER.error(Logger.get_log_string(string))

    @staticmethod
    def log_validation_warning(field="values"):
        string = f'\nValidation Failed {field}'
        LOGGER.warning(Logger.get_log_string(string))

    @staticmethod
    def get_log_string(string):
        full_string = ReadConfig.get_test_log_header() + string
        return full_string
