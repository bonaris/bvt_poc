import time

import pytest
from utils.read_config import ReadConfig

test_results_file = ReadConfig.get_test_results_filename().replace("^1", "")


class MyPlugin:

    def pytest_sessionfinish(self):
        print("\n\t*** test run reporting finishing")


pytest.main(["--html", test_results_file.replace("_^1", ""), "--self-contained-html", "--browser", "chrome", "tests/steps/bvt/test_bvt_01.py"], plugins=[MyPlugin()])
#str(time.time_ns())