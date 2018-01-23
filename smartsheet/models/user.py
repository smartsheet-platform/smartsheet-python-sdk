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

from .alternate_email import AlternateEmail
from ..types import TypedList
from ..util import serialize
from ..util import deserialize
from datetime import datetime
from dateutil.parser import parse


class User(object):

    """Smartsheet User data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the User model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'status': [
                'ACTIVE',
                'PENDING',
                'DECLINED']}

        self._admin = None
        self._alternate_emails = TypedList(AlternateEmail)
        self._custom_welcome_screen_viewed = None
        self._email = None
        self._first_name = None
        self._group_admin = None
        self._id_ = None
        self._last_login = None
        self._last_name = None
        self._licensed_sheet_creator = None
        self._name = None
        self._resource_viewer = None
        self._sheet_count = None
        self._status = None

        if props:
            deserialize(self, props)

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
            super(User, self).__setattr__(key, value)

    @property
    def admin(self):
        return self._admin

    @admin.setter
    def admin(self, value):
        if isinstance(value, bool):
            self._admin = value

    @property
    def alternate_emails(self):
        return self._alternate_emails

    @alternate_emails.setter
    def alternate_emails(self, value):
        self._alternate_emails.load(value)

    @property
    def custom_welcome_screen_viewed(self):
        return self._custom_welcome_screen_viewed

    @custom_welcome_screen_viewed.setter
    def custom_welcome_screen_viewed(self, value):
        if isinstance(value, datetime):
            self._custom_welcome_screen_viewed = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._custom_welcome_screen_viewed = value

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
    def last_login(self):
        return self._last_login

    @last_login.setter
    def last_login(self, value):
        if isinstance(value, datetime):
            self._last_login = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._last_login = value

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
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, six.string_types):
            self._name = value

    @property
    def resource_viewer(self):
        return self._resource_viewer

    @resource_viewer.setter
    def resource_viewer(self, value):
        if isinstance(value, bool):
            self._resource_viewer = value

    @property
    def sheet_count(self):
        return self._sheet_count

    @sheet_count.setter
    def sheet_count(self, value):
        if isinstance(value, six.integer_types):
            self._sheet_count = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['status']:
                raise ValueError(
                    ("`{0}` is an invalid value for User`status`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['status']))
            self._status = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
