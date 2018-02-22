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
from .user import User
from .schedule import Schedule
from ..types import *
from ..util import serialize
from ..util import deserialize


class UpdateRequest(MultiRowEmail):

    """Smartsheet UpdateRequest data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the UpdateRequest model."""
        super(UpdateRequest, self).__init__(None, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._created_at = Timestamp()
        self._id_ = Number()
        self._modified_at = Timestamp()
        self._schedule = TypedObject(Schedule)
        self._sent_by = TypedObject(User)

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None
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
            super(UpdateRequest, self).__setattr__(key, value)

    @property
    def created_at(self):
        return self._created_at.value

    @created_at.setter
    def created_at(self, value):
        self._created_at.value = value

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def modified_at(self):
        return self._modified_at.value

    @modified_at.setter
    def modified_at(self, value):
        self._modified_at.value = value

    @property
    def schedule(self):
        return self._schedule.value

    @schedule.setter
    def schedule(self, value):
        self._schedule.value = value

    @property
    def sent_by(self):
        return self._sent_by.value

    @sent_by.setter
    def sent_by(self, value):
        self._sent_by.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
