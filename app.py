import os
import json
import boto3
import random
import string

from pyvirtualdisplay import Display
from testexecutor import TestExecutor
import argparse
from datetime import datetime
from utils.logger import Logger
import requests
from requests.utils import requote_uri

logger = Logger.logger()


def list_tests(event, context):
    test_list = TestExecutor.list_tests()
    resp = {
        'test_cases': {'set': test_list},
        's3_prefix': datetime.strftime(datetime.today(), '%d-%m-%Y %H:%M:%S'),
        'start_time': datetime.strftime(datetime.today(), '%h %d, %H:%M'),
        'run_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    }
    return resp


def build_report(event, context):
    print('## EVENT')
    print(event)
    if not event.get('s3_bucket'):
        return __report_msg(500, 'S3 bucket not specified')
    if not event.get('ctx') or (len(event.get('ctx')) == 0):
        return __report_msg(500, 'Result section not found')

    run_rep = TestExecutor.test_results
    s3_prefix = None
    start_time = None
    for run_list in event.get('ctx'):
        if run_list.get('Payload') and run_list.get('Payload').get('tests_results'):
            s3_prefix = run_list.get('Payload').get('s3_prefix')
            start_time = run_list.get('Payload').get('start_time')
            run_id = run_list.get('Payload').get('run_id')
            for rep in run_list.get('Payload').get('tests_results'):
                if isinstance(rep, list) and (len(rep) > 0):
                    if (len(rep) == 10) and (rep[9] == run_id):
                        run_rep.append(rep)

    tmp_file = '/tmp/report.txt'
    report = ''
    fail_cnt = 0
    with open(tmp_file, 'w') as f:
        for line in run_rep:
            line_str = ' | '.join(line) + '\n'
            f.write(line_str)
            report = report + line_str
            if 'FAIL' in line:
                fail_cnt += 1
            print(line_str)

    if event.get('slack_webhook'):
        try:
            slack_rep = {
                "blocks": [{
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "ZGallerie Selenium Test result. " + start_time + " - " + datetime.strftime(datetime.today(), '%H:%M'),
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f" {':x:' if fail_cnt > 0 else ':white_check_mark:' }  "
                                f"{(len(run_rep)-fail_cnt-1)}/{(len(run_rep)-1)} tests passed  (*{'{:.0%}'.format((len(run_rep)-fail_cnt-1)/(len(run_rep)-1))}*)"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Report",
                                "emoji": True
                            },
                            "style": "primary",
                            "url": requote_uri(f"https://s3.console.aws.amazon.com/s3/object/{event.get('s3_bucket')}/{s3_prefix}/report.txt")
                        }
                    ]
                }]}

            print("slack payload: " + json.dumps(slack_rep))
            resp = requests.post(event.get('slack_webhook'), json=slack_rep)
        except Exception as e:
            logger.error('Slack webhook report post failed: \n%s' % e)

    try:
        s3_file = s3_prefix + '/' + 'report.txt'
        s3_client = boto3.client('s3')
        with open('/tmp/report.txt', 'rb') as data:
            s3_client.upload_fileobj(data, event.get('s3_bucket'), s3_file)
        print("Saved report to " + event.get('s3_bucket') + "::" + s3_file)
    except Exception as e:
        os.remove(tmp_file)
        raise Exception('S3 Report save failed: %s' % e)
    if fail_cnt > 0:
        raise Exception(report)
    else:
        return report


def lambda_handler(event, context):
    print('## ENVIRONMENT VARIABLES')
    print(os.environ)
    print('## EVENT')
    print(event)

    enable_display = False
    try:
        if 'DISPLAY' in os.environ and os.environ['DISPLAY'] == ':25':
            enable_display = True

        if enable_display:
            display = Display(visible=False, extra_args=[':25'], size=(2560, 1440))
            display.start()
            logger.info('Started Display %s' % os.environ['DISPLAY'])

        if not event.get('browser'):
            return __report_msg(500, 'Browser type not specified')

        s3_prefix = event.get('s3_prefix', datetime.strftime(datetime.today(), '%d-%m-%Y %H:%M:%S')) + '/' + event.get(
            'browser')
        result = TestExecutor.run_tests(
            testcase_class=event.get('aws_ctx').get('testcase_name', None) if event.get('aws_ctx') else None,
            browser=event.get('browser'), s3_bucket=event.get('s3_bucket', None),
            s3_prefix=s3_prefix, mode=event.get('Mode', None),
            run_id=event.get('run_id', None))
        return result[1] if (len(result) == 2) else []

    except Exception as e:
        logger.error('Lambda Execution failed: \n%s' % e)
        return __report_msg(200, 'Failed: %s' % e)


def __report_msg(http_code, msg):
    return {
        "statusCode": http_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({'message': msg})
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--browser', help='chrome/firefox/edge')
    parser.add_argument('--mode', help='iphone6/iphone7/iphone8/iphonex/pixel')
    parser.add_argument('--tc', help='specific test case file name')
    parser.add_argument('--type', help='specific test type bvt/e2e')

    args = parser.parse_args()

    TestExecutor.run_tests(testcase_class=args.tc, browser=args.browser, mode=args.mode)
