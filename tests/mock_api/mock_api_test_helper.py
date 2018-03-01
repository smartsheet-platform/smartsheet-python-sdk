import os
import smartsheet
from smartsheet.exceptions import ApiError


def clean_api_error(test_func):
    def wrapper(*args, **kwargs):
        try:
            test_func(*args, **kwargs)
        except ApiError as error:
            assert False, 'ApiError: ' + error.message

    return wrapper


class MockApiTestHelper(object):
    def setup_method(self, method):
        self.client = smartsheet.Smartsheet(access_token='abc123', api_base='http://localhost:8082')
        self.client.errors_as_exceptions()

    def check_error_code(self, exception_info, expected_error_code):
        actual_error_code = exception_info.value.error.result.error_code

        if self.is_test_scenario_error_code(actual_error_code):
            raise exception_info.value

        assert actual_error_code == expected_error_code

    def is_test_scenario_error_code(self, error_code):
        return error_code == 9999
