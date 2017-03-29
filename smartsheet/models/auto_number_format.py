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

class AutoNumberFormat(object):

    """Smartsheet AutoNumberFormat data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the AutoNumberFormat model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._fill = None
        self._prefix = None
        self._starting_number = None
        self._suffix = None

        if props:
            # account for alternate variable names from raw API response
            if 'fill' in props:
                self.fill = props['fill']
            if 'prefix' in props:
                self.prefix = props['prefix']
            if 'startingNumber' in props:
                self.starting_number = props['startingNumber']
            if 'starting_number' in props:
                self.starting_number = props['starting_number']
            if 'suffix' in props:
                self.suffix = props['suffix']

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, value):
        if isinstance(value, six.string_types):
            self._fill = value

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        if isinstance(value, six.string_types):
            self._prefix = value

    @property
    def starting_number(self):
        return self._starting_number

    @starting_number.setter
    def starting_number(self, value):
        if isinstance(value, six.integer_types):
            self._starting_number = value

    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        if isinstance(value, six.string_types):
            self._suffix = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'fill': prep(self._fill),
            'prefix': prep(self._prefix),
            'startingNumber': prep(self._starting_number),
            'suffix': prep(self._suffix)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
