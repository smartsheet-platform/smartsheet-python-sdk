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
from datetime import datetime
from dateutil.parser import parse
import logging
import six
import json


class WebhookStats(object):

    """Smartsheet WebhookStats data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the WebhookStats model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._last_callback_attempt_retry_count = None
        self._last_callback_attempt = None
        self._last_successful_callback = None

        if props:
            # account for alternate variable names from raw API response
            if 'lastCallbackAttemptRetryCount' in props:
                self.last_callback_attempt_retry_count = props['lastCallbackAttemptRetryCount']
            if 'last_callback_attempt_retry_count' in props:
                self.last_callback_attempt_retry_count = props['last_callback_attempt_retry_count']
            if 'lastCallbackAttempt' in props:
                self.last_callback_attempt = props['lastCallbackAttempt']
            if 'last_callback_attempt' in props:
                self.last_callback_attempt = props['last_callback_attempt']
            if 'lastSuccessfulCallback' in props:
                self.last_successful_callback = props['lastSuccessfulCallback']
            if 'last_successful_callback' in props:
                self.last_successful_callback = props['last_successful_callback']

        # requests package Response object
        self.request_response = None
        self.__initialized = True

    @property
    def last_callback_attempt_retry_count(self):
        return self._last_callback_attempt_retry_count

    @last_callback_attempt_retry_count.setter
    def last_callback_attempt_retry_count(self, value):
        if isinstance(value, six.integer_types):
            self._last_callback_attempt_retry_count = value

    @property
    def last_callback_attempt(self):
        return self._last_callback_attempt

    @last_callback_attempt.setter
    def last_callback_attempt(self, value):
        if isinstance(value, datetime):
            self._last_callback_attempt = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._last_callback_attempt = value

    @property
    def last_successful_callback(self):
        return self._last_successful_callback

    @last_successful_callback.setter
    def last_successful_callback(self, value):
        if isinstance(value, datetime):
            self._last_successful_callback = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._last_successful_callback = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'lastCallbackAttemptRetryCount': prep(self._last_callback_attempt_retry_count),
            'lastCallbackAttempt': prep(self._last_callback_attempt),
            'lastSuccessfulCallback': prep(self._last_successful_callback)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())