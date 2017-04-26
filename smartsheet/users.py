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
from . import fresh_operation
from datetime import datetime


class Users(object):

    """Class for handling Users operations."""

    def __init__(self, smartsheet_obj):
        """Init Users with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def add_alternate_email(self, user_id, list_of_alternate_emails):
        """Add one or more alternate email addresses for the specified User

        Args:
            user_id (int): User ID
            list_of_alternate_emails (list[AlternateEmail]):
                An array of one or more AlternateEmail objects.

        Returns:
            Result
        """
        _op = fresh_operation('add_alternate_email')
        _op['method'] = 'POST'
        _op['path'] = '/users/' + str(user_id) + '/alternateemails'
        _op['json'] = list_of_alternate_emails
        # filter before we go
        for item in _op['json']:
            item.pre_request_filter = 'add_alternate_email'

        expected = ['Result', 'AlternateEmail']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def promote_alternate_email(self, user_id, alt_id):
        """Add one or more alternate email addresses for the specified User

        Args:
            user_id (int): User ID
            alt_id(int):  AlternateEmail ID to be promoted

        Returns:
            Result
        """
        _op = fresh_operation('promote_alternate_email')
        _op['method'] = 'POST'
        _op['path'] = '/users/' + str(user_id) + '/alternateemails/' + str(alt_id) + '/makeprimary'

        expected = ['Result', 'AlternateEmail']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def add_user(self, user_obj, send_email=False):
        """Add a User to the organization.

        Args:
            user_obj (User): User object with the following attributes:

                email (required)

                admin (required)

                licensedSheetCreator (required)

                firstName (optional)

                lastName (optional)

                resourceViewer (optional)

                send_email (bool): Either true or false to indicate whether or not to notify the user by email. Default
                is false.

        Returns:
            Result
        """
        _op = fresh_operation('add_user')
        _op['method'] = 'POST'
        _op['path'] = '/users'
        _op['query_params']['sendEmail'] = send_email
        _op['json'] = user_obj
        # filter before we go
        _op['json'].pre_request_filter = 'add_user'

        expected = ['Result', 'User']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_alternate_email(self, user_id, alternate_email_id):
        """Deletes the specified alternate email address for the specified User.

        Args:
            user_id (int): User ID
            alternate_email_id (int): Alternate Email ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_alternate_email')
        _op['method'] = 'DELETE'
        _op['path'] = '/users/' + str(user_id) + '/alternateemails/' + str(
            alternate_email_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_alternate_email(self, user_id, alternate_email_id):
        """Get the specified Alternate Email

        Args:
            user_id (int): User ID
            alternate_email_id (int): Alternate Email ID

        Returns:
            AlternateEmail
        """
        _op = fresh_operation('get_alternate_email')
        _op['method'] = 'GET'
        _op['path'] = '/users/' + str(user_id) + '/alternateemails/' + str(
            alternate_email_id)

        expected = 'AlternateEmail'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_current_user(self):
        """Get the currently authenticated User.
        Returns:
            UserProfile
        """
        _op = fresh_operation('get_current_user')
        _op['method'] = 'GET'
        _op['path'] = '/users/me'

        expected = 'UserProfile'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_user(self, user_id):
        """Get the specified User.

        Args:
            user_id (int): User ID

        Returns:
            UserProfile
        """
        _op = fresh_operation('get_user')
        _op['method'] = 'GET'
        _op['path'] = '/users/' + str(user_id)

        expected = 'UserProfile'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_alternate_emails(self, user_id):
        """Get a list of the Alternate Emails for the specified User.

        Args:
            user_id (int): User ID

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_alternate_emails')
        _op['method'] = 'GET'
        _op['path'] = '/users/' + str(user_id) + '/alternateemails'

        expected = ['IndexResult', 'AlternateEmail']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_org_sheets(self, page_size=100, page=1,
                    include_all=False, modified_since=None):
        """Get a list of all Sheets owned by an organization.

        Get the list of all Sheets owned by the members of the
        account (organization).

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
        _op = fresh_operation('list_org_sheets')
        _op['method'] = 'GET'
        _op['path'] = '/users/sheets'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all
        if isinstance(modified_since, datetime):
            _op['query_params']['modifiedSince'] = modified_since.isoformat()

        expected = ['IndexResult', 'Sheet']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_users(self, email=None, page_size=100, page=1,
                   include_all=False):
        """Get the list of Users in the organization.

        Args:
            email (list[str]): Comma separated list of email
                addresses on which to filter the results.
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_users')
        _op['method'] = 'GET'
        _op['path'] = '/users'
        _op['query_params']['email'] = email
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'User']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def remove_user(self, user_id, transfer_to=None, transfer_sheets=False,
                    remove_from_sharing=False):
        """Remove a user from an organization.

        Remove a User from an organization. User is transitioned to
        a free collaborator with read-only access to owned sheets, unless
        those are optionally transferred to another User.

        Args:
            user_id (int): User ID
            transfer_to (int): The ID of the User to
                transfer ownership to. If the User being removed owns
                groups, this value is required. Any groups owned by the User
                being removed will be transferred to the specified User. If
                the User owns sheets, _and_ **transferSheets** is `true`,
                the removed User's sheets will be transferred to the
                specified User.
            transfer_sheets (bool): If `true` and
                **transferTo** is specified, the removed User's sheets will
                be transferred. Otherwise, sheets will not be transferred.
                Defaults to `false`.
            remove_from_sharing (bool): Set to `true` to
                remove the user from sharing for all sheets/workspaces in
                the organization. If not specified, User will not be removed
                from sharing.

        Returns:
            Result
        """
        _op = fresh_operation('remove_user')
        _op['method'] = 'DELETE'
        _op['path'] = '/users/' + str(user_id)
        _op['query_params']['transferTo'] = transfer_to
        _op['query_params']['transferSheets'] = transfer_sheets
        _op['query_params']['removeFromSharing'] = remove_from_sharing

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_user(self, user_id, user_obj):
        """Update the specified User.

        Args:
            user_id (int): User ID
            user_obj (User): User object with the following
                attributes:
          * email (required)
          * admin
                (required)
          * licensedSheetCreator (required)

                    * firstName (optional)
          * lastName (optional)

                        * resourceViewer (optional)

        Returns:
            Result
        """
        _op = fresh_operation('update_user')
        _op['method'] = 'PUT'
        _op['path'] = '/users/' + str(user_id)
        _op['json'] = user_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_user'

        expected = ['Result', 'User']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
