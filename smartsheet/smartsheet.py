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

import requests
import requests_toolbelt
from requests_toolbelt.utils import dump
from requests_toolbelt.utils.user_agent import user_agent as ua
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
    'Smartsheet', 'fresh_operation',
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


class Smartsheet(object):
    """Use this to make requests to the Smartsheet API."""

    models = models

    def __init__(self, access_token=None, max_connections=8,
                 max_retries_on_error=4, user_agent=None,
                 proxies=None):
        """
        Set up base client object.

        Args:
            access_token (str): Access Token for making client
                requests. May also be set as an env variable in
                SMARTSHEET_ACCESS_TOKEN. (required)
            max_connections (int): Maximum connection pool size.
            max_retries_on_error (int): On 5xx errors, the number of times to
                retry.
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

        self._session = pinned_session(pool_maxsize=max_connections)
        if proxies:
            self._session.proxies = proxies
        self._max_retries_on_error = max_retries_on_error

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
            the_ex = native.name
            raise the_ex(native, native.code + ': ' + native.message)
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
        Perform the request with an expontial backoff retry.

        Args:
            prepped_request (Request): A prepared request object for
                the operation.

        Returns:
            Operation Result object.
        """
        attempt = 0
        while True:
            self._log.info('Request to %s', prepped_request.url)
            try:
                return self._request(prepped_request, operation)
            except (ApiError, HttpError) as err:
                if isinstance(err, (
                        InternalServerError, UnexpectedRequestError)):
                    # Do not count a rate limiting error as an attempt
                    attempt += 1
                if attempt <= self._max_retries_on_error:
                    # Use exponential backoff
                    backoff = 2 ** attempt * random.random()
                    self._log.info('HttpError status_code=%s: '
                                   'Retrying in %.1f seconds',
                                   err.status_code, backoff)
                    time.sleep(backoff)
                else:
                    raise

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
        1001: {
            'name': 'AccessTokenRequiredError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that Authorization header is '
                               'present and set properly.'),
            'should_retry': False},
        1002: {
            'name': 'AccessTokenInvalidError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that the access token '
                               'specified in the Authorization header is '
                               'valid.'),
            'should_retry': False},
        1003: {
            'name': 'AccessTokenExpiredError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Generate a new access token or '
                               'refresh the token.'),
            'should_retry': False},
        1004: {
            'name': 'UnauthorizedError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that Authorization header is '
                               'present and set properly, and that the '
                               'requester has the required permission '
                               'level in Smartsheet to perform the '
                               'requested action.'),
            'should_retry': False},
        1005: {
            'name': 'SSORequiredError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1006: {
            'name': 'NotFoundError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that specified URI is '
                               'correct. If the URI contains an object ID, '
                               'verify that the object ID is correct and '
                               'that the requester has access to the '
                               'corresponding object in Smartsheet.'),
            'should_retry': False},
        1007: {
            'name': 'VersionNotSupportedError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1008: {
            'name': 'UnparseableRequestError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1010: {
            'name': 'HttpMethodNotSupportedError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that the proper verb is '
                               'specified for the request (GET, PUT, POST, '
                               'or DELETE).'),
            'should_retry': False},
        1011: {
            'name': 'RequiredHeaderMissingInvalidError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1012: {
            'name': 'RequiredObjectAttributeMissingError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1013: {
            'name': 'UnsupportedByPlanError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1014: {
            'name': 'NoLicensesAvailableError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1015: {
            'name': 'UserExistsInAnotherAccountError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1016: {
            'name': 'UserAlreadyExistsError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1017: {
            'name': 'PaidUserAccountExistsError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1018: {
            'name': 'InvalidParameterValueError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1019: {
            'name': 'TransferNonexistentUserError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that the transferTo User ID '
                               'specified is correct.'),
            'should_retry': False},
        1020: {
            'name': 'UserNotFoundError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that the User ID specified is '
                               'correct.'),
            'should_retry': False},
        1021: {
            'name': 'TransferNonmemberUserError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1022: {
            'name': 'DeleteNonmemberUserError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1023: {
            'name': 'SheetSharedAtWorkspaceLevelError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1024: {
            'name': 'HttpBodyRequiredError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1025: {
            'name': 'ShareAlreadyExistsError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1026: {
            'name': 'TransferringOwnershipNotSupportedError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1027: {
            'name': 'ShareNotFoundError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that the Share ID specified '
                               'is correct.'),
            'should_retry': False},
        1028: {
            'name': 'EditShareOfOwnerError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1029: {
            'name': 'URIParameterDoesNotMatchBodyError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1030: {
            'name': 'UnableToAssumeUserError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1031: {
            'name': 'InvalidAttributeError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1032: {
            'name': 'AttributeNotAllowedError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1033: {
            'name': 'TemplateNotFoundError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that the Template ID '
                               'specified is correct.'),
            'should_retry': False},
        1034: {
            'name': 'InvalidRowIdError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1035: {
            'name': 'RowPostError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1036: {
            'name': 'InvalidColumnIdError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1037: {
            'name': 'DuplicateColumnIdError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1038: {
            'name': 'InvalidCellValueError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1039: {
            'name': 'EditLockedColumnError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1040: {
            'name': 'CannotEditOwnShareError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1041: {
            'name': 'InvalidCharacterLengthError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1042: {
            'name': 'StrictRequirementsFailureError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1043: {
            'name': 'BlankRowRetrievalError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1044: {
            'name': 'AssumeUserHeaderRequiredError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1045: {
            'name': 'ReadOnlyResourceError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1046: {
            'name': 'NotEditableViaApiError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1047: {
            'name': 'CannotRemoveSelfViaApiError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1048: {
            'name': 'ModifyDeclinedInvitationError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1049: {
            'name': 'CannotRemoveAdminForSelfViaApiError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1050: {
            'name': 'EditLockedRowError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1051: {
            'name': 'FileAttachmentUsingJsonError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1052: {
            'name': 'InvalidAcceptHeaderError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that Accept header is set to '
                               'the proper value (to match the output of '
                               'the invoked endpoint -- typically '
                               '"application/json").'),
            'should_retry': False},
        1053: {
            'name': 'UnknownPaperSizeError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1054: {
            'name': 'NewSheetMissingRequirementsError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1055: {
            'name': 'OnlyOnePrimaryError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1056: {
            'name': 'UniqueColumnTitlesError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1057: {
            'name': 'PrimaryColumnTypeError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1058: {
            'name': 'ColumnTypeSymbolTypeUnsupportedError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1059: {
            'name': 'ColumnOptionsNotAllowedWhenSymbolError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1060: {
            'name': 'ColumnOptionsNotAllowedForColumnTypeError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1061: {
            'name': 'MaxCountExceededError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1062: {
            'name': 'InvalidRowLocationError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1063: {
            'name': 'InvalidParentIdError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1064: {
            'name': 'InvalidSiblingIdError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1065: {
            'name': 'ColumnCannotBeDeletedError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1066: {
            'name': 'UserShareLimitError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Reduce the number of users specified '
                               'in the Share request.'),
            'should_retry': False},
        1067: {
            'name': 'InvalidClientIdError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that the value of the '
                               'client_id querystring parameter matches '
                               'the value of the App client Id shown in '
                               'the Smartsheet web UI (Developer Tools >> '
                               'App Profile).'),
            'should_retry': False},
        1068: {
            'name': 'UnsupportedGrantTypeError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that the value of the '
                               'grant_type querystring parameter is '
                               '"authorization_code".'),
            'should_retry': False},
        1069: {
            'name': 'AuthorizationCodeExpiredError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Repeat step 1 of the OAuth flow (to '
                               'retrieve a new authorization code).'),
            'should_retry': False},
        1070: {
            'name': 'RequiredParameterMissingError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1071: {
            'name': 'InvalidTokenProvidedError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1072: {
            'name': 'InvalidHashValueError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1073: {
            'name': 'RedirectUrlDidNotMatchError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Omit the redirect_uri querystring '
                               'parameter -- if redirect_uri is not '
                               'specified in the querystring, the value '
                               'specified in the Smartsheet web UI '
                               '(Developer Tools >> App Profile) will be '
                               'used by default.'),
            'should_retry': False},
        1074: {
            'name': 'UploadUnsupportedFileError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1075: {
            'name': 'ContentSizeDidNotMatchError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1076: {
            'name': 'UserMustBeLicensedError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1077: {
            'name': 'DuplicateSystemColumnTypeError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1078: {
            'name': 'SystemColumnTypeNotSupportedError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1079: {
            'name': 'ColumnTypeNotSupportedForSystemTypeError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1080: {
            'name': 'DependencyEnabledEndDatesError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1081: {
            'name': 'DeleteAnotherUserDiscussionElementsError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1082: {
            'name': 'NonPicklistError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1083: {
            'name': 'AutoNumberFormattingCannotBeAddedError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1084: {
            'name': 'AutoNumberFormatInvalidError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1085: {
            'name': 'ChangeColumnDisableDependenciesFirstError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1086: {
            'name': 'GoogleAccessVerificationError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1087: {
            'name': 'ColumnRequiredByConditionalFormattingError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1088: {
            'name': 'InvalidLengthAutoNumberFormatError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1089: {
            'name': 'TypeForSystemColumnsOnlyError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1090: {
            'name': 'ColumnTypeRequiredError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1091: {
            'name': 'InvalidContentTypeError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1092: {
            'name': 'LockedChildrenError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1095: {
            'name': 'ExcelFileCorruptError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1096: {
            'name': 'ApplePaymentReceiptAlreadyAppliedError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1097: {
            'name': 'LicensedSheetCreatorRequiredError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1098: {
            'name': 'DeleteColumnDisableDependenciesFirstError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1099: {
            'name': 'DeleteColumnDisableResourceManagementFirstError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1100: {
            'name': 'DiscussionCommentAttachmentVersionsNotSupportedError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1101: {
            'name': 'NewVersionsNonFileNotSupportedError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1102: {
            'name': 'AdminRequiresLicensedSheetCreatorError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1103: {
            'name': 'GroupNameExistsError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1104: {
            'name': 'GroupAdminMustCreateGroupError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that the requester has "Group '
                               'Admin" permissions in Smartsheet.'),
            'should_retry': False},
        1105: {
            'name': 'GroupMembersNotMembersOfAccountError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1106: {
            'name': 'GroupNotFoundError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that specified Group ID is '
                               'correct.'),
            'should_retry': False},
        1107: {
            'name': 'TransferGroupsToUserMustBeGroupAdminError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1108: {
            'name': 'TransferGroupsToValueRequiredError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1109: {
            'name': 'OnlyOneLinkMayBeNonNullError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1110: {
            'name': 'CellValueMustBeNullError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1111: {
            'name': 'OnlyOneNullCellHyperlinkSheetIdReportIdError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1112: {
            'name': 'CellHyperlinkUrlMustBeNullError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1113: {
            'name': 'CellHyperlinkValueMustBeStringError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1114: {
            'name': 'InvalidSheetIdOrReportIdError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1115: {
            'name': 'UpdateTypeMixingNotSupportedError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1116: {
            'name': 'CellLinkToSelfSheetError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1117: {
            'name': 'CellHyperlinkNeedsUrlSheetIdOrReportIdError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1118: {
            'name': 'GanttAllocationColumnIdError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1119: {
            'name': 'CopyFailedError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1120: {
            'name': 'TooManySheetsToCopyError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Reduce number of sheets being copied '
                               'to maxSheetCount or fewer before '
                               'reattempting the request.'),
            'should_retry': False},
        1121: {
            'name': 'TransferToRequiredError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1122: {
            'name': 'UnsupportedMethodError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that the verb specified for '
                               'the request (GET, POST, PUT, DELETE) is '
                               'valid for the specified URI.'),
            'should_retry': False},
        1123: {
            'name': 'MultipleRowLocationSpecificationError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1124: {
            'name': 'InvalidContentTypeMediaUnsupportedError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that Content-Type header is '
                               'specified and set to the proper value.'),
            'should_retry': False},
        1125: {
            'name': 'AllPartsRequireNamesMultipartPayloadError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1126: {
            'name': 'DuplicatePartNamesMultipartPayloadError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1127: {
            'name': 'RequiredMultiPartPartMissingError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1128: {
            'name': 'MultipartUploadSizeLimitExceededError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1129: {
            'name': 'ResourceAlreadyExistsError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1130: {
            'name': 'CellValueOrObjectValueError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1131: {
            'name': 'CellWrongObjectTypeError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1132: {
            'name': 'TokenRevokedError',
            'recommendation': ('Do not retry. Hint: This error occurs '
                               'during the OAuth flow when trying to '
                               'refresh a token that\'s previously been '
                               'revoked.  Must instead obtain a new token.'),
            'should_retry': False},
        1133: {
            'name': 'ColumnTitlesNotUniqueInInputError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1134: {
            'name': 'DuplicateSystemColumnTypesInInputError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1135: {
            'name': 'InputColumnIndexDiffersFromFirstInputColumnIndexError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1136: {
            'name': 'CopyMoveInSameSheetError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1137: {
            'name': 'MultipleInstancesSameElementError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1138: {
            'name': 'UserIneligibleForTrialOrgError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1139: {
            'name': 'UserAdminAnotherOrgError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1140: {
            'name': 'UserMustBeAddedAsLicensedError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1141: {
            'name': 'InvitingEnterpriseUsersError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1142: {
            'name': 'ColumnTypeReservedForProjectSheetsError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1143: {
            'name': 'EnableSheetDependenciesFirstError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1144: {
            'name': 'UserOwnsOnePlusGroupsError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1145: {
            'name': 'InvalidMultipartUploadRequestError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1146: {
            'name': 'UnsupportedOperationError',
            'recommendation': 'Do not retry.',
            'should_retry': False},
        1147: {
            'name': 'InvalidPartNameMultipartPayloadError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        1148: {
            'name': 'CellValuesOutOfRangeError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        2000: {
            'name': 'InvalidUsernameOrPasswordError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        2001: {
            'name': 'AccountLockedError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        2002: {
            'name': 'InvalidEmailAddressError',
            'recommendation': ('Do not retry without fixing the problem. '
                               'Hint: Verify that value of Assume-User '
                               'header is URL-encoded.'),
            'should_retry': False},
        2003: {
            'name': 'AccountBillingLockError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        2004: {
            'name': 'EmailConfirmationRequiredError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        2005: {
            'name': 'DeviceIdExceedsMaxLengthError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        2006: {
            'name': 'InvalidClientIdProvidedError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        2008: {
            'name': 'InvalidLoginTicketError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        2009: {
            'name': 'LaunchParametersProvidedUnsupportedError',
            'recommendation': 'Do not retry without fixing the problem.',
            'should_retry': False},
        4000: {
            'name': 'UnexpectedError',
            'recommendation': 'Do not retry.',
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
            'should_retry': True}
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
        error_name = OperationErrorResult.error_lookup[error_code]['name']
        obj = Error({
            'result': ErrorResult({
                'name': error_name,
                'status_code': self.resp.status_code,
                'code': error_code,
                'message': error_payload['message'],
                'recommendation': OperationErrorResult
                              .error_lookup[error_code]['recommendation'],
                'should_retry': OperationErrorResult
                            .error_lookup[error_code]['should_retry']
            }),
            'request_response': self.resp
        })
        return obj
