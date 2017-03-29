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

class Source(object):

    """Smartsheet Source data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Source model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self.allowed_values = {
            '_type': [
                'sheet',
                'template']}

        self.__id = None
        self.__type = None

        if props:
            # account for alternate variable names from raw API response
            # read only
            if 'id' in props:
                self._id = props['id']
            # read only
            if 'type' in props:
                self._type = props['type']
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        elif key == 'type':
            return self._type
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
    def _type(self):
        return self.__type

    @_type.setter
    def _type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Source`_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['_type']))
            self.__type = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'id': prep(self.__id),
            'type': prep(self.__type)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
