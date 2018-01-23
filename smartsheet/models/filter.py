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

from .criteria import Criteria
from ..types import TypedList
from ..util import serialize
from ..util import deserialize


class Filter(object):

    """Smartsheet Filter data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Filter model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            '_type': [
                'LIST',
                'CUSTOM']}

        self._criteria = TypedList(Criteria)
        self._exclude_selected = None
        self._type_ = None
        self._values = TypedList(str)

        if props:
            deserialize(self, props)

        self.__initialized = True

    def __getattr__(self, key):
        if key == 'type':
            return self.type_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'type':
            self.type_ = value
        else:
            super(Filter, self).__setattr__(key, value)

    @property
    def criteria(self):
        return self._criteria

    @criteria.setter
    def criteria(self, value):
        self._criteria.load(value)

    @property
    def exclude_selected(self):
        return self._exclude_selected

    @exclude_selected.setter
    def exclude_selected(self, value):
        if isinstance(value, bool):
            self._exclude_selected = value

    @property
    def type_(self):
        return self._type_

    @type_.setter
    def type_(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Filter`_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['_type']))
            self._type_ = value

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
