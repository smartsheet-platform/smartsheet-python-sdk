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

from .enums import AttachmentParentType, AttachmentSubType, AttachmentType
from .user import User
from ..types import *
from ..util import serialize
from ..util import deserialize


class Attachment(object):

    """Smartsheet Attachment data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Attachment model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._attachment_sub_type = EnumeratedValue(AttachmentSubType)
        self._attachment_type = EnumeratedValue(AttachmentType)
        self._created_at = Timestamp()
        self._created_by = TypedObject(User)
        self._description = String()
        self._id_ = Number()
        self._mime_type = String()
        self._name = String()
        self._parent_id = Number()
        self._parent_type = EnumeratedValue(AttachmentParentType)
        self._size_in_kb = Number()
        self._url = String()
        self._url_expires_in_millis = Number()

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
            super(Attachment, self).__setattr__(key, value)

    @property
    def attachment_sub_type(self):
        return self._attachment_sub_type

    @attachment_sub_type.setter
    def attachment_sub_type(self, value):
        self._attachment_sub_type.set(value)

    @property
    def attachment_type(self):
        return self._attachment_type

    @attachment_type.setter
    def attachment_type(self, value):
        self._attachment_type.set(value)

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
    def description(self):
        return self._description.value
    
    @description.setter
    def description(self, value):
        self._description.value = value

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def mime_type(self):
        return self._mime_type.value

    @mime_type.setter
    def mime_type(self, value):
        self._mime_type.value = value

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._name.value = value

    @property
    def parent_id(self):
        return self._parent_id.value

    @parent_id.setter
    def parent_id(self, value):
        self._parent_id.value = value

    @property
    def parent_type(self):
        return self._parent_type

    @parent_type.setter
    def parent_type(self, value):
        self._parent_type.set(value)

    @property
    def size_in_kb(self):
        return self._size_in_kb.value

    @size_in_kb.setter
    def size_in_kb(self, value):
        self._size_in_kb.value = value

    @property
    def url(self):
        return self._url.value

    @url.setter
    def url(self, value):
        self._url.value = value

    @property
    def url_expires_in_millis(self):
        return self._url_expires_in_millis.value

    @url_expires_in_millis.setter
    def url_expires_in_millis(self, value):
        self._url_expires_in_millis.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
