import unittest
import boto3
from pathlib import Path
from utils import logger


class TestExecutor(object):
    s3_client = None
    test_results = [['TestCase', 'Browser/Mode', 'StartTime', 'EndTime',
                     'UserType', 'Status', 'Order #', 'FailReasons', 'Screenshots', 'RunID']]
    @staticmethod
    def run_tests(testcase_class=None, browser='chrome', s3_bucket=None, test_type='bvt',
                  s3_prefix=None, run_id=None, mode=None):

        loader = unittest.TestLoader()
        if testcase_class:
            suite = unittest.TestSuite()
            tcs = testcase_class.split(",")
            for tc in tcs:
                suite.addTests(loader.discover(start_dir='tests/steps', pattern=('*' + tc.strip() + '*'))._tests)
        else:
            suite = loader.discover(start_dir='tests/steps', pattern='test*.py')
        TestExecutor.set_params(suite, browser, s3_bucket, s3_prefix, run_id, mode)

        with open('/tmp/test-result.out', 'w') as f:
            unittest.TextTestRunner(f, verbosity=2).run(suite)

            for line in TestExecutor.test_results:
                f.write(' | '.join(line) + '\n')
                print(' | '.join(line) + '\n')
            with open(logger.Logger.file_handler.baseFilename, 'r') as lf:
                for line in lf:
                    f.write(line)

        if s3_bucket:
            TestExecutor.s3_client = boto3.client('s3') if TestExecutor.s3_client is None else TestExecutor.s3_client
            s3_file = s3_prefix + '/' + ((testcase_class.replace('.py', '') + '_')
                                         if testcase_class else '') + 'test-result.txt'
            with open('/tmp/test-result.out', 'rb') as data:
                TestExecutor.s3_client.upload_fileobj(data, s3_bucket, s3_file)
            print("Saved test result to " + s3_bucket + "::" + s3_file)
        return TestExecutor.test_results

    @staticmethod
    def set_params(suites, browser, s3_bucket, s3_prefix, run_id, mode):
        def list_suites(suite, t_cases={}):
            if hasattr(suite, '__iter__'):
                for x in suite:
                    list_suites(x, t_cases)
            else:
                if hasattr(suite, 'ctx') and not t_cases.get(suite.__class__, None):
                    t_cases[suite.__class__] = suite

        cases = {}
        list_suites(suites, cases)
        for case in cases.values():
            case.ctx = {
                "browser": browser,
                "mode": mode,
                "s3_prefix": s3_prefix,
                "s3_bucket": s3_bucket,
                "run_id": run_id,
                "test_results": TestExecutor.test_results
            }

    @staticmethod
    def list_tests():
        return [{'testcase_name': path.name} for path in Path('tests').rglob('test*.py')]

if __name__ == '__main__':
    TestExecutor.run_tests(
        browser='chrome',
        # mode='pixel',
        testcase_class='test_bvt_01.py'
    )
