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

from .alternate_email import AlternateEmail
from ..types import *
from ..util import serialize
from ..util import deserialize


class UserModel(object):

    """Smartsheet UserModel data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the UserModel model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'status': [
                'ACTIVE',
                'PENDING',
                'DECLINED']}

        self._admin = Boolean()
        self._alternate_emails = TypedList(AlternateEmail)
        self._custom_welcome_screen_viewed = Timestamp()
        self._email = String()
        self._first_name = String()
        self._group_admin = Boolean()
        self._id_ = Number()
        self._last_login = Timestamp()
        self._last_name = String()
        self._licensed_sheet_creator = Boolean()
        self._resource_viewer = Boolean()
        self._sheet_count = Number()
        self._status = String(
            accept=self.allowed_values['status']
        )

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
            super(UserModel, self).__setattr__(key, value)

    @property
    def admin(self):
        return self._admin.value

    @admin.setter
    def admin(self, value):
        self._admin.value = value

    @property
    def alternate_emails(self):
        return self._alternate_emails

    @alternate_emails.setter
    def alternate_emails(self, value):
        self._alternate_emails.load(value)

    @property
    def custom_welcome_screen_viewed(self):
        return self._custom_welcome_screen_viewed.value

    @custom_welcome_screen_viewed.setter
    def custom_welcome_screen_viewed(self, value):
        self._custom_welcome_screen_viewed.value = value

    @property
    def email(self):
        return self._email.value

    @email.setter
    def email(self, value):
        self._email.value = value

    @property
    def first_name(self):
        return self._first_name.value

    @first_name.setter
    def first_name(self, value):
        self._first_name.value = value

    @property
    def group_admin(self):
        return self._group_admin.value

    @group_admin.setter
    def group_admin(self, value):
        self._group_admin.value = value

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def last_login(self):
        return self._last_login.value

    @last_login.setter
    def last_login(self, value):
        self._last_login.value = value

    @property
    def last_name(self):
        return self._last_name.value

    @last_name.setter
    def last_name(self, value):
        self._last_name.value = value

    @property
    def licensed_sheet_creator(self):
        return self._licensed_sheet_creator.value

    @licensed_sheet_creator.setter
    def licensed_sheet_creator(self, value):
        self._licensed_sheet_creator.value = value

    @property
    def resource_viewer(self):
        return self._resource_viewer.value

    @resource_viewer.setter
    def resource_viewer(self, value):
        self._resource_viewer.value = value

    @property
    def sheet_count(self):
        return self._sheet_count.value

    @sheet_count.setter
    def sheet_count(self, value):
        self._sheet_count.value = value

    @property
    def status(self):
        return self._status.value

    @status.setter
    def status(self, value):
        self._status.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
