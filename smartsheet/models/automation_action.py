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

from .enums import AutomationActionFrequency, AutomationActionType
from .recipient import Recipient
from ..types import *
from ..util import serialize
from ..util import deserialize


class AutomationAction(object):

    """Smartsheet AutomationAction data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the AutomationAction model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._frequency = EnumeratedValue(AutomationActionFrequency)
        self._include_all_columns = Boolean()
        self._include_attachments = Boolean()
        self._include_discussions = Boolean()
        self._included_column_ids = TypedList(six.integer_types)
        self._message = String()
        self._notify_all_shared_users = Boolean()
        self._recipient_column_ids = TypedList(six.integer_types)
        self._recipients = TypedList(Recipient)
        self._subject = String()
        self._type_ = EnumeratedValue(AutomationActionType)

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None
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
            super(AutomationAction, self).__setattr__(key, value)

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency.set(value)

    @property
    def include_all_columns(self):
        return self._include_all_columns.value

    @include_all_columns.setter
    def include_all_columns(self, value):
        self._include_all_columns.value = value

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
    def included_column_ids(self):
        return self._included_column_ids

    @included_column_ids.setter
    def included_column_ids(self, value):
        self._included_column_ids.load(value)

    @property
    def message(self):
        return self._message.value

    @message.setter
    def message(self, value):
        self._message.value = value

    @property
    def notify_all_shared_users(self):
        return self._notify_all_shared_users.value

    @notify_all_shared_users.setter
    def notify_all_shared_users(self, value):
        self._notify_all_shared_users.value = value

    @property
    def recipient_column_ids(self):
        return self._recipient_column_ids

    @recipient_column_ids.setter
    def recipient_column_ids(self, value):
        self._recipient_column_ids.load(value)

    @property
    def recipients(self):
        return self._recipients

    @recipients.setter
    def recipients(self, value):
        self._recipients.load(value)

    @property
    def subject(self):
        return self._subject.value

    @subject.setter
    def subject(self, value):
        self._subject.value = value

    @property
    def type_(self):
        return self._type_

    @type_.setter
    def type_(self, value):
        self._type_.set(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
