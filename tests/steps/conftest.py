from utils.logger import Logger
import pytest
from utils.browser_utils import create_browser_instance


@pytest.fixture
def driver(request, browser, mode, useremail):

    driver = create_browser_instance(browser, mode)
    if request.cls is not None:
        request.cls.driver = driver

    yield driver
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--mode", help="Desktop or iphone-X, iPhone-6/7/8")
    parser.addoption("--useremail", help="email to report")


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def mode(request):
    return request.config.getoption("--mode")


@pytest.fixture(scope="session")
def useremail(request):
    return request.config.getoption("--useremail")


@pytest.fixture(scope='function')
def context():
    return {}
