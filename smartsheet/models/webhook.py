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

from .webhook_stats import WebhookStats
from ..types import TypedList
from ..util import serialize
from ..util import deserialize
from datetime import datetime
from dateutil.parser import parse


class Webhook(object):

    """Smartsheet Webhook data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Webhook model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._api_client_id = None
        self._api_client_name = None
        self._callback_url = None
        self._created_at = None
        self._disabled_details = None
        self._enabled = None
        self._events = TypedList(six.string_types)
        self._id_ = None
        self._modified_at = None
        self._name = None
        self._scope = None
        self._scope_object_id = None
        self._shared_secret = None
        self._stats = None
        self._status = None
        self._version = None

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
            super(Webhook, self).__setattr__(key, value)

    @property
    def api_client_id(self):
        return self._api_client_id

    @api_client_id.setter
    def api_client_id(self, value):
        if isinstance(value, six.string_types):
            self._api_client_id = value

    @property
    def api_client_name(self):
        return self._api_client_name

    @api_client_name.setter
    def api_client_name(self, value):
        if isinstance(value, six.string_types):
            self._api_client_name = value

    @property
    def callback_url(self):
        return self._callback_url

    @callback_url.setter
    def callback_url(self, value):
        if isinstance(value, six.string_types):
            self._callback_url = value

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
    def disabled_details(self):
        return self._disabled_details

    @disabled_details.setter
    def disabled_details(self, value):
        if isinstance(value, six.string_types):
            self._disabled_details = value

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if isinstance(value, bool):
            self._enabled = value

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, value):
        self._events.load(value)

    @property
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, value):
        if isinstance(value, six.integer_types):
            self._id_ = value

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
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, six.string_types):
            self._name = value

    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self, value):
        if isinstance(value, six.string_types):
            self._scope = value

    @property
    def scope_object_id(self):
        return self._scope_object_id

    @scope_object_id.setter
    def scope_object_id(self, value):
        if isinstance(value, six.integer_types):
            self._scope_object_id = value

    @property
    def shared_secret(self):
        return self._shared_secret

    @shared_secret.setter
    def shared_secret(self, value):
        if isinstance(value, six.string_types):
            self._shared_secret = value

    @property
    def stats(self):
        return self._stats

    @stats.setter
    def stats(self, value):
        if isinstance(value, dict):
            self._stats = WebhookStats(value, self._base)
        if isinstance(value, WebhookStats):
            self._stats = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, six.string_types):
            self._status = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if isinstance(value, six.integer_types):
            self._version = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
