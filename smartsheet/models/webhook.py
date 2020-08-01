# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2017 - 2020 Smartsheet.com, Inc.
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

from .webhook_stats import WebhookStats
from .webhook_subscope import WebhookSubscope
from ..types import *
from ..util import serialize
from ..util import deserialize


class Webhook(object):

    """Smartsheet Webhook data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Webhook model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'scope': [
                'sheet']}

        self._api_client_id = String()
        self._api_client_name = String()
        self._callback_url = String()
        self._created_at = Timestamp()
        self._disabled_details = String()
        self._enabled = Boolean()
        self._events = TypedList(six.string_types)
        self._id_ = Number()
        self._modified_at = Timestamp()
        self._name = String()
        self._scope = String(
            accept=self.allowed_values['scope']
        )
        self._scope_object_id = Number()
        self._shared_secret = String()
        self._stats = TypedObject(WebhookStats)
        self._status = String()
        self._version = Number()
        self._subscope = TypedObject(WebhookSubscope)

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
        return self._api_client_id.value

    @api_client_id.setter
    def api_client_id(self, value):
        self._api_client_id.value = value

    @property
    def api_client_name(self):
        return self._api_client_name.value

    @api_client_name.setter
    def api_client_name(self, value):
        self._api_client_name.value = value

    @property
    def callback_url(self):
        return self._callback_url.value

    @callback_url.setter
    def callback_url(self, value):
        self._callback_url.value = value

    @property
    def created_at(self):
        return self._created_at.value

    @created_at.setter
    def created_at(self, value):
        self._created_at.value = value

    @property
    def disabled_details(self):
        return self._disabled_details.value

    @disabled_details.setter
    def disabled_details(self, value):
        self._disabled_details.value = value

    @property
    def enabled(self):
        return self._enabled.value

    @enabled.setter
    def enabled(self, value):
        self._enabled.value = value

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, value):
        self._events.load(value)

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
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._name.value = value

    @property
    def scope(self):
        return self._scope.value

    @scope.setter
    def scope(self, value):
        self._scope.value = value

    @property
    def scope_object_id(self):
        return self._scope_object_id.value

    @scope_object_id.setter
    def scope_object_id(self, value):
        self._scope_object_id.value = value

    @property
    def shared_secret(self):
        return self._shared_secret.value

    @shared_secret.setter
    def shared_secret(self, value):
        self._shared_secret.value = value

    @property
    def stats(self):
        return self._stats.value

    @stats.setter
    def stats(self, value):
        self._stats.value = value

    @property
    def status(self):
        return self._status.value

    @status.setter
    def status(self, value):
        self._status.value = value

    @property
    def subscope(self):
        return self._subscope.value

    @subscope.setter
    def subscope(self, value):
        self._subscope.value = value

    @property
    def version(self):
        return self._version.value

    @version.setter
    def version(self, value):
        self._version.value = value

    @property
    def subscope(self):
        return self._subscope.value

    @subscope.setter
    def subscope(self, value):
        self._subscope.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
