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

class GroupMember(object):

    """Smartsheet GroupMember data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the GroupMember model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self._email = None
        self._first_name = None
        self.__id = None
        self._last_name = None
        self._name = None

        if props:
            # account for alternate variable names from raw API response
            if 'email' in props:
                self.email = props['email']
            if 'firstName' in props:
                self.first_name = props['firstName']
            if 'first_name' in props:
                self.first_name = props['first_name']
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'lastName' in props:
                self.last_name = props['lastName']
            if 'last_name' in props:
                self.last_name = props['last_name']
            if 'name' in props:
                self.name = props['name']
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if isinstance(value, six.string_types):
            self._email = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if isinstance(value, six.string_types):
            self._first_name = value

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if isinstance(value, six.string_types):
            self._last_name = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, six.string_types):
            self._name = value

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'email': prep(self._email),
            'firstName': prep(self._first_name),
            'id': prep(self.__id),
            'lastName': prep(self._last_name),
            'name': prep(self._name)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'create_group':
            permitted = ['email']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
