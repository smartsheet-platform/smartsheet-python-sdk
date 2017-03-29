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

class AlternateEmail(object):

    """Smartsheet AlternateEmail data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the AlternateEmail model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self._confirmed = False
        self._email = None
        self.__id = None

        if props:
            # account for alternate variable names from raw API response
            if 'confirmed' in props:
                self.confirmed = props['confirmed']
            if 'email' in props:
                self.email = props['email']
            # read only
            if 'id' in props:
                self._id = props['id']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

    @property
    def confirmed(self):
        return self._confirmed

    @confirmed.setter
    def confirmed(self, value):
        if isinstance(value, bool):
            self._confirmed = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if isinstance(value, six.string_types):
            self._email = value

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'confirmed': prep(self._confirmed),
            'email': prep(self._email),
            'id': prep(self.__id)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'add_alternate_email':
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
