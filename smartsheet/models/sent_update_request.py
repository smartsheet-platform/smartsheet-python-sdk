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

from .enums import UpdateRequestStatus
from .user import User
from .recipient import Recipient
from ..util import serialize
from ..util import deserialize
from ..types import *


class SentUpdateRequest(object):
    """Smartsheet SentUpdateRequest data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SentUpdateRequest model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._column_ids = TypedList(six.integer_types)
        self._id_ = Number()
        self._include_attachments = Boolean()
        self._include_discussions = Boolean()
        self._message = String()
        self._row_ids = TypedList(six.integer_types)
        self._sent_at = Timestamp()
        self._sent_by = TypedObject(User)
        self._sent_to = TypedObject(Recipient)
        self._status = EnumeratedValue(UpdateRequestStatus)
        self._subject = String()
        self._update_request_id = Number()

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
            super(SentUpdateRequest, self).__setattr__(key, value)

    @property
    def column_ids(self):
        return self._column_ids

    @column_ids.setter
    def column_ids(self, value):
        self._column_ids.load(value)

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def include_attachments(self):
        return self._include_attachments.value

    @include_attachments.setter
    def include_attachments(self, value):
        self._include_attachments.value = value

    @property
    def include_discussions(self):
        return self._include_discussions.value

    @include_discussions.setter
    def include_discussions(self, value):
        self._include_discussions.value = value

    @property
    def message(self):
        return self._message.value

    @message.setter
    def message(self, value):
        self._message.value = value

    @property
    def row_ids(self):
        return self._row_ids

    @row_ids.setter
    def row_ids(self, value):
        self._row_ids.load(value)

    @property
    def sent_at(self):
        return self._sent_at.value

    @sent_at.setter
    def sent_at(self, value):
        self._sent_at.value = value

    @property
    def sent_by(self):
        return self._sent_by.value

    @sent_by.setter
    def sent_by(self, value):
        self._sent_by.value = value

    @property
    def sent_to(self):
        return self._sent_to.value

    @sent_to.setter
    def sent_to(self, value):
        self._sent_to.value = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status.set(value)

    @property
    def subject(self):
        return self._subject.value

    @subject.setter
    def subject(self, value):
        self._subject.value = value

    @property
    def update_request_id(self):
        return self._update_request_id.value

    @update_request_id.setter
    def update_request_id(self, value):
        self._update_request_id.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
