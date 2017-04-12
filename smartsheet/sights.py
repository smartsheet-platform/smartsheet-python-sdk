# pylint: disable=C0111,R0902,R0913
# Smartsheet Python SDK.
#
# Copyright 2017 Smartsheet.com, Inc.
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

import logging
from . import fresh_operation
from datetime import datetime

class Sights(object):

    """Class for handling Sights operations."""

    def __init__(self, smartsheet_obj):
        """Init Sights with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def list_sights(self, page_size=100, page=1,
                    include_all=False, modified_since=None):
        """Get the list of all Sights the User has access to, in alphabetical
        order, by name.

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
        _op = fresh_operation('list_sights')
        _op['method'] = 'GET'
        _op['path'] = '/sights'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all
        if isinstance(modified_since, datetime):
            _op['query_params']['modifiedSince'] = modified_since.isoformat()

        expected = ['IndexResult', 'Sight']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_sight(self, sight_id):
        """Get the specified Sight.

        Args:
            sight_id (int): Sight ID

        Returns:
            Sight
        """
        _op = fresh_operation('get_sight')
        _op['method'] = 'GET'
        _op['path'] = '/sights/' + str(sight_id)

        expected = 'Sight'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_sight(self, sight_id, sight_obj):
        """Updates the specified Sight.

        Args:
            sight_id (int): Sight ID
            sight_obj (Sight): Sight object.

        Returns:
            Result
        """
        _op = fresh_operation('update_sight')
        _op['method'] = 'PUT'
        _op['path'] = '/sights/' + str(sight_id)
        _op['json'] = sight_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_sight'

        expected = ['Result', 'Sight']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_sight(self, sight_id):
        """Delete the specified Sight.

        Args:
            sight_id (int): Sight ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_sight')
        _op['method'] = 'DELETE'
        _op['path'] = '/sights/' + str(sight_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def copy_sight(self, sight_id, container_destination_obj):
        """Creates a copy of the specified Sight

        Args:
            sight_id (int): Sight ID
            container_destination_obj
                (ContainerDestination): Container Destination object.

        Returns:
            Result
        """
        _op = fresh_operation('copy_sight')
        _op['method'] = 'POST'
        _op['path'] = '/sights/' + str(sight_id) + '/copy'
        _op['json'] = container_destination_obj

        expected = ['Result', 'Sight']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def move_sight(self, sight_id, container_destination_obj):
        """Creates a copy of the specified Sight

        Args:
            sight_id (int): Sight ID
            container_destination_obj
                (ContainerDestination): Container Destination object.

        Returns:
            Result
        """
        _op = fresh_operation('move_sight')
        _op['method'] = 'POST'
        _op['path'] = '/sights/' + str(sight_id) + '/move'
        _op['json'] = container_destination_obj

        expected = ['Result', 'Sight']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_shares(self, sight_id, page_size=100, page=1,
                    include_all=False, include_workspace_shares=False ):
        """Get the list of all Users and Groups to whom the specified Sight is
        shared, and their access level.

        Args:
            sight_id (int): Sight ID
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_shares')
        _op['method'] = 'GET'
        _op['path'] = '/sights/' + str(sight_id) + '/shares'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all
        if include_workspace_shares:
            _op['query_params']['include'] = 'workspaceShares'

        expected = ['IndexResult', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_share(self, sight_id, share_id):
        """Get the specified Share.

        Args:
            sight_id (int): Sight ID
            share_id (str): Share ID

        Returns:
            Share
        """
        _op = fresh_operation('get_share')
        _op['method'] = 'GET'
        _op['path'] = '/sights/' + str(sight_id) + '/shares/' + str(share_id)

        expected = 'Share'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def share_sight(self, share_id, share_obj, send_email=False):
        """Share the specified Sight.

        Share the specified Sight with the specified Users and
        Groups.

        Args:
            sight_id (int): Sight ID
            share_obj (Share): Share object.
            send_email (bool): Either true or false to
                indicate whether or not to notify the user by email. Default
                is false.

        Returns:
            Result
        """
        _op = fresh_operation('share_sight')
        _op['method'] = 'POST'
        _op['path'] = '/sights/' + str(share_id) + '/shares'
        _op['query_params']['sendEmail'] = send_email
        _op['json'] = share_obj

        expected = ['Result', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_share(self, sight_id, share_id, share_obj):
        """Update the access level of a User or Group for the specified Sight.

        Args:
            sight_id (int): Sight ID
            share_id (str): Share ID
            share_obj (Share): Share object.

        Returns:
            Result
        """
        if not all(val is not None for val in ['sight_id', 'share_id',
                                               'share_obj']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('update_share')
        _op['method'] = 'PUT'
        _op['path'] = '/sights/' + str(sight_id) + '/shares/' + str(share_id)
        _op['json'] = share_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_share'

        expected = ['Result', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_share(self, sight_id, share_id):
        """Delete the specified Share.

        Args:
            sight_id (int): Sight ID
            share_id (str): Share ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_share')
        _op['method'] = 'DELETE'
        _op['path'] = '/sights/' + str(sight_id) + '/shares/' + str(share_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_publish_status(self, sight_id):
        """Get the Publish status of the Sight.

        Get the status of the Publish settings of the Sight,
        including URLs of any enabled publishings.

        Args:
            sight_id (int): Sight ID

        Returns:
            SightPublish
        """
        _op = fresh_operation('get_publish_status')
        _op['method'] = 'GET'
        _op['path'] = '/sights/' + str(sight_id) + '/publish'

        expected = 'SightPublish'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def set_publish_status(self, sight_id, sight_publish_obj):
        """Set the publish status of the Sight and returns the new status,
        including the URLs of any enabled publishings.

        Args:
            sight_id (int): Sight ID
            sight_publish_obj (SightPublish): SightPublish object.

        Returns:
            Result
        """
        attributes = ['read_only_full_enabled','read_only_full_accessible_by']

        fetch_first = False
        # check for incompleteness, fill in from current status if necessary
        for attribute in attributes:
            val = getattr(sight_publish_obj, attribute, None)
            if val is None:
                fetch_first = True
                break

        if fetch_first:
            current_status = self.get_publish_status(sight_id).to_dict()
            current_status.update(sight_publish_obj.to_dict())
            sight_publish_obj = self._base.models.SightPublish(current_status)

        _op = fresh_operation('set_publish_status')
        _op['method'] = 'PUT'
        _op['path'] = '/sights/' + str(sight_id) + '/publish'
        _op['json'] = sight_publish_obj
        # filter before we go
        _op['json'].pre_request_filter = 'set_publish_status'

        expected = ['Result', 'SightPublish']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response