# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
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

from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class OAuthError(object):

    """Smartsheet OAuthError data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the OAuthError model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self.allowed_values = {
            'error': [
                'invalid_request',
                'invalid_client',
                'invalid_grant',
                'unauthorized_client',
                'unsupported_grant_type',
                'invalid_scope']}

        self._error = None
        self._error_code = None
        self._error_description = None

        if props:
            # account for alternate variable names from raw API response
            if 'error' in props:
                self.error = props['error']
            if 'errorCode' in props:
                self.error_code = props['errorCode']
            if 'error_code' in props:
                self.error_code = props['error_code']
            if 'error_description' in props:
                self.error_description = props[
                    'error_description']
        # requests package Response object
        self.request_response = None

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['error']:
                raise ValueError(
                    ("`{0}` is an invalid value for OAuthError`error`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['error']))
            self._error = value

    @property
    def error_code(self):
        return self._error_code

    @error_code.setter
    def error_code(self, value):
        if isinstance(value, six.integer_types):
            self._error_code = value

    @property
    def error_description(self):
        return self._error_description

    @error_description.setter
    def error_description(self, value):
        if isinstance(value, six.string_types):
            self._error_description = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'error': prep(self._error),
            'errorCode': prep(self._error_code),
            'error_description': prep(self._error_description)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
