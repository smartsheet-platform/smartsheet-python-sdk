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

from .enums import AccessLevel, ShareScope, ShareType
from ..types import *
from ..util import serialize
from ..util import deserialize


class Share(object):

    """Smartsheet Share data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Share model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._access_level = EnumeratedValue(AccessLevel)
        self._cc_me = Boolean()
        self._created_at = Timestamp()
        self._email = String()
        self._group_id = Number()
        self._id_ = String()
        self._message = String()
        self._modified_at = Timestamp()
        self._name = String()
        self._scope = EnumeratedValue(ShareScope)
        self._subject = String()
        self._type_ = EnumeratedValue(ShareType)
        self._user_id = Number()

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self.id_
        elif key == 'type':
            return self.type_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'id':
            self.id_ = value
        elif key == 'type':
            self.type_ = value
        else:
            super(Share, self).__setattr__(key, value)

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        self._access_level.set(value)

    @property
    def cc_me(self):
        return self._cc_me.value

    @cc_me.setter
    def cc_me(self, value):
        self._cc_me.value = value

    @property
    def created_at(self):
        return self._created_at.value

    @created_at.setter
    def created_at(self, value):
        self._created_at.value = value

    @property
    def email(self):
        return self._email.value

    @email.setter
    def email(self, value):
        self._email.value = value

    @property
    def group_id(self):
        return self._group_id.value

    @group_id.setter
    def group_id(self, value):
        self._group_id.value = value

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def message(self):
        return self._message.value

    @message.setter
    def message(self, value):
        self._message.value = value

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
        return self._scope

    @scope.setter
    def scope(self, value):
        self._scope.set(value)

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
