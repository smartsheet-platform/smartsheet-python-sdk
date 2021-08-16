# pylint: disable=     ### find out what goes here ###
# Smartsheet Python SDK.
#
# Copyright 2021 Smartsheet.com, Inc.
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

# imports go here      # verify these imports
from .enums import AttachmentType
from .comment import Comment
from .user import User
from ..types import *
from ..util import serialize
from ..util import deserialize

class Proof(object):

    """Smartsheet Proof data model."""

    def __init__(self, props=None, base_obj=None):
            """Initialize the proof model."""
            self._base = None
            if base_obj is not None:
                self._base = base_obj

            # definition of attributes goes here
            self._id = Number()
            self._original_id = Number()
            self._name = String()
#             self._proof_type = String()
            self._proof_request_url = String()
            self._version = Number()

            self._last_updated_at = Number() | String() # Verify
            self._last_updated_by = Object() # Verify
            self._is_completed = Boolean()
            self._attachments = Array() # Verify
            self._discussions = Array() # Verify

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
            super(Proof, self).__setattr__(key, value)

            ##########################################

#         @property
#         def attachment_sub_type(self):
#             return self._attachment_sub_type
#
#         @attachment_sub_type.setter
#         def attachment_sub_type(self, value):
#             self._attachment_sub_type.set(value)

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

#         @property
#         def parent_id(self):
#             return self._parent_id.value
#
#         @parent_id.setter
#         def parent_id(self, value):
#             self._parent_id.value = value
#
#         @property
#         def parent_type(self):
#             return self._parent_type
#
#         @parent_type.setter
#         def parent_type(self, value):
#             self._parent_type.set(value)

#     @property
#     def size_in_kb(self):
#         return self._size_in_kb.value
#
#     @size_in_kb.setter
#     def size_in_kb(self, value):
#         self._size_in_kb.value = value
#
#     @property
#     def url(self):
#         return self._url.value
#
#     @url.setter
#     def url(self, value):
#         self._url.value = value

    # Keep everything below here
    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
