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

from ..types import *
from ..util import serialize
from ..util import deserialize


class WebhookStats(object):

    """Smartsheet WebhookStats data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the WebhookStats model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._last_callback_attempt = Timestamp()
        self._last_callback_attempt_retry_count = Number()
        self._last_successful_callback = Timestamp()

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None
        self.__initialized = True

    @property
    def last_callback_attempt(self):
        return self._last_callback_attempt.value

    @last_callback_attempt.setter
    def last_callback_attempt(self, value):
        self._last_callback_attempt.value = value

    @property
    def last_callback_attempt_retry_count(self):
        return self._last_callback_attempt_retry_count.value

    @last_callback_attempt_retry_count.setter
    def last_callback_attempt_retry_count(self, value):
        self._last_callback_attempt_retry_count.value = value

    @property
    def last_successful_callback(self):
        return self._last_successful_callback.value

    @last_successful_callback.setter
    def last_successful_callback(self, value):
        self._last_successful_callback.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
