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

class Currency(object):

    """Smartsheet Currency data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Currency model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self.allowed_values = {
            'code': [
                'none',
                'ARS',
                'AUD',
                'BRL',
                'CAD',
                'CLP',
                'EUR',
                'GBP',
                'ILS',
                'INR',
                'JPY',
                'MXN',
                'RUB',
                'USD',
                'ZAR',
                'CHF',
                'CNY',
                'DKK',
                'HKD',
                'KRW',
                'NOK',
                'NZD',
                'SEK',
                'SGD']}

        self._code = None
        self._symbol = None

        if props:
            if 'code' in props:
                self.code = props['code']
            if 'symbol' in props:
                self.symbol = props['symbol']

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['code']:
                raise ValueError(
                    ("`{0}` is an invalid value for Currency`code`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['code']))
            self._code = value

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        if isinstance(value, six.string_types):
            self._symbol = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'code': prep(self._code),
            'symbol': prep(self._symbol)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
