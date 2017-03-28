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

from .user import User
from ..types import TypedList
from ..util import prep
from datetime import datetime
from dateutil.parser import parse
import json
import logging
import six

class Attachment(object):

    """Smartsheet Attachment data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Attachment model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

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
        self.__id = None
        self._mime_type = None
        self._name = None
        self._parent_id = None
        self._parent_type = None
        self._size_in_kb = None
        self._url = None
        self._url_expires_in_millis = None

        if props:
            # account for alternate variable names from raw API response
            if 'attachmentSubType' in props:
                self.attachment_sub_type = props[
                    'attachmentSubType']
            if 'attachment_sub_type' in props:
                self.attachment_sub_type = props[
                    'attachment_sub_type']
            if 'attachmentType' in props:
                self.attachment_type = props['attachmentType']
            if 'attachment_type' in props:
                self.attachment_type = props['attachment_type']
            # read only
            if 'createdAt' in props:
                self.created_at = props['createdAt']
            if 'createdBy' in props:
                self.created_by = props['createdBy']
            if 'created_by' in props:
                self.created_by = props['created_by']
            if 'description' in props:
                self.description = props['description']
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            # read only
            if 'mimeType' in props:
                self.mime_type = props['mimeType']
            if 'name' in props:
                self.name = props['name']
            # read only
            if 'parentId' in props:
                self.parent_id = props['parentId']
            # read only
            if 'parentType' in props:
                self.parent_type = props['parentType']
            # read only
            if 'sizeInKb' in props:
                self.size_in_kb = props['sizeInKb']
            if 'url' in props:
                self.url = props['url']
            # read only
            if 'urlExpiresInMillis' in props:
                self.url_expires_in_millis = props[
                    'urlExpiresInMillis']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

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
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

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

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        if self.created_by is not None:
            self.created_by.pre_request_filter = value
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        req_filter = self.pre_request_filter
        if req_filter:
            if self.created_by is not None:
                self.created_by.pre_request_filter = req_filter

        obj = {
            'attachmentSubType': prep(self._attachment_sub_type),
            'attachmentType': prep(self._attachment_type),
            'createdAt': prep(self._created_at),
            'createdBy': prep(self._created_by),
            'description': prep(self._description),
            'id': prep(self.__id),
            'mimeType': prep(self._mime_type),
            'name': prep(self._name),
            'parentId': prep(self._parent_id),
            'parentType': prep(self._parent_type),
            'sizeInKb': prep(self._size_in_kb),
            'url': prep(self._url),
            'urlExpiresInMillis': prep(self._url_expires_in_millis)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'attach_url_to_comment':
            permitted = ['name', 'url', 'attachmentType',
                         'attachmentSubType']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'attach_url_to_row':
            permitted = ['name', 'description', 'url',
                         'attachmentType', 'attachmentSubType']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'attach_url_to_sheet':
            permitted = ['name', 'description', 'url',
                         'attachmentType', 'attachmentSubType']
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
