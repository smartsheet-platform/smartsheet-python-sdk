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
from .comment import Comment
from .user import User
from ..types import TypedList
from ..util import serialize
from ..util import deserialize
from datetime import datetime
from dateutil.parser import parse


class Discussion(object):

    """Smartsheet Discussion data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Discussion model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'access_level': [
                'VIEWER',
                'EDITOR',
                'EDITOR_SHARE',
                'ADMIN',
                'OWNER']}

        self._access_level = None
        self._comment = None
        self._comment_attachments = TypedList(Attachment)
        self._comment_count = None
        self._comments = TypedList(Comment)
        self._created_by = None
        self._id_ = None
        self._last_commented_at = None
        self._last_commented_user = None
        self._parent_id = None
        self._parent_type = None
        self._read_only = None
        self._title = None

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
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['access_level']:
                raise ValueError(
                    ("`{0}` is an invalid value for Discussion`access_level`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['access_level']))
            self._access_level = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        if isinstance(value, Comment):
            self._comment = value
        else:
            self._comment = Comment(value, self._base)

    @property
    def comment_attachments(self):
        return self._comment_attachments

    @comment_attachments.setter
    def comment_attachments(self, value):
        if isinstance(value, list):
            self._comment_attachments.purge()
            self._comment_attachments.extend([
                (Attachment(x, self._base)
                 if not isinstance(x, Attachment) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._comment_attachments.purge()
            self._comment_attachments = value.to_list()
        elif isinstance(value, Attachment):
            self._comment_attachments.purge()
            self._comment_attachments.append(value)

    @property
    def comment_count(self):
        return self._comment_count

    @comment_count.setter
    def comment_count(self, value):
        if isinstance(value, six.integer_types):
            self._comment_count = value

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, value):
        if isinstance(value, list):
            self._comments.purge()
            self._comments.extend([
                (Comment(x, self._base)
                 if not isinstance(x, Comment) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._comments.purge()
            self._comments = value.to_list()
        elif isinstance(value, Comment):
            self._comments.purge()
            self._comments.append(value)

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
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, value):
        if isinstance(value, six.integer_types):
            self._id_ = value

    @property
    def last_commented_at(self):
        return self._last_commented_at

    @last_commented_at.setter
    def last_commented_at(self, value):
        if isinstance(value, datetime):
            self._last_commented_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._last_commented_at = value

    @property
    def last_commented_user(self):
        return self._last_commented_user

    @last_commented_user.setter
    def last_commented_user(self, value):
        if isinstance(value, User):
            self._last_commented_user = value
        else:
            self._last_commented_user = User(value, self._base)

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
            self._parent_type = value

    @property
    def read_only(self):
        return self._read_only

    @read_only.setter
    def read_only(self, value):
        if isinstance(value, bool):
            self._read_only = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, six.string_types):
            self._title = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
