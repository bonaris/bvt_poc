import random
import time
import tempfile
import os
import sys
import logging
from pathlib import Path
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



class Utils():
    s3_client = None
    body = 'Dummy html email template'
    LOGGER = logging.getLogger()

    @staticmethod
    def check_for_newsletter_popup(driver):
        try:
            popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//div[@id="bx-creative-1382906"]')))
            time.sleep(2)
            if popup:
                popup.find_element_by_xpath(".//button[@type='reset']").click()
                Utils.LOGGER.info("Removed newsletter popup")
                time.sleep(2)
        except Exception as e:
            Utils.LOGGER.info('No Newsletter signup box displayed. {}'.format(str(e)))


    @staticmethod
    def exception_handler(exception, frame_name, ctx=None):
        ss_time = datetime.datetime.strftime(datetime.datetime.now(), '%m-%d_%H_%M_%S')
        ss_name = ctx.get('tc_name', '') + '_' + frame_name + "_" + ss_time + ".png"
        Utils.save_screenshot(ctx, ss_name)
        Utils.log_http_calls(ctx)
        ex_details = Utils.exception_line()
        error_msg = f'Exception occurred:---- {ex_details}:: Error:--- {exception}'
        Utils.LOGGER.error(error_msg)
        Utils.LOGGER.error(str(exception))
        raise Exception(error_msg)

    @staticmethod
    def log_http_calls(ctx):
        Utils.LOGGER.info("Http application/json calls")
        for request in ctx['driver'].requests:
            if request.response and (request.response.headers['Content-Type'] == 'application/json') \
                    and request.response.status_code > 302:
                Utils.LOGGER.info(f"{request.url} {request.response.status_code} {request.method} "
                                  f"{request.params if request.method == 'GET' else request.body} {request.response.body}")

    @staticmethod
    def visible_clickable(driver, condition, wait=30):
        elem = WebDriverWait(driver, wait).until(EC.presence_of_element_located(condition))
        try:
            elem = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(condition))
        except Exception as e:
            Utils.LOGGER.warning(f"element_to_be_clickable failed for condition {str(condition)}")
        time.sleep(3)
        return elem

    @staticmethod
    def visible(driver, condition, wait=30):
        elem = WebDriverWait(driver, wait).until(EC.presence_of_element_located(condition))
        return elem

    @staticmethod
    def exception_line():
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        line = exc_tb.tb_lineno
        exc_type = str(exc_type)
        line = str(line)
        exception = exc_type
        excepType = exception.split("'")
        excepType = excepType[1]
        details = fname + ' : An error occurred on line ' + \
            line + ' , Exception type : ' + excepType
        return details

    @staticmethod
    def save_screenshot(driver, tc_name=None, ss_name=None, frame_name=None):
        if not ss_name and frame_name:
            ss_time = datetime.datetime.strftime(datetime.datetime.now(), '%m-%d_%H_%M_%S')
            ss_name = tc_name + '_' + frame_name + "_" + ss_time + ".png"
        Path(tempfile.gettempdir()).mkdir(parents=True, exist_ok=True)
        data_file_path = tempfile.gettempdir() + os.path.sep + ss_name
        driver.save_screenshot(data_file_path)
        # if ctx.get('s3_bucket'):
        #     Utils.s3_client = boto3.client('s3') if Utils.s3_client is None else Utils.s3_client
        #     with open(data_file_path, 'rb') as data:
        #         Utils.s3_client.upload_fileobj(
        #             data, ctx.get('s3_bucket'), ctx.get('s3_prefix') + '/' + ss_name)
        # ss_list = [] if ctx.get('screenshots') is None else ctx.get('screenshots')
        # ss_list.append((ctx.get('s3_bucket') + '/' + ctx.get('s3_prefix') + '/' + ss_name)
        #                if ctx.get('s3_bucket') else data_file_path)
        # ctx['screenshots'] = ss_list

    @staticmethod
    def add_failure(ctx, failure):
        failures = [] if ctx.get('failures') is None else ctx.get('failures')
        failures.append(failure)
        ctx['failures'] = failures

    @staticmethod
    def fill_edit_fields(driver, keys_and_values, wait=5):
        for k in keys_and_values:
            Utils.visible_clickable(driver, (By.XPATH, k[0]), wait).send_keys(k[1])
            time.sleep(wait)

    @staticmethod
    def assign_cc_fields(xpaths, cc_data):
        cc_keys = [(xpaths.get("card_number"), cc_data.get('num')),
                   (xpaths.get("expiry_date"), cc_data.get('expiry')),
                   (xpaths.get("cvs"), cc_data.get('cvv'))]
        return cc_keys

    @staticmethod
    def get_random_list_element(elements_list):
        total_elements = len(elements_list)
        random_index = random.randint(0, total_elements - 1)
        return elements_list[random_index]

    @staticmethod
    def price_to_number(price):
        return float(price.replace('$', ""))


