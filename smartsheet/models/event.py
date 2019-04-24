# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2019 Smartsheet.com, Inc.
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

from .enums import EventObjectType, EventAction, EventSource
from ..types import *
from ..util import serialize
from ..util import deserialize


class Event(object):

    """Smartsheet Event data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Event model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._access_token_name = String()
        self._action = EnumeratedValue(EventAction)
        self._additional_details = None
        self._event_id = String()
        self._event_timestamp = None
        self._object_id = None
        self._object_type = EnumeratedValue(EventObjectType)
        self._request_user_id = Number()
        self._source = EnumeratedValue(EventSource)
        self._user_id = Number()

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        raise AttributeError(key)

    def __setattr__(self, key, value):
        super(Event, self).__setattr__(key, value)

    @property
    def access_token_name(self):
        return self._access_token_name.value

    @access_token_name.setter
    def access_token_name(self, value):
        self._access_token_name.value = value

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action.set(value)

    @property
    def additional_details(self):
        return self._additional_details

    @additional_details.setter
    def additional_details(self, value):
        self._additional_details = value

    @property
    def event_id(self):
        return self._event_id.value

    @event_id.setter
    def event_id(self, value):
        self._event_id.value = value

    @property
    def event_timestamp(self):
        if self._event_timestamp is not None:
            return self._event_timestamp.value
        else:
            return None

    @event_timestamp.setter
    def event_timestamp(self, value):
        if isinstance(value, six.string_types):
            self._event_timestamp = Timestamp()
        else:
            self._event_timestamp = Number()
        self._event_timestamp.value = value

    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        self._object_id = value

    @property
    def object_type(self):
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        self._object_type.set(value)

    @property
    def request_user_id(self):
        return self._request_user_id.value

    @request_user_id.setter
    def request_user_id(self, value):
        self._request_user_id.value = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source.set(value)

    @property
    def user_id(self):
        return self._user_id.value

    @user_id.setter
    def user_id(self, value):
        self._user_id.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
