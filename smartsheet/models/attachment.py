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

from .user import User
from ..util import serialize
from ..util import deserialize
from datetime import datetime


class Attachment(object):

    """Smartsheet Attachment data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Attachment model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'attachment_sub_type': [
                'DOCUMENT',
                'SPREADSHEET',
                'PRESENTATION',
                'PDF',
                'DRAWING'],
            'attachment_type': [
                'BOX_COM',
                'DROPBOX',
                'EGNYTE',
                'EVERNOTE',
                'FILE',
                'GOOGLE_DRIVE',
                'LINK',
                'ONEDRIVE'],
            'parent_type': [
                'SHEET',
                'ROW',
                'COMMENT']}

        self._attachment_sub_type = None
        self._attachment_type = None
        self._created_at = None
        self._created_by = None
        self._description = None
        self._id_ = None
        self._mime_type = None
        self._name = None
        self._parent_id = None
        self._parent_type = None
        self._size_in_kb = None
        self._url = None
        self._url_expires_in_millis = None

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
    def attachment_sub_type(self):
        return self._attachment_sub_type

    @attachment_sub_type.setter
    def attachment_sub_type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['attachment_sub_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Attachment`attachment_sub_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['attachment_sub_type']))
            self._attachment_sub_type = value

    @property
    def attachment_type(self):
        return self._attachment_type

    @attachment_type.setter
    def attachment_type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['attachment_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Attachment`attachment_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['attachment_type']))
            self._attachment_type = value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        if isinstance(value, datetime):
            self._created_at = value

    @property
    def created_by(self):
        return self._created_by

    @created_by.setter
    def created_by(self, value):
        if isinstance(value, User):
            self._created_by = value
        else:
            self._created_by = User(value, self._base)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, six.string_types):
            self._description = value

    @property
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, value):
        if isinstance(value, six.integer_types):
            self._id_ = value

    @property
    def mime_type(self):
        return self._mime_type

    @mime_type.setter
    def mime_type(self, value):
        if isinstance(value, six.string_types):
            self._mime_type = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, six.string_types):
            self._name = value

    @property
    def parent_id(self):
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value):
        if isinstance(value, six.integer_types):
            self._parent_id = value

    @property
    def parent_type(self):
        return self._parent_type

    @parent_type.setter
    def parent_type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['parent_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Attachment`parent_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['parent_type']))
            self._parent_type = value

    @property
    def size_in_kb(self):
        return self._size_in_kb

    @size_in_kb.setter
    def size_in_kb(self, value):
        if isinstance(value, six.integer_types):
            self._size_in_kb = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if isinstance(value, six.string_types):
            self._url = value

    @property
    def url_expires_in_millis(self):
        return self._url_expires_in_millis

    @url_expires_in_millis.setter
    def url_expires_in_millis(self, value):
        if isinstance(value, six.integer_types):
            self._url_expires_in_millis = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
