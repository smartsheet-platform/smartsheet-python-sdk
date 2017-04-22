# pylint: disable=C0111,R0902,R0913
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

import logging
import os.path
import six
from . import fresh_operation


class Discussions(object):

    """Class for handling Discussions operations."""

    def __init__(self, smartsheet_obj):
        """Init Discussions with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def add_comment_to_discussion(self, sheet_id, discussion_id,
                                  comment_obj=None):
        """Add a Comment to the specified Discussion

        Args:
            sheet_id (int): Sheet ID
            discussion_id (int): Discussion ID
            comment_obj (Comment): Comment object.

        Returns:
            Result
        """
        _op = fresh_operation('add_comment_to_discussion')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/discussions/' + str(
            discussion_id) + '/comments'
        _op['json'] = comment_obj
        # filter before we go
        _op['json'].pre_request_filter = 'add_comment_to_discussion'

        expected = ['Result', 'Comment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    # pylint: disable=invalid-name
    def add_comment_to_discussion_with_attachment(self, sheet_id,
                                                  discussion_id, comment, _file=None):
        """Add a Comment with an Attachment to the specified Discussion

        Args:
            sheet_id (int): Sheet ID
            discussion_id (int): Discussion ID
            comment (file): Comment object.
            _file (file): String or file stream object.

        Returns:
            Result
        """
        if not all(val is not None for val in ['sheet_id', 'discussion_id',
                                               'comment']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('add_comment_to_discussion_with_attachment')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/discussions/' + str(
            discussion_id) + '/comments'
        _op['files'] = {}
        comment.pre_request_filter = 'add_comment_to_discussion_with_attachment'
        field_str = comment.to_json()
        _op['files']['comment'] = (None, six.StringIO(field_str), 'application/json')
        _op['files']['file'] = _file

        expected = ['Result', 'Comment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    # pylint: enable=invalid-name

    def create_discussion_on_row(self, sheet_id, row_id,
                                 discussion_obj=None):
        """Create a new Discussion on a Row.



        Args:
            sheet_id (int): Sheet ID
            row_id (int): Row ID
            discussion_obj (Discussion): Discussion object.

        Returns:
            Result
        """
        _op = fresh_operation('create_discussion_on_row')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows/' + str(
            row_id) + '/discussions'
        _op['json'] = discussion_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_discussion_on_row'

        expected = ['Result', 'Discussion']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    # pylint: disable=invalid-name
    def create_discussion_on_row_with_attachment(self, sheet_id, row_id,
                                                 discussion, _file=None):
        """Create a new Discussion on a Row with an attachment.

        Args:
            sheet_id (int): Sheet ID
            row_id (int): Row ID
            discussion (file): Discussion object.
            _file (file): String or file stream object.

        Returns:
            Result
        """
        if not all(val is not None for val in ['sheet_id', 'row_id',
                                               'discussion']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('create_discussion_on_row_with_attachment')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows/' + str(
            row_id) + '/discussions'
        _op['files'] = {}
        discussion.pre_request_filter = 'create_discussion_on_row_with_attachment'
        field_str = discussion.to_json()
        _op['files']['discussion'] = (None, six.StringIO(field_str), 'application/json')
        _op['files']['file'] = _file

        expected = ['Result', 'Discussion']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    # pylint: enable=invalid-name

    def create_discussion_on_sheet(self, sheet_id, discussion_obj=None):
        """Create a new Discussion on a Sheet.

        Args:
            sheet_id (int): Sheet ID
            discussion_obj (Discussion): Discussion object.

        Returns:
            Result
        """
        _op = fresh_operation('create_discussion_on_sheet')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/discussions'
        _op['json'] = discussion_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_discussion_on_sheet'

        expected = ['Result', 'Discussion']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    # pylint: disable=invalid-name
    def create_discussion_on_sheet_with_attachment(self, sheet_id,
                                                   discussion, _file=None):
        """Create a new Discussion on a Sheet with an attachment.

        Args:
            sheet_id (int): Sheet ID
            discussion (file): Discussion object.
            _file (file): String or file stream object.

        Returns:
            Result
        """
        _op = fresh_operation('create_discussion_on_sheet_with_attachment')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/discussions'
        _op['files'] = {}
        discussion.pre_request_filter = 'create_discussion_on_sheet_with_attachment'
        field_str = discussion.to_json()
        _op['files']['discussion'] = (None, six.StringIO(field_str), 'application/json')
        _op['files']['file'] = _file

        expected = ['Result', 'Discussion']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    # pylint: enable=invalid-name

    def delete_discussion(self, sheet_id, discussion_id):
        """Delete the specified Discussion.

        Args:
            sheet_id (int): Sheet ID
            discussion_id (int): Discussion ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_discussion')
        _op['method'] = 'DELETE'
        _op['path'] = '/sheets/' + str(sheet_id) + '/discussions/' + str(
            discussion_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_discussion_comment(self, sheet_id, comment_id):
        """Delete the specified Sheet Comment.

        Delete the specified Comment from the specified Sheet.

        Args:
            sheet_id (int): Sheet ID
            comment_id (int): Comment ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_discussion_comment')
        _op['method'] = 'DELETE'
        _op['path'] = '/sheets/' + str(sheet_id) + '/comments/' + str(
            comment_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_all_discussions(self, sheet_id, include=None, page_size=100,
                            page=1, include_all=False):
        """Get a list of all Discussions on the specified Sheet.

        Get a list of all Discussions associated with the specified
        Sheet (both sheet-level discussions and row-level discussions).

        Args:
            sheet_id (int): Sheet ID
            include (list[str]): A comma-separated list of
                optional elements to include in the response. Valid list
                values: comments, attachments
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('get_all_discussions')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/discussions'
        _op['query_params']['include'] = include
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Discussion']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_discussion(self, sheet_id, discussion_id):
        """Get the specified Discussion.

        Args:
            sheet_id (int): Sheet ID
            discussion_id (int): Discussion ID

        Returns:
            Discussion
        """
        _op = fresh_operation('get_discussion')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/discussions/' + str(
            discussion_id)

        expected = 'Discussion'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_discussion_comment(self, sheet_id, comment_id):
        """Get the specified Comment.

        Args:
            sheet_id (int): Sheet ID
            comment_id (int): Comment ID

        Returns:
            Comment
        """
        _op = fresh_operation('get_discussion_comment')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/comments/' + str(
            comment_id)

        expected = 'Comment'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_row_discussions(self, sheet_id, row_id, include=None,
                            page_size=100, page=1, include_all=False):
        """Get a list of all Discussions associated with the specified Row.

        Args:
            sheet_id (int): Sheet ID
            row_id (int): Row ID
            include (list[str]): A comma-separated list of
                optional elements to include in the response. Valid list
                values: comments, attachments. (Attachments is effective
                only if comments is present, otherwise ignored.)
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('get_row_discussions')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows/' + str(
            row_id) + '/discussions'
        _op['query_params']['include'] = include
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Discussion']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_comment(self, sheet_id, comment_id, comment_obj):
        """Update the specified Comment.

        Args:
            sheet_id (int): Sheet ID
            comment_id (int): Comment ID
            comment_obj (Comment): Comment object with the following attributes:
          * text (required)

        Returns:
            Result
        """
        _op = fresh_operation('update_comment')
        _op['method'] = 'PUT'
        _op['path'] = '/sheets/' + str(sheet_id) + '/comments/' + str(comment_id)
        _op['json'] = comment_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_comment'

        expected = ['Result', 'Comment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response