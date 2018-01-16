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

from .multi_row_email import MultiRowEmail
from ..util import prep
from .user import User
from .schedule import Schedule
from datetime import datetime
from dateutil.parser import parse
import json
import six


class UpdateRequest(MultiRowEmail):

    """Smartsheet UpdateRequest data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the UpdateRequest model."""
        super(UpdateRequest, self).__init__(props, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._created_at = None
        self.__id = None
        self._modified_at = None
        self._schedule = None
        self._sent_by = None

        if props:
            # account for alternate variable names from raw API response
            if 'createdAt' in props:
                self.created_at = props['createdAt']
            if 'created_at' in props:
                self.created_at = props['created_at']
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'modifiedAt' in props:
                self.modified_at = props['modifiedAt']
            if 'modified_at' in props:
                self.modified_at = props['modified_at']
            if 'schedule' in props:
                self.schedule = props['schedule']
            if 'sentBy' in props:
                self.sent_by = props['sentBy']
            if 'sent_by' in props:
                self.sent_by = props['sent_by']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        if isinstance(value, datetime):
            self._created_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._created_at = value

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

    @property
    def modified_at(self):
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value):
        if isinstance(value, datetime):
            self._modified_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._modified_at = value

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, value):
        if isinstance(value, Schedule):
            self._schedule = value
        else:
            if isinstance(value, dict):
                self._schedule = Schedule(value, self._base)

    @property
    def sent_by(self):
        return self._sent_by

    @sent_by.setter
    def sent_by(self, value):
        if isinstance(value, User):
            self._sent_by = value
        else:
            if isinstance(value, dict):
                self._sent_by = User(value, self._base)

    def to_dict(self, op_id=None, method=None):
        parent_obj = super(UpdateRequest, self).to_dict(op_id, method)
        obj = {
            'createdAt': prep(self._created_at),
            'id': prep(self.__id),
            'modifiedAt': prep(self._modified_at),
            'schedule': prep(self._schedule),
            'sentBy': prep(self._sent_by)}
        combo = parent_obj.copy()
        combo.update(obj)
        return combo

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
