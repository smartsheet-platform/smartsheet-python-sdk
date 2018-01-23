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

from .attachment import Attachment
from .user import User
from ..types import TypedList
from ..util import serialize
from ..util import deserialize
from datetime import datetime
from dateutil.parser import parse


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
        self._id_ = None
        self._modified_at = None
        self._text = None

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
            super(Comment, self).__setattr__(key, value)

    @property
    def attachments(self):
        return self._attachments

    @attachments.setter
    def attachments(self, value):
        self._attachments.load(value)

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
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, value):
        if isinstance(value, six.integer_types):
            self._id_ = value

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

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
