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

class AccessToken(object):

    """Smartsheet AccessToken data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the AccessToken model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self.allowed_values = {
            'token_type': [
                'bearer']}

        self._access_token = None
        self._expires_in = None
        self._refresh_token = None
        self._token_type = None

        if props:
            if 'access_token' in props:
                self.access_token = props['access_token']
            if 'expires_in' in props:
                self.expires_in = props['expires_in']
            if 'refresh_token' in props:
                self.refresh_token = props['refresh_token']
            if 'token_type' in props:
                self.token_type = props['token_type']
        # requests package Response object
        self.request_response = None

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        if isinstance(value, six.string_types):
            self._access_token = value

    @property
    def expires_in(self):
        return self._expires_in

    @expires_in.setter
    def expires_in(self, value):
        if isinstance(value, six.integer_types):
            self._expires_in = value

    @property
    def refresh_token(self):
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, value):
        if isinstance(value, six.string_types):
            self._refresh_token = value

    @property
    def token_type(self):
        return self._token_type

    @token_type.setter
    def token_type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['token_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for AccessToken`token_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['token_type']))
            self._token_type = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'access_token': prep(self._access_token),
            'expires_in': prep(self._expires_in),
            'refresh_token': prep(self._refresh_token),
            'token_type': prep(self._token_type)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
