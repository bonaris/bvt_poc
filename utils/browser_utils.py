from utils.logger import Logger
import time
import os
import sys
import random
import string
import platform
import config.broswers as browser_data
from msedge.selenium_tools import EdgeOptions, Edge
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from seleniumwire import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as ff_options

logger = Logger.logger()


def linux_ff_browser(firefox_options, browser_version, driver_version):
    if not firefox_options:
        firefox_options = ff_options()
        firefox_options.add_argument("-safe-mode")
        firefox_options.add_argument('window-size=2560,1440')

    try:
        browser_version = browser_version if browser_version else '93.0'
        driver_version = driver_version if driver_version else '0.30.0'
        random_dir = '/tmp/' + ''.join(random.choice(string.ascii_lowercase) for i in range(8))
        os.mkdir(random_dir)
        ff_profile = webdriver.FirefoxProfile(profile_directory=random_dir)
        driver = webdriver.Firefox(firefox_profile=ff_profile,
                                   firefox_binary='/opt/firefox/' + browser_version + '/firefox',
                                   executable_path='/opt/geckodriver/' + driver_version + '/geckodriver',
                                   options=firefox_options,
                                   service_log_path='/tmp/geckodriver.log')
        return driver
    except:
        print("Linux FF browser instance create error:", sys.exc_info()[0])
        print('#### /tmp/geckodriver.log ####')
        with open('/tmp/geckodriver.log', 'r') as f:
            print(f.read())
        raise


def linux_chrome_browser(chrome_options, browser_version, driver_version):
    if not chrome_options:
        chrome_options = Options()

    browser_version = browser_version if browser_version else "93.0.4577.0"
    driver_version = driver_version if driver_version else "93.0.4577.63"
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("window-size=2560x1440")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    chrome_options.add_argument("--remote-debugging-port=9230")
    chrome_options.binary_location = '/opt/chrome/' + browser_version + '/chrome'
    driver = webdriver.Chrome(executable_path='/opt/chromedriver/' + driver_version + '/chromedriver',
                              options=chrome_options,
                              service_log_path='/tmp/chromedriver.log')
    return driver


def create_browser_instance(browser_type=None,
                            mode=None,
                            browser_version=None,
                            driver_version=None):
    os_type = platform.system()
    if browser_type == 'firefox' or browser_type == 'ff':
        if os_type == "Linux":
            driver = linux_ff_browser(None, browser_version, driver_version)
        elif os_type == "Darwin":
            driver = webdriver.Firefox(executable_path=browser_data._firefox_browser_mac)
        else:
            driver = webdriver.Firefox(executable_path=browser_data._firefox_browser)
        driver.delete_all_cookies()
        driver.maximize_window()
        driver.implicitly_wait(5)
        logger.info(f'Running tests on FF. Window size {driver.get_window_size()}')

    elif browser_type == 'firefox_headless' or browser_type == 'ff_headless':
        options = ff_options()
        options.add_argument('--headless')
        options.add_argument("window-size=1936,1056")
        if os_type == "Darwin":
            driver = webdriver.Firefox(
                executable_path=browser_data._firefox_browser_mac, options=options)
        elif os_type == "Linux":
            driver = linux_ff_browser(options, browser_version, driver_version)
        else:
            driver = webdriver.Firefox(
                executable_path=browser_data._firefox_browser, options=options)
        driver.delete_all_cookies()
        driver.maximize_window()
        driver.implicitly_wait(5)
        logger.info(f'ff browser size ====={driver.get_window_size()}')
        logger.info(f'Running tests on FF headless. Window size {driver.get_window_size()}')

    elif browser_type == 'chrome':
        if os_type == "Darwin":
            driver = webdriver.Chrome(browser_data._chrome_browser_mac)
        elif os_type == "Linux":
            driver = linux_chrome_browser(None, browser_version, driver_version)
        else:
            chrome_driver_manager = ChromeDriverManager()
            driver = webdriver.Chrome(chrome_driver_manager.install())
        driver.delete_all_cookies()
        driver.maximize_window()
        driver.implicitly_wait(3)
        logger.info(f'Running tests on chrome. Window size {driver.get_window_size()}')

    elif browser_type == 'chrome_headless':
        options = Options()
        options.add_argument('--headless')
        options.add_argument("window-size=1936,1056")
        
        if os_type == "Darwin":
            driver = webdriver.Chrome(
                browser_data._chrome_browser_mac, options=options)
        elif os_type == "Linux":
            driver = linux_chrome_browser(options, browser_version, driver_version)
        else:
            driver = webdriver.Chrome(
                browser_data._chrome_browser, options=options)
        driver.delete_all_cookies()
        driver.maximize_window()
        driver.implicitly_wait(3)
        logger.info(f'headless chrome window size is ===={driver.get_window_size()}')
        logger.info(f'Running tests on chrome headless. Window size {driver.get_window_size()}')

    elif browser_type == "remote_chrome":
        time.sleep(5)
        desiredCapabilities = DesiredCapabilities.CHROME.copy()
        cap = {"configuration": {
            "_comment": "Configuration for Node", "timeout": 30000}}
        desiredCapabilities.update(cap)
        chromeOptionsRemote = webdriver.ChromeOptions()
        chromeOptionsRemote.add_argument("--start-maximized")
        chromeOptionsRemote.add_argument("--disable-session-crashed-bubble")
        chromeOptionsRemote.add_argument("window-size=1936,1056")
        chromeOptionsRemote.add_argument("--disable-dev-shm-usage")
        chromeOptionsRemote.add_argument("--disable-gpu")
        chromeOptionsRemote.add_argument("--no-sandbox")
        driver = webdriver.Remote(command_executor='http://192.168.0.17:4444/wd/hub',
                                  desired_capabilities=desiredCapabilities, options=chromeOptionsRemote)
        driver.maximize_window()

        logger.info(f'Running tests on HUB chrome. Window size {driver.get_window_size()}')
        logger.info(f'Running tests on HUB chrome. Window size {driver.get_window_size()}')
        driver.implicitly_wait(3)

    elif browser_type == "remote_ff":
        time.sleep(25)
        desiredCapabilities = DesiredCapabilities.FIREFOX.copy()
        cap = {"configuration": {"_comment": "Configuration for Node", "timeout": 30000}}
        desiredCapabilities.update(cap)
        ff_options_remote = webdriver.FirefoxOptions()
        ff_options_remote.add_argument("--start-maximized")
        ff_options_remote.add_argument("--disable-session-crashed-bubble")
        ff_options_remote.add_argument("window-size=1936,1056")
        ff_options_remote.add_argument("--disable-dev-shm-usage")
        ff_options_remote.add_argument("--disable-gpu")
        ff_options_remote.add_argument("--no-sandbox")

        driver = webdriver.Remote(command_executor='http://192.168.0.17:4444/wd/hub',
                                  desired_capabilities=desiredCapabilities, options=ff_options_remote)
        driver.maximize_window()
        driver.set_window_size(1936, 1056)
        print(f'Running tests on HUB ff. Window size {driver.get_window_size()}')
        logger.info(f'Running tests on HUB ff. Window size {driver.get_window_size()}')
        driver.implicitly_wait(3)

    elif browser_type == 'edge':
        if os_type == "Linux":
            options = EdgeOptions()
            options.use_chromium = True
            options.binary_location = r"/usr/bin/microsoft-edge"
            options.set_capability("platform", "LINUX")
            options.headless = True
            options.debugger_address = "127.0.0.1:9222"
            driver = Edge(options=options, executable_path=browser_data._edge_browser_linux)
        else:
            driver = webdriver.Edge(seleniumwire_options={'port': 12345}, executable_path=browser_data._edge_browser_new)
        driver.delete_all_cookies()
        driver.maximize_window()
        driver.implicitly_wait(3)
        logger.info(f'Running tests on Edge. Window size {driver.get_window_size()}')

    elif mode == 'iphone6' or mode == 'iphone7' or mode == 'iphone8':
        mobile_emulation = {'deviceMetrics': {'width': 375, 'height': 667},
                            'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        chrome_options = Options()
        chrome_options.add_experimental_option(
            "mobileEmulation", mobile_emulation)
        driver = webdriver.Chrome(
            browser_data._chrome_browser, options=chrome_options)
        driver.delete_all_cookies()
        driver.set_window_size(375, 812)
        # driver.maximize_window()
        driver.implicitly_wait(3)
        logger.info(f'Running test on chrome browser for {mode} emulator. Window size {driver.get_window_size()}')

    elif mode == 'iphonex':
        mobile_emulation = {'deviceMetrics': {'width': 375, 'height': 812, 'pixelRatio': 3.0},
                            'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}

        chrome_options = Options()
        chrome_options.add_experimental_option(
            "mobileEmulation", mobile_emulation)
        driver = webdriver.Chrome(
            browser_data._chrome_browser, options=chrome_options)
        driver.delete_all_cookies()
        driver.set_window_size(375,976)
        # driver.maximize_window()
        driver.implicitly_wait(3)
        logger.info(
            f'Running test on chrome browser for {mode} emulator. Window size {driver.get_window_size()}')

    elif mode == '':
        mobile_emulation = {'deviceMetrics': {'width': 375, 'height': 812},
                            'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}

        chrome_options = Options()
        chrome_options.add_experimental_option(
            "mobileEmulation", mobile_emulation)
        driver = webdriver.Chrome(
            browser_data._chrome_browser, options=chrome_options)
        driver.delete_all_cookies()
        driver.set_window_size(375, 976)
        # driver.maximize_window()
        driver.implicitly_wait(3)
        logger.info(f'Running test on chrome browser for iPhoneX emulator. Window size {driver.get_window_size()}')

    elif mode == 'pixel':
        mobile_emulation = {'deviceMetrics': {'width': 411, 'height': 823},
                            'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        chrome_options = Options()
        chrome_options.add_experimental_option(
            "mobileEmulation", mobile_emulation)

        if os_type == "Darwin":
            driver = webdriver.Chrome(browser_data._chrome_browser_mac, options=chrome_options)
        else:
            driver = webdriver.Chrome(browser_data._chrome_browser, options=chrome_options)
        driver.delete_all_cookies()
        driver.set_window_size(375, 976)
        # driver.maximize_window()
        driver.implicitly_wait(3)
        logger.info(f'Running test on chrome browser for {mode} emulator. Window size {driver.get_window_size()}')
    else:
        driver = webdriver.Chrome(browser_data._chrome_browser)
        driver.maximize_window()
        driver.implicitly_wait(5)
        logger.info(f'Running tests on chrome. Window size {driver.get_window_size()}')

    return driver
