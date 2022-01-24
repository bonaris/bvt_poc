import pytest
from utils.read_config import ReadConfig

test_results_file = ReadConfig.get_test_results_filename()


class MyPlugin:

    def pytest_sessionfinish(self):
        print("\n\t*** test run reporting finishing")


pytest.main(["-x",  "--html", test_results_file, "--self-contained-html", "--browser", "chrome", "tests/steps/bvt/test_bvt_account.py"], plugins=[MyPlugin()])
