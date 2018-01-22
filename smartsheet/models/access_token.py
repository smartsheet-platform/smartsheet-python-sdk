# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2018 Smartsheet.com, Inc.
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

import six
import json

from ..util import serialize
from ..util import deserialize


class AccessToken(object):

    """Smartsheet AccessToken data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the AccessToken model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'token_type': [
                'bearer']}

        self._access_token = None
        self._expires_in = None
        self._refresh_token = None
        self._token_type = None

        if props:
            deserialize(self, props)

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

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
