# pylint: disable=C0111,R0902,R0913,W0614,C0302,W0401
# Smartsheet Python SDK.
#
# Copyright 2016 Smartsheet.com, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import

import importlib
import logging
import logging.config
import os
import re
import random
import time
import sys
import requests
from requests_toolbelt.utils import dump
import six

from .exceptions import *
from .models import Error, ErrorResult
from .session import pinned_session
from .types import TypedList
from .util import is_multipart
from . import (
    __version__,
    __api_base__,
    models
)

__all__ = (
    'Smartsheet', 'fresh_operation', 'AbstractUserCalcBackoff'
)


def fresh_operation(op_id):
    """Create a default operation object."""
    operation = {'path': '', 'headers': {}, 'header_params': {},
                 'path_params': {}, 'query_params': {}, 'params': {},
                 'files': None, 'form_data': None, 'json': None, 'id': op_id,
                 'dl_path': None, 'auth_settings': 'access_token'}

    return operation


def setup_logging():
    """Allow for easy insight into SDK behavior."""
    log_env = os.environ.get('LOG_CFG', None)
    if log_env is not None:
        if os.path.exists(log_env):
            import json
            with open(log_env, 'rt') as config_file:
                config = json.load(config_file)
            logging.config.dictConfig(config)
        else:
            if log_env.upper() == 'DEBUG':
                logging.basicConfig(level=logging.DEBUG)
            elif log_env.upper() == 'INFO':
                logging.basicConfig(level=logging.INFO)


class AbstractUserCalcBackoff(object):

    def calc_backoff(self, previous_attempts, total_elapsed_time, error_result):
        raise NotImplementedError("Class %s doesn't implement calc_backoff()" % (self.__class__.__name__))


class DefaultCalcBackoff(AbstractUserCalcBackoff):

    def __init__(self, max_retry_time):
        self._max_retry_time = max_retry_time

    def calc_backoff(self, previous_attempts, total_elapsed_time, error_result):
        """
        Default back off calculator on retry.

        Args:
            previous_attempts(int) : number of previous retry attempts
            total_elapsed_time(float): elapsed time in seconds
            error_result(Smartsheet.models.ErrorResult): ErrorResult object for previous API attempt

        Returns:
             (float) Back off time in seconds (any negative number will drop out of retry loop)
        """
        if total_elapsed_time > self._max_retry_time:
            return -1

        # Use exponential backoff
        backoff = (2 ** previous_attempts) + random.random()
        return backoff


class Smartsheet(object):
    """Use this to make requests to the Smartsheet API."""

    models = models

    def __init__(self, access_token=None, max_connections=8,
                 user_agent=None, max_retry_time = 15, proxies=None):
        """
        Set up base client object.

        Args:
            access_token (str): Access Token for making client
                requests. May also be set as an env variable in
                SMARTSHEET_ACCESS_TOKEN. (required)
            max_connections (int): Maximum connection pool size.
            max_retry_time (int or AbstractUserCalcBackoff): user provided maximum
                elapsed time or AbstractUserCalcBackoff class for user back off calculation on retry.
            user_agent (str): The user agent to use when making requests. This
                helps us identify requests coming from your application. We
                recommend you use the format "AppName/Version". If set, we
                append "/SmartsheetPythonSDK/__version__" to the user_agent.
            proxies (dict): See the `requests module
                <http://docs.python-requests.org/en/latest/user/advanced/#proxies>`_
                for more details.
        """
        self.raise_exceptions = False
        if access_token:
            self._access_token = access_token
        else:
            self._access_token = os.environ.get(
                'SMARTSHEET_ACCESS_TOKEN', None)

        if self._access_token is None:
            raise ValueError('Access Token must be set in the environment '
                             'or passed to smartsheet.Smartsheet() '
                             'as a parameter.')

        if isinstance(max_retry_time, AbstractUserCalcBackoff):
            self._user_calc_backoff = max_retry_time
        else:
            self._user_calc_backoff = DefaultCalcBackoff(max_retry_time)

        self._session = pinned_session(pool_maxsize=max_connections)
        if proxies:
            self._session.proxies = proxies

        base_user_agent = 'SmartsheetPythonSDK/' + __version__
        if user_agent:
            self._user_agent = '{}/{}'.format(user_agent, base_user_agent)
        else:
            self._user_agent = base_user_agent

        self._log = logging.getLogger(__name__)
        setup_logging()
        self._url = ''
        self._api_base = os.environ.get(
            'API_BASE', __api_base__)
        self._assume_user = None

    def assume_user(self, email=None):
        """Assume identity of specified user.

        As an administrator, you can assume the identity of any user
        in your organization.

        Args:
            email (str): Valid email address of user whose identity
                should be assumed.
        """
        if email is None:
            self._assume_user = None
        else:
            # email = email.replace('@', '%40')
            self._assume_user = six.moves.urllib.parse.quote(email)

    def errors_as_exceptions(self, preference=True):
        """
        Set preference on whether or not to raise exceptions on API errors.
        When preference is True, exceptions will be raised. When False,
        instances of the Error data type will be returned.

        The property `raise_exceptions` defaults to False. Therefore, this
        method should only be called if exceptions *should* be raised.

        Args:
            preference (bool): Flag indicating whether errors should be raised
                as exceptions.
        """
        self.raise_exceptions = preference

    def request(self, prepped_request, expected, operation):
        """
        Make a request from the Smartsheet API.

        Make a request from the Smartsheet API and validate that inputs
        and outputs are as expected. The API response is converted from
        raw wire messages to a native objects based on the value of `expected`.

        Args:
            prepped_request (Request): Prepared request for the operation.
            expected (list|str): The expected response data type.

        Returns:
            The API operation result object.
        """
        res = self.request_with_retry(prepped_request, operation)
        native = res.native(expected)

        if not self.raise_exceptions:
            return native

        if isinstance(native, self.models.Error):
            the_ex = getattr(sys.modules[__name__], native.result.name)
            raise the_ex(native, str(native.result.code) + ': ' + native.result.message)
        else:
            return native

        return res.native(expected)

    def _request(self, prepped_request, operation):
        """
        Wrapper for the low-level Request action.

        Only low-level error handling.

        Args:
            prepped_request (Request): Prepared request for the operation.

        Returns:
            Operation Result object.
        """
        stream = False
        if operation['dl_path']:
            stream = True
        try:
            res = self._session.send(prepped_request, stream=stream)
        except requests.exceptions.SSLError as rex:
            raise HttpError(rex, 'SSL handshake error, old CA bundle or old OpenSSL?')
        except (requests.exceptions.RequestException) as rex:
            raise UnexpectedRequestError(rex.request, rex.response)

        # req_headers = dump_message_headers(res.request)
        # self._log.debug(req_headers)
        if is_multipart(res.request):
            res.request.body = '<< multipart body suppressed >>'
        if 200 <= res.status_code <= 299:
            if operation['dl_path'] is None:
                self._log.debug(dump.dump_response(res))
            else:
                self._log.debug(res.status_code)
                self._log.debug(res.headers)
            return OperationResult(res.text, res, self, operation)
        else:
            self._log.info(dump.dump_response(res))
            return OperationErrorResult(res.text, res)

    def request_with_retry(self, prepped_request, operation):
        """
        Perform the request with retry.

        Args:
            prepped_request (Request): A prepared request object for
                the operation.

        Returns:
            Operation Result object.
        """
        attempt = 0
        start_time = time.time()
        # Make a copy of the request as the access token will be redacted on response prior to logging
        pre_redact_request = prepped_request.copy()
        while True:
            self._log.info('Request to %s', prepped_request.url)
            result = self._request(prepped_request, operation)
            if isinstance(result, OperationErrorResult):
                native = result.native('Error')
                if native.result.should_retry:
                    attempt += 1
                    elapsed_time = time.time()-start_time
                    backoff = self._user_calc_backoff.calc_backoff(attempt,elapsed_time,native.result)
                    if backoff < 0:
                        break
                    self._log.info('HttpError status_code=%s: Retrying in %.1f seconds', native.result.status_code, backoff)
                    time.sleep(backoff)
                    # restore un-redacted request prior to retry
                    prepped_request = pre_redact_request.copy()
                else:
                    break
            else:
                break
        return result

    def prepare_request(self, _op):
        """Generate a Requests prepared request object."""
        if _op['header_params']:
            _op['headers'].update(_op['header_params'])

        if _op['path_params']:
            for key, val in six.iteritems(_op['path_params']):
                _op['path'] = _op['path'].replace('{' + key + '}', str(val))

        if _op['json']:
            if isinstance(_op['json'], (list, TypedList)):
                _op['json'] = [
                    x.to_dict(_op['id'], _op['method']) for x in _op['json']
                ]
            else:
                _op['json'] = _op['json'].to_dict(_op['id'], _op['method'])

        if _op['query_params']:
            for key, val in six.iteritems(_op['query_params']):
                if isinstance(val, list):
                    val = ','.join([str(num) for num in val])
                _op['query_params'][key] = val

        req = requests.Request(
            _op['method'],
            self._api_base + _op['path'],
            headers=_op['headers'],
            params=_op['query_params'],
            files=_op['files'],
            data=_op['form_data'],
            json=_op['json'])

        try:
            prepped_request = self._session.prepare_request(req)
        except TypeError as ex:
            # JSON not serializable for some reason
            self._log.debug(ex)

        prepped_request.headers.update({'User-Agent': self._user_agent})
        if _op['auth_settings'] is not None:
            auth_header_val = 'Bearer ' + self._access_token
            prepped_request.headers.update(
                {'Authorization': auth_header_val})

        if self._assume_user is not None:
            prepped_request.headers.update(
                {'Assume-User': self._assume_user})
        else:
            try:
                del prepped_request.headers['Assume-User']
            except KeyError:
                pass

        return prepped_request

    def __getattr__(self, name):
        """
        Handle sub-class instantiation.

        Args:
            name (str): Name of smartsheet to instantiate.

        Returns:
            Instance of named class.
        """
        try:
            # api class first
            self._log.debug('try loading api class %s', name)
            class_ = getattr(importlib.import_module(
                __package__ + '.' + name.lower()), name)
            self._log.debug('loaded instance of api class %s', name)
            return class_(self)
        except ImportError:
            # model class next:
            try:
                self._log.debug('try loading model class %s', name)
                class_ = getattr(importlib.import_module(
                    name.lower()), name)
                self._log.debug('loaded instance of model class %s', name)
                return class_()
            except ImportError:
                self._log.debug(
                    'ImportError! Cound not load api or model class %s', name)
                return name


class OperationResult(object):
    """The successful result of a call to an operation."""

    def __init__(self, op_result, resp=None, base_obj=None, operation=None):
        """Initialize OperationResult.

        Args:
            op_result (str): The result of an operation not including
                the binary payload portion, if one exists. Must be
                a JSON string.
            resp (requests.models.Response): A raw HTTP response.
                It will be used to stream the binary-body payload of the
                response.
            base_obj (smartsheet.Smartsheet): Configured core object
                for subsequent convenience method requests.
        """
        assert isinstance(op_result, six.string_types), \
            'op_result: expected string, got %r' % type(op_result)
        if resp is not None:
            assert isinstance(resp, requests.models.Response), \
                'resp: expected requests.models.Response, got %r' % \
                type(resp)
        self._base = base_obj
        self.op_result = op_result
        self.resp = resp
        self.dynamic_data_types = []
        self.operation = operation

    def native(self, expected):
        """Initialize expected result object and return it.

        Args:
            expected (list): Expected objects to return.

        Returns:
            Operation Result object or Operation Error Result object.
        """
        try:
            if expected != 'DownloadedFile':
                data = self.resp.json()
            else:
                filename = re.findall(
                        'filename="(.+)";',
                        self.resp.headers['Content-Disposition'])

                data = {
                    'resultCode': 0,
                    'message': 'SUCCESS',
                    'resp': self.resp,
                    'filename': filename[0],
                    'downloadDirectory': self.operation['dl_path']
                }
        except ValueError:
            return OperationErrorResult(self.op_result, self.resp)

        if isinstance(expected, list):
            klass = expected[0]
            dynamic_type = expected[1]
            class_ = getattr(importlib.import_module(
                'smartsheet.models'), klass)
            obj = class_(data, dynamic_type, self._base)
            if hasattr(obj, 'request_response'):
                obj.request_response = self.resp

            return obj

        class_ = getattr(importlib.import_module(
            'smartsheet.models'), expected)

        obj = class_(data, self._base)
        if hasattr(obj, 'request_response'):
            obj.request_response = self.resp

        return obj


class OperationErrorResult(object):
    """The error result of a call to an operation."""

    error_lookup = {
        0: {
            'name': 'ApiError',
            'recommendation': ('Do not retry without fixing the problem. '),
            'should_retry': False},
        4001: {
            'name': 'SystemMaintenanceError',
            'recommendation': ('Retry using exponential backoff. Hint: '
                               'Wait time between retries should measure '
                               'in minutes (not seconds).'),
            'should_retry': True},
        4002: {
            'name': 'ServerTimeoutExceededError',
            'recommendation': 'Retry using exponential backoff.',
            'should_retry': True},
        4003: {
            'name': 'RateLimitExceededError',
            'recommendation': ('Retry using exponential backoff. Hint: '
                               'Reduce the rate at which you are sending '
                               'requests.'),
            'should_retry': True},
        4004: {
            'name': 'UnexpectedErrorShouldRetryError',
            'recommendation': 'Retry using exponential backoff.',
            'should_retry': True},
    }

    def __init__(self, op_result, resp):
        """
        Initialize OperationErrorResult.

        Args:
            op_result (str): The result of an operation not including the
                binary payload portion, if one exists.
            resp (requests.models.Response): A raw HTTP response.
        """
        self.op_result = op_result
        self.resp = resp
        self._log = logging.getLogger(__name__)

    def native(self, expected):
        """
        Sadly, we won't be returning what was expected.

        Args:
            expected (list): Dashed expectations
        """
        # look up name of the error
        error_payload = self.resp.json()
        error_code = error_payload['errorCode']
        try:
            error_name = OperationErrorResult.error_lookup[error_code]['name']
            recommendation = OperationErrorResult.error_lookup[error_code]['recommendation']
            should_retry = OperationErrorResult.error_lookup[error_code]['should_retry']
        except:
            error_name = OperationErrorResult.error_lookup[0]['name']
            recommendation = OperationErrorResult.error_lookup[0]['recommendation']
            should_retry = OperationErrorResult.error_lookup[0]['should_retry']

        obj = Error({
            'result': ErrorResult({
                'name': error_name,
                'status_code': self.resp.status_code,
                'code': error_code,
                'message': error_payload['message'],
                'recommendation': recommendation,
                'should_retry': should_retry
            }),
            'request_response': self.resp
        })
        return obj
