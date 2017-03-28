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

from ..util import prep
from datetime import datetime
from dateutil.parser import parse
import json
import logging
import six

class Share(object):

    """Smartsheet Share data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Share model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self.allowed_values = {
            'access_level': [
                'VIEWER',
                'EDITOR',
                'EDITOR_SHARE',
                'ADMIN',
                'OWNER'],
            '_type': [
                'USER',
                'GROUP']}

        self._access_level = None
        self._cc_me = None
        self._created_at = None
        self._email = None
        self._group_id = None
        self.__id = None
        self._message = None
        self._modified_at = None
        self._name = None
        self._scope = None
        self._subject = None
        self.__type = None
        self._user_id = None

        if props:
            # account for alternate variable names from raw API response
            if 'accessLevel' in props:
                self.access_level = props['accessLevel']
            if 'access_level' in props:
                self.access_level = props['access_level']
            if 'ccMe' in props:
                self.cc_me = props['ccMe']
            if 'cc_me' in props:
                self.cc_me = props['cc_me']
            if 'createdAt' in props:
                self.created_at = props['createdAt']
            if 'created_at' in props:
                self.created_at = props['created_at']
            if 'email' in props:
                self.email = props['email']
            if 'groupId' in props:
                self.group_id = props['groupId']
            if 'group_id' in props:
                self.group_id = props['group_id']
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'message' in props:
                self.message = props['message']
            if 'modifiedAt' in props:
                self.modified_at = props['modifiedAt']
            if 'modified_at' in props:
                self.modified_at = props['modified_at']
            if 'name' in props:
                self.name = props['name']
            if 'scope' in props:
                self.scope = props['scope']
            if 'subject' in props:
                self.subject = props['subject']
            if 'type' in props:
                self._type = props['type']
            if '_type' in props:
                self._type = props['_type']
            if 'userId' in props:
                self.user_id = props['userId']
            if 'user_id' in props:
                self.user_id = props['user_id']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        elif key == 'type':
            return self._type
        else:
            raise AttributeError(key)

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['access_level']:
                raise ValueError(
                    ("`{0}` is an invalid value for Share`access_level`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['access_level']))
            self._access_level = value

    @property
    def cc_me(self):
        return self._cc_me

    @cc_me.setter
    def cc_me(self, value):
        if isinstance(value, bool):
            self._cc_me = value

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
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if isinstance(value, six.string_types):
            self._email = value

    @property
    def group_id(self):
        return self._group_id

    @group_id.setter
    def group_id(self, value):
        if isinstance(value, six.integer_types):
            self._group_id = value

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.string_types):
            self.__id = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if isinstance(value, six.string_types):
            self._message = value

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
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        if isinstance(value, six.string_types):
            self._subject = value

    @property
    def _type(self):
        return self.__type

    @_type.setter
    def _type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Share`_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['_type']))
            self.__type = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if isinstance(value, six.integer_types):
            self._user_id = value

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'accessLevel': prep(self._access_level),
            'ccMe': prep(self._cc_me),
            'createdAt': prep(self._created_at),
            'email': prep(self._email),
            'groupId': prep(self._group_id),
            'id': prep(self.__id),
            'message': prep(self._message),
            'modifiedAt': prep(self._modified_at),
            'name': prep(self._name),
            'scope': prep(self._scope),
            'subject': prep(self._subject),
            'type': prep(self.__type),
            'userId': prep(self._user_id)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'share_sheet':
            permitted = ['email', 'groupId', 'accessLevel',
                         'subject', 'message', 'ccMe']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'share_sight':
            permitted = ['email', 'groupId', 'accessLevel',
                         'subject', 'message', 'ccMe']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'share_workspace':
            permitted = ['email', 'groupId', 'accessLevel',
                         'subject', 'message', 'ccMe']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'update_share':
            permitted = ['accessLevel']
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
