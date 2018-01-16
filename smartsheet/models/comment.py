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

from .attachment import Attachment
from .user import User
from ..types import TypedList
from ..util import prep
from datetime import datetime
from dateutil.parser import parse
import json
import six


class Comment(object):

    """Smartsheet Comment data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Comment model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._attachments = TypedList(Attachment)
        self._created_at = None
        self._created_by = None
        self._discussion_id = None
        self.__id = None
        self._modified_at = None
        self._text = None

        if props:
            # account for alternate variable names from raw API response
            if 'attachments' in props:
                self.attachments = props['attachments']
            if 'createdAt' in props:
                self.created_at = props['createdAt']
            if 'created_at' in props:
                self.created_at = props['created_at']
            if 'createdBy' in props:
                self.created_by = props['createdBy']
            if 'created_by' in props:
                self.created_by = props['created_by']
            if 'discussionId' in props:
                self.discussion_id = props['discussionId']
            if 'discussion_id' in props:
                self.discussion_id = props['discussion_id']
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'modifiedAt' in props:
                self.modified_at = props['modifiedAt']
            if 'modified_at' in props:
                self.modified_at = props['modified_at']
            if 'text' in props:
                self.text = props['text']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

    @property
    def attachments(self):
        return self._attachments

    @attachments.setter
    def attachments(self, value):
        if isinstance(value, list):
            self._attachments.purge()
            self._attachments.extend([
                (Attachment(x, self._base)
                 if not isinstance(x, Attachment) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._attachments.purge()
            self._attachments = value.to_list()
        elif isinstance(value, Attachment):
            self._attachments.purge()
            self._attachments.append(value)

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        if isinstance(value, datetime):
            self._created_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
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
    def discussion_id(self):
        return self._discussion_id

    @discussion_id.setter
    def discussion_id(self, value):
        if isinstance(value, six.integer_types):
            self._discussion_id = value

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

    @property
    def modified_at(self):
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value):
        if isinstance(value, datetime):
            self._modified_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._modified_at = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if isinstance(value, six.string_types):
            self._text = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'attachments': prep(self._attachments),
            'createdAt': prep(self._created_at),
            'createdBy': prep(self._created_by),
            'discussionId': prep(self._discussion_id),
            'id': prep(self.__id),
            'modifiedAt': prep(self._modified_at),
            'text': prep(self._text)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
