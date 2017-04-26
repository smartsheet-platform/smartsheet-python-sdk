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

from .attachment import Attachment
from .comment import Comment
from .user import User
from ..types import TypedList
from ..util import prep
from datetime import datetime
from dateutil.parser import parse
import json
import logging
import six

class Discussion(object):

    """Smartsheet Discussion data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Discussion model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

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
        self.__id = None
        self._last_commented_at = None
        self._last_commented_user = None
        self._parent_id = None
        self._parent_type = None
        self._read_only = None
        self._title = None

        if props:
            # account for alternate variable names from raw API response
            if 'accessLevel' in props:
                self.access_level = props['accessLevel']
            if 'access_level' in props:
                self.access_level = props['access_level']
            if 'comment' in props:
                self.comment = props['comment']
            if 'commentAttachments' in props:
                self.comment_attachments = props[
                    'commentAttachments']
            if 'comment_attachments' in props:
                self.comment_attachments = props[
                    'comment_attachments']
            if 'commentCount' in props:
                self.comment_count = props['commentCount']
            if 'comment_count' in props:
                self.comment_count = props['comment_count']
            if 'comments' in props:
                self.comments = props['comments']
            if 'createdBy' in props:
                self.created_by = props['createdBy']
            if 'created_by' in props:
                self.created_by = props['created_by']
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'lastCommentedAt' in props:
                self.last_commented_at = props[
                    'lastCommentedAt']
            if 'last_commented_at' in props:
                self.last_commented_at = props[
                    'last_commented_at']
            if 'lastCommentedUser' in props:
                self.last_commented_user = props[
                    'lastCommentedUser']
            if 'last_commented_user' in props:
                self.last_commented_user = props[
                    'last_commented_user']
            if 'parentId' in props:
                self.parent_id = props['parentId']
            if 'parent_id' in props:
                self.parent_id = props['parent_id']
            if 'parentType' in props:
                self.parent_type = props['parentType']
            if 'parent_type' in props:
                self.parent_type = props['parent_type']
            if 'readOnly' in props:
                self.read_only = props['readOnly']
            if 'read_only' in props:
                self.read_only = props['read_only']
            if 'title' in props:
                self.title = props['title']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

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
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

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

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        if self.comment is not None:
            self.comment.pre_request_filter = value
        if self.comment_attachments is not None:
            # Attachment
            for item in self.comment_attachments:
                item.pre_request_filter = value
        if self.comments is not None:
            # Comment
            for item in self.comments:
                item.pre_request_filter = value
        if self.created_by is not None:
            self.created_by.pre_request_filter = value
        if self.last_commented_user is not None:
            self.last_commented_user.pre_request_filter = value
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        req_filter = self.pre_request_filter
        if req_filter:
            if self.comment is not None:
                self.comment.pre_request_filter = req_filter
            if self.comment_attachments is not None:
                for item in self.comment_attachments:
                    item.pre_request_filter = req_filter
            if self.comments is not None:
                for item in self.comments:
                    item.pre_request_filter = req_filter
            if self.created_by is not None:
                self.created_by.pre_request_filter = req_filter
            if self.last_commented_user is not None:
                self.last_commented_user.pre_request_filter = req_filter

        obj = {
            'accessLevel': prep(self._access_level),
            'comment': prep(self._comment),
            'commentAttachments': prep(self._comment_attachments),
            'commentCount':prep(self._comment_count),
            'comments': prep(self._comments),
            'createdBy': prep(self._created_by),
            'id': prep(self.__id),
            'lastCommentedAt': prep(self._last_commented_at),
            'lastCommentedUser': prep(self._last_commented_user),
            'parentId': prep(self._parent_id),
            'parentType': prep(self._parent_type),
            'readOnly': prep(self._read_only),
            'title': prep(self._title)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'create_discussion_on_row':
            permitted = ['title', 'comment']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'create_discussion_on_row_with_attachment':
            permitted = ['title', 'comment']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'create_discussion_on_sheet':
            permitted = ['title', 'comment']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'create_discussion_on_sheet_with_attachment':
            permitted = ['title', 'comment']
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
