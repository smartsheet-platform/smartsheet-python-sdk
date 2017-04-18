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

from ..types import TypedList
from ..util import prep
from datetime import datetime
from dateutil.parser import parse
from .alternate_email import AlternateEmail
import json
import logging
import six

class User(object):

    """Smartsheet User data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the User model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

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
        self.__id = None
        self._last_login = None
        self._last_name = None
        self._licensed_sheet_creator = None
        self._name = None
        self._resource_viewer = None
        self._sheet_count = None
        self._status = None

        if props:
            # account for alternate variable names from raw API response
            if 'admin' in props:
                self.admin = props['admin']
            if 'alternateEmails' in props:
                self.alternate_emails = props['alternateEmails']
            if 'alternate_emails' in props:
                self.alternate_emails = props['alternate_emails']
            if 'customWelcomeScreenViewed' in props:
                self.custom_welcome_screen_viewed = props['customWelcomeScreenViewed']
            if 'custom_welcome_screen_viewed' in props:
                self.custom_welcome_screen_viewed = props['custom_welcome_screen_viewed']
            if 'email' in props:
                self.email = props['email']
            if 'firstName' in props:
                self.first_name = props['firstName']
            if 'first_name' in props:
                self.first_name = props['first_name']
            if 'groupAdmin' in props:
                self.group_admin = props['groupAdmin']
            if 'group_admin' in props:
                self.group_admin = props['group_admin']
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'lastLogin' in props:
                self.last_login = props['lastLogin']
            if 'last_login' in props:
                self.last_login = props['last_login']
            if 'lastName' in props:
                self.last_name = props['lastName']
            if 'last_name' in props:
                self.last_name = props['last_name']
            if 'licensedSheetCreator' in props:
                self.licensed_sheet_creator = props[
                    'licensedSheetCreator']
            if 'licensed_sheet_creator' in props:
                self.licensed_sheet_creator = props[
                    'licensed_sheet_creator']
            if 'name' in props:
                self.name = props['name']
            if 'resourceViewer' in props:
                self.resource_viewer = props['resourceViewer']
            if 'resource_viewer' in props:
                self.resource_viewer = props['resource_viewer']
            if 'sheetCount' in props:
                self.sheet_count = props['sheetCount']
            if 'sheet_count' in props:
                self.sheet_count = props['sheet_count']
            if 'status' in props:
                self.status = props['status']
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

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
        if isinstance(value, list):
            self._alternate_emails.purge()
            self._alternate_emails.extend([
                (AlternateEmail(x, self._base)
                 if not isinstance(x, AlternateEmail) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._alternate_emails.purge()
            self._alternate_emails = value.to_list()
        elif isinstance(value, AlternateEmail):
            self._alternate_emails.purge()
            self._alternate_emails.append(value)

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
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

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

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'admin': prep(self._admin),
            'alternateEmails': prep(self._alternate_emails),
            'customWelcomeScreenViewed': prep(self._custom_welcome_screen_viewed),
            'email': prep(self._email),
            'firstName': prep(self._first_name),
            'groupAdmin': prep(self._group_admin),
            'id': prep(self.__id),
            'lastLogin': prep(self._last_login),
            'lastName': prep(self._last_name),
            'licensedSheetCreator': prep(self._licensed_sheet_creator),
            'name': prep(self._name),
            'resourceViewer': prep(self._resource_viewer),
            'sheetCount': prep(self.sheet_count),
            'status': prep(self._status)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'add_user':
            permitted = ['email', 'admin',
                         'licensedSheetCreator', 'firstName', 'lastName',
                         'resourceViewer']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'update_user':
            permitted = ['admin', 'licensedSheetCreator',
                         'firstName', 'lastName', 'resourceViewer']
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
