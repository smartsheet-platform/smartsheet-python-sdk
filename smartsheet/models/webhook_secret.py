# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2017 Smartsheet.com, Inc.
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

from ..util import prep
import logging
import six
import json

class WebhookSecret(object):

    """Smartsheet WebhookSecret data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the WebhookSecret model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._shared_secret = None

        if props:
            # account for alternate variable names from raw API response
            if 'sharedSecret' in props:
                self.shared_secret = props['sharedSecret']
            if 'shared_secret' in props:
                self.shared_secret = props['shared_secret']

        # requests package Response object
        self.request_response = None
        self.__initialized = True

    @property
    def shared_secret(self):
        return self._shared_secret

    @shared_secret.setter
    def shared_secret(self, value):
        if isinstance(value, six.string_types):
            self._shared_secret = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'sharedSecret':prep(self._shared_secret)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())