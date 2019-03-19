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

from .account import Account
from .group import Group
from .user_model import UserModel
from ..types import *
from ..util import serialize
from ..util import deserialize


class UserProfile(UserModel):

    """Smartsheet UserProfile data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the UserProfile model."""
        super(UserProfile, self).__init__(None, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._account = TypedObject(Account)
        self._groups = TypedList(Group)
        self._locale = String()
        self._time_zone = String()

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None
        self.__initialized = True

    @property
    def account(self):
        return self._account.value

    @account.setter
    def account(self, value):
        self._account.value = value

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, value):
        self._groups.load(value)

    @property
    def locale(self):
        return self._locale.value

    @locale.setter
    def locale(self, value):
        self._locale.value = value

    @property
    def time_zone(self):
        return self._time_zone.value

    @time_zone.setter
    def time_zone(self, value):
        self._time_zone.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
