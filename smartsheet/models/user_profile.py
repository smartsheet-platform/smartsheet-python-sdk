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

import six
import json

from .account import Account
from ..util import serialize
from ..util import deserialize


class UserProfile(object):

    """Smartsheet UserProfile data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the UserProfile model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'status': [
                'ACTIVE',
                'PENDING',
                'DECLINED']}

        self._account = None
        self._admin = None
        self._email = None
        self._first_name = None
        self._group_admin = None
        self._id_ = None
        self._last_name = None
        self._licensed_sheet_creator = None
        self._locale = None
        self._resource_viewer = None
        self._status = None
        self._time_zone = None

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
            super(__class__, self).__setattr__(key, value)

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, value):
        if isinstance(value, Account):
            self._account = value
        else:
            self._account = Account(value, self._base)

    @property
    def admin(self):
        return self._admin

    @admin.setter
    def admin(self, value):
        if isinstance(value, bool):
            self._admin = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if isinstance(value, six.string_types):
            self._email = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if isinstance(value, six.string_types):
            self._first_name = value

    @property
    def group_admin(self):
        return self._group_admin

    @group_admin.setter
    def group_admin(self, value):
        if isinstance(value, bool):
            self._group_admin = value

    @property
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, value):
        if isinstance(value, six.integer_types):
            self._id_ = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if isinstance(value, six.string_types):
            self._last_name = value

    @property
    def licensed_sheet_creator(self):
        return self._licensed_sheet_creator

    @licensed_sheet_creator.setter
    def licensed_sheet_creator(self, value):
        if isinstance(value, bool):
            self._licensed_sheet_creator = value

    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, value):
        if isinstance(value, six.string_types):
            self._locale = value

    @property
    def resource_viewer(self):
        return self._resource_viewer

    @resource_viewer.setter
    def resource_viewer(self, value):
        if isinstance(value, bool):
            self._resource_viewer = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['status']:
                raise ValueError(
                    ("`{0}` is an invalid value for UserProfile`status`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['status']))
            self._status = value

    @property
    def time_zone(self):
        return self._time_zone

    @time_zone.setter
    def time_zone(self, value):
        if isinstance(value, six.string_types):
            self._time_zone = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
