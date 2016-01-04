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


class Groups(object):

    """Class for handling Groups operations."""

    def __init__(self, smartsheet_obj):
        """Init Groups with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def add_members(self, group_id, group_member_obj):
        """Add one or more members to a Group.

        Args:
            group_id (int): Group ID
            group_member_obj (GroupMember): Group member
                object(s).

        Returns:
            Result
        """
        _op = fresh_operation('add_members')
        _op['method'] = 'POST'
        _op['path'] = '/groups/' + str(group_id) + '/members'
        _op['json'] = group_member_obj

        expected = ['Result', 'GroupMember']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def create_group(self, group_obj):
        """Create a new Group

        Args:
            group_obj (Group): Group object.

        Returns:
            Result
        """
        _op = fresh_operation('create_group')
        _op['method'] = 'POST'
        _op['path'] = '/groups'
        _op['json'] = group_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_group'

        expected = ['Result', 'Group']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_group(self, group_id):
        """Delete the specified Group.

        Args:
            group_id (int): Group ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_group')
        _op['method'] = 'DELETE'
        _op['path'] = '/groups/' + str(group_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_group(self, group_id):
        """Get the specified Group.

        Args:
            group_id (int): Group ID

        Returns:
            Group
        """
        _op = fresh_operation('get_group')
        _op['method'] = 'GET'
        _op['path'] = '/groups/' + str(group_id)

        expected = 'Group'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_groups(self, page_size=100, page=1, include_all=False):
        """Get all Groups in an organization.

        Get the list of all Groups in an organization. To fetch the
        members of an individual group, use the getGroup operation.

        Args:
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_groups')
        _op['method'] = 'GET'
        _op['path'] = '/groups'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Group']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def remove_member(self, group_id, user_id):
        """Removes a member from the specified Group.

        Args:
            group_id (int): Group ID
            user_id (int): User ID

        Returns:
            Result
        """
        _op = fresh_operation('remove_member')
        _op['method'] = 'DELETE'
        _op['path'] = '/groups/' + str(group_id) + '/members/' + str(user_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_group(self, group_id, group_obj):
        """Updates the specified Group.

        Args:
            group_id (int): Group ID
            group_obj (Group): Group object.

        Returns:
            Result
        """
        _op = fresh_operation('update_group')
        _op['method'] = 'PUT'
        _op['path'] = '/groups/' + str(group_id)
        _op['json'] = group_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_group'

        expected = ['Result', 'Group']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
