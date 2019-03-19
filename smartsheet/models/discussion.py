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
from .comment import Comment
from .enums import AccessLevel
from .user import User
from ..types import *
from ..util import serialize
from ..util import deserialize


class Discussion(object):

    """Smartsheet Discussion data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Discussion model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._access_level = EnumeratedValue(AccessLevel)
        self._comment = TypedObject(Comment)  # outbound (POST) only - singular
        self._comment_attachments = TypedList(Attachment)
        self._comment_count = Number()
        self._comments = TypedList(Comment)
        self._created_by = TypedObject(User)
        self._id_ = Number()
        self._last_commented_at = Timestamp()
        self._last_commented_user = TypedObject(User)
        self._parent_id = Number()
        self._parent_type = String()
        self._read_only = Boolean()
        self._title = String()

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
            super(Discussion, self).__setattr__(key, value)

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        self._access_level.set(value)

    @property
    def comment(self):
        return self._comment.value

    @comment.setter
    def comment(self, value):
        self._comment.value = value

    @property
    def comment_attachments(self):
        return self._comment_attachments

    @comment_attachments.setter
    def comment_attachments(self, value):
        self._comment_attachments.load(value)

    @property
    def comment_count(self):
        return self._comment_count.value

    @comment_count.setter
    def comment_count(self, value):
        self._comment_count.value = value

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, value):
        self._comments.load(value)

    @property
    def created_by(self):
        return self._created_by.value

    @created_by.setter
    def created_by(self, value):
        self._created_by.value = value

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def last_commented_at(self):
        return self._last_commented_at.value

    @last_commented_at.setter
    def last_commented_at(self, value):
        self._last_commented_at.value = value

    @property
    def last_commented_user(self):
        return self._last_commented_user.value

    @last_commented_user.setter
    def last_commented_user(self, value):
        self._last_commented_user.value = value

    @property
    def parent_id(self):
        return self._parent_id.value

    @parent_id.setter
    def parent_id(self, value):
        self._parent_id.value = value

    @property
    def parent_type(self):
        return self._parent_type.value

    @parent_type.setter
    def parent_type(self, value):
        self._parent_type.value = value

    @property
    def read_only(self):
        return self._read_only.value

    @read_only.setter
    def read_only(self, value):
        self._read_only.value = value

    @property
    def title(self):
        return self._title.value

    @title.setter
    def title(self, value):
        self._title.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
