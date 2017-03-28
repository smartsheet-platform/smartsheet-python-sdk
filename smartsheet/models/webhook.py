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

from ..types import TypedList
from ..util import prep
from .webhook_stats import WebhookStats
from datetime import datetime
from dateutil.parser import parse
import logging
import six
import json


class Webhook(object):

    """Smartsheet Webhook data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Webhook model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self.__id = None
        self._name = None
        self._api_client_id = None
        self._api_client_name = None
        self._scope = None
        self._scope_object_id = None
        self._events = TypedList(six.string_types)
        self._callback_url = None
        self._shared_secret = None
        self._enabled = None
        self._status = None
        self._disabled_details = None
        self._version = None
        self._stats = None
        self._created_at = None
        self._modified_at = None

        if props:
            # account for alternate variable names from raw API response
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'name' in props:
                self.name = props['name']
            if 'apiClientId' in props:
                self.api_client_id = props['apiClientId']
            if 'api_client_id' in props:
                self.api_client_id = props['api_client_id']
            if 'apiClientName' in props:
                self.api_client_name = props['apiClientName']
            if 'api_client_name' in props:
                self.api_client_name = props['api_client_name']
            if 'scope' in props:
                self.scope = props['scope']
            if 'scopeObjectId' in props:
                self.scope_object_id = props['scopeObjectId']
            if 'scope_object_id' in props:
                self.scope_object_id = props['scope_object_id']
            if 'events' in props:
                self.events = props['events']
            if 'callbackUrl' in props:
                self.callback_url = props['callbackUrl']
            if 'callback_url' in props:
                self.callback_url = props['callback_url']
            if 'sharedSecrect' in props:
                self.shared_secret = props['sharedSecrect']
            if 'shared_secrect' in props:
                self.shared_secret = props['shared_secrect']
            if 'enabled' in props:
                self.enabled = props['enabled']
            if 'status' in props:
                self.status = props['status']
            if 'disabledDetails' in props:
                self.disabled_details = props['disabledDetails']
            if 'disabled_details' in props:
                self.disabled_details = props['disabled_details']
            if 'version' in props:
                self.version = props['version']
            if 'stats' in props:
                self.stats = props['stats']
            if 'createdAt' in props:
                self.created_at = props['createdAt']
            if 'created_at' in props:
                self.created_at = props['created_at']
            if 'modifiedAt' in props:
                self.modified_at = props['modifiedAt']
            if 'modified_at' in props:
                self.modified_at = props['modified_at']

        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, six.string_types):
            self._name = value

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
    def events(self):
        return self._events

    @events.setter
    def events(self, value):
        if isinstance(value, list):
            self._events.purge()
            self._events.extend([
                (six.string_types(x, self._base)
                 if not isinstance(x, six.string_types) else x) for x in value
             ])
        elif isinstance(value, TypedList):
            self._events.purge()
            self._events = value.to_list()
        elif isinstance(value, six.string_types):
            self._events.purge()
            self._events.append(value)

    @property
    def callback_url(self):
        return self._callback_url

    @callback_url.setter
    def callback_url(self, value):
        if isinstance(value, six.string_types):
            self._callback_url = value

    @property
    def shared_secret(self):
        return self._shared_secret

    @shared_secret.setter
    def shared_secret(self, value):
        if isinstance(value, six.string_types):
            self._shared_secret = value

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if isinstance(value, bool):
            self._enabled = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, six.string_types):
            self._status = value

    @property
    def disabled_details(self):
        return self._disabled_details

    @disabled_details.setter
    def disabled_details(self, value):
        if isinstance(value, six.string_types):
            self._disabled_details = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if isinstance(value, six.integer_types):
            self._version = value

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
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'id': prep(self.__id),
            'name': prep(self._name),
            'apiClientId': prep(self._api_client_id),
            'apiClientName': prep(self._api_client_name),
            'scope': prep(self._scope),
            'scopeObjectId': prep(self._scope_object_id),
            'events': prep(self._events),
            'callbackUrl': prep(self._callback_url),
            'sharedSecret':prep(self._shared_secret),
            'enabled': prep(self._enabled),
            'status': prep(self._status),
            'disabledDetails': prep(self._disabled_details),
            'version': prep(self._version),
            'stats': prep(self._stats),
            'createdAt': prep(self._created_at),
            'modifiedAt': prep(self._modified_at)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'create_webhook':
            permitted = ['name','callbackUrl','scope','scopeObjectId','events','version']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]
        if self.pre_request_filter == 'update_webhook':
            permitted = ['name','events','callbackUrl','enabled','version']
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