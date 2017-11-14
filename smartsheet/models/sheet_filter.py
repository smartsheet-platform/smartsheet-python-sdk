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
from .sheet_filter_details import SheetFilterDetails
import json
import six

class SheetFilter(object):

    """Smartsheet SheetFilter data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SheetFilter model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self.allowed_values = {
            '_filter_type': [
                'ADHOC',
                'PERSONAL',
                'SHARED']}

        self.__id = None
        self._name = None
        self._filter_type = None
        self._query = None

        if props:
            # account for alternate variable names from raw API response
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'name' in props:
                self.name = props['name']
            if 'filterType' in props:
                self.filter_type = props['filterType']
            if 'filter_type' in props:
                self.filter_type = props['filter_type']
            if 'query' in props:
                self.query = props['query']
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, six.string_types):
            self._name = value

    @property
    def filter_type(self):
        return self._filter_type

    @filter_type.setter
    def filter_type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['_filter_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Filter`_filter_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['_filter_type']))
            self._filter_type = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        if isinstance(value, SheetFilterDetails):
            self._query = value
        elif isinstance(value, dict):
            self._query = SheetFilterDetails(value, self._base)

    def to_dict(self, op_id=None, method=None):
        obj = {
            'id': prep(self.__id),
            'name': prep(self._name),
            'filterType': prep(self._filter_type),
            'query': prep(self._query)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
