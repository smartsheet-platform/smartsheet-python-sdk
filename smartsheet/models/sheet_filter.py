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

import six
import json

from ..util import serialize
from ..util import deserialize
from .sheet_filter_details import SheetFilterDetails


class SheetFilter(object):

    """Smartsheet SheetFilter data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SheetFilter model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            '_filter_type': [
                'ADHOC',
                'PERSONAL',
                'SHARED']}

        self._filter_type = None
        self._id_ = None
        self._name = None
        self._query = None

        if props:
            deserialize(self, props)

        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self.id_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'id':
            self.id_ = value
        else:
            super(__class__, self).__setattr__(key, value)

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
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, value):
        if isinstance(value, six.integer_types):
            self._id_ = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, six.string_types):
            self._name = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        if isinstance(value, SheetFilterDetails):
            self._query = value
        elif isinstance(value, dict):
            self._query = SheetFilterDetails(value, self._base)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
