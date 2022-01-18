import configparser

config = configparser.RawConfigParser()
config.read(".\\config\\config.ini")


class ReadConfig:
    @staticmethod
    def get_url():
        return config.get('store-info', 'store_url')

    @staticmethod
    def get_test_data_filename():
        return config.get('file-info', 'test_data_file')

    @staticmethod
    def get_test_results_filename():
        return config.get('file-info', 'test_results_file')

    @staticmethod
    def get_locators_filename():
        return config.get('file-info', 'locators_file')

    @staticmethod
    def get_test_log_header():
        return config.get('log-info', 'header')

    @staticmethod
    def get_test_log_footer():
        return config.get('log-info', 'header')

    @staticmethod
    def get_log_level():
        return config.get('log-info', 'log_level')

    @staticmethod
    def get_max_wait_time():
        return int(config.get('test-info', 'max_wait_time'))

    @staticmethod
    def get_value_by_keys(section, key):
        return config.get(section, key)
