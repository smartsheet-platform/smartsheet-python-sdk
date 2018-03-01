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

from .automation_action import AutomationAction
from .enums import AutomationRuleDisabledReason
from .user import User
from ..types import *
from ..util import serialize
from ..util import deserialize


class AutomationRule(object):

    """Smartsheet AutomationRule data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the AutomationRule model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._action = TypedObject(AutomationAction)
        self._created_at = Timestamp()
        self._created_by = TypedObject(User)
        self._disabled_reason = EnumeratedValue(AutomationRuleDisabledReason)
        self._disabled_reason_text = String()
        self._enabled = Boolean()
        self._id_ = Number()
        self._modified_at = Timestamp()
        self._modified_by = TypedObject(User)
        self._name = String()
        self._user_can_modify = Boolean()

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
            super(AutomationRule, self).__setattr__(key, value)

    @property
    def action(self):
        return self._action.value

    @action.setter
    def action(self, value):
        self._action.value = value

    @property
    def created_at(self):
        return self._created_at.value

    @created_at.setter
    def created_at(self, value):
        self._created_at.value = value

    @property
    def created_by(self):
        return self._created_by.value

    @created_by.setter
    def created_by(self, value):
        self._created_by.value = value

    @property
    def disabled_reason(self):
        return self._disabled_reason

    @disabled_reason.setter
    def disabled_reason(self, value):
        self._disabled_reason.set(value)

    @property
    def disabled_reason_text(self):
        return self._disabled_reason_text.value

    @disabled_reason_text.setter
    def disabled_reason_text(self, value):
        self._disabled_reason_text.value = value

    @property
    def enabled(self):
        return self._enabled.value

    @enabled.setter
    def enabled(self, value):
        self._enabled.value = value

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
    def modified_by(self):
        return self._modified_by.value

    @modified_by.setter
    def modified_by(self, value):
        self._modified_by.value = value

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._name.value = value

    @property
    def user_can_modify(self):
        return self._user_can_modify.value

    @user_can_modify.setter
    def user_can_modify(self, value):
        self._user_can_modify.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
