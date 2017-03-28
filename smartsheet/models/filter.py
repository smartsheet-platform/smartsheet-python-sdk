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

from .criteria import Criteria
from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class Filter(object):

    """Smartsheet Filter data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Filter model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self.allowed_values = {
            '_type': [
                'LIST',
                'CUSTOM']}

        self._criteria = TypedList(Criteria)
        self._exclude_selected = None
        self.__type = None
        self._values = TypedList(str)

        if props:
            # account for alternate variable names from raw API response
            if 'criteria' in props:
                self.criteria = props['criteria']
            if 'excludeSelected' in props:
                self.exclude_selected = props['excludeSelected']
            if 'exclude_selected' in props:
                self.exclude_selected = props[
                    'exclude_selected']
            if 'type' in props:
                self._type = props['type']
            if '_type' in props:
                self._type = props['_type']
            if 'values' in props:
                self.values = props['values']
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'type':
            return self._type
        else:
            raise AttributeError(key)

    @property
    def criteria(self):
        return self._criteria

    @criteria.setter
    def criteria(self, value):
        if isinstance(value, list):
            self._criteria.purge()
            self._criteria.extend([
                (Criteria(x, self._base)
                 if not isinstance(x, Criteria) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._criteria.purge()
            self._criteria = value.to_list()
        elif isinstance(value, Criteria):
            self._criteria.purge()
            self._criteria.append(value)

    @property
    def exclude_selected(self):
        return self._exclude_selected

    @exclude_selected.setter
    def exclude_selected(self, value):
        if isinstance(value, bool):
            self._exclude_selected = value

    @property
    def _type(self):
        return self.__type

    @_type.setter
    def _type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Filter`_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['_type']))
            self.__type = value

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        if isinstance(value, list):
            self._values.purge()
            self._values.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._values.purge()
            self._values = value.to_list()
        elif isinstance(value, str):
            self._values.purge()
            self._values.append(value)

    def to_dict(self, op_id=None, method=None):
        obj = {
            'criteria': prep(self._criteria),
            'excludeSelected': prep(self._exclude_selected),
            'type': prep(self.__type),
            'values': prep(self._values)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
