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

from .models.folder import Folder
import logging
import os.path
import six
from . import fresh_operation


class Workspaces(object):

    """Class for handling Workspaces operations."""

    def __init__(self, smartsheet_obj):
        """Init Workspaces with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def copy_workspace(self, workspace_id, container_destination_obj,
                       include=None, skip_remap=None):
        """Create a copy of the specified Workspace.

        Args:
            workspace_id (int): Workspace ID
            container_destination_obj (ContainerDestination): Container Destination object.
            include (list[str]): A comma-separated list of optional elements to copy. Valid list values:

                data

                attachments

                discussions

                cellLinks

                forms

                brand

                shares

                **all** - specify a value of \"all\" to include everything.

        Cell history will not be copied, regardless of which **include** parameter values are specified.
            skip_remap (list[str]): A comma separated list of references to NOT re-map for the newly created resource.
            Valid list items: cellLinks, reports, sheetHyperlinks, sights

        Returns:
            Result
        """
        _op = fresh_operation('copy_workspace')
        _op['method'] = 'POST'
        _op['path'] = '/workspaces/' + str(workspace_id) + '/copy'
        _op['query_params']['include'] = include
        _op['query_params']['skipRemap'] = skip_remap
        _op['json'] = container_destination_obj
        # filter before we go
        _op['json'].pre_request_filter = 'copy_workspace'

        expected = ['Result', 'Workspace']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def create_folder_in_workspace(self, workspace_id, folder_obj):
        """Creates a Folder in the specified Workspace

        Args:
            workspace_id (int): Workspace ID
            folder_obj (Folder): Folder object.

        Returns:
            Result
        """
        if isinstance(folder_obj, str):
            folder_obj = Folder({
                'name': folder_obj
            })

        _op = fresh_operation('create_folder_in_workspace')
        _op['method'] = 'POST'
        _op['path'] = '/workspaces/' + str(workspace_id) + '/folders'
        _op['json'] = folder_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_folder_in_workspace'

        expected = ['Result', 'Folder']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def create_sheet_in_workspace(self, workspace_id, sheet_obj):
        """Create a Sheet from scratch at the top-level of the specified
        Workspace.

        Args:
            workspace_id (int): Workspace ID
            sheet_obj (Sheet): Sheet object.

        Returns:
            Result
        """
        _op = fresh_operation('create_sheet_in_workspace')
        _op['method'] = 'POST'
        _op['path'] = '/workspaces/' + str(workspace_id) + '/sheets'
        _op['json'] = sheet_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_sheet_in_workspace'

        expected = ['Result', 'Sheet']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    # pylint: disable=invalid-name
    def create_sheet_in_workspace_from_template(self, workspace_id,
                                                sheet_obj, include=None):
        """Create a Sheet in the specified Workspace from the specified Template.

        The Sheet object should be limited to the following
        attributes:

        name (required): need not be unique.
        fromId (required): the ID of the Template to use in creating the
        Sheet.

        The optional Include parameter is a list of elements to copy from
        the Template. It may include: data, attachments, discussions,
        cellLinks, forms

        Args:
            workspace_id (int): Workspace ID
            sheet_obj (Sheet): Sheet object.
            include (list[str]): A list of optional elements
                to include from the source Template. Valid list values:
                data, attachments, discussions, cellLinks, forms.

        Returns:
            Result
        """
        _op = fresh_operation('create_sheet_in_workspace_from_template')
        _op['method'] = 'POST'
        _op['path'] = '/workspaces/' + str(workspace_id) + '/sheets'
        _op['query_params']['include'] = include
        _op['json'] = sheet_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_sheet_in_workspace_from_template'

        expected = ['Result', 'Sheet']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    # pylint: enable=invalid-name

    def create_workspace(self, workspace_obj):
        """Create a Workspace.

        Args:
            workspace_obj (Workspace): A Workspace object.

        Returns:
            Result
        """
        _op = fresh_operation('create_workspace')
        _op['method'] = 'POST'
        _op['path'] = '/workspaces'
        _op['json'] = workspace_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_workspace'

        expected = ['Result', 'Workspace']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_share(self, workspace_id, share_id):
        """Delete the Share specified.

        Args:
            workspace_id (int): Workspace ID
            share_id (str): Share ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_share')
        _op['method'] = 'DELETE'
        _op['path'] = '/workspaces/' + str(workspace_id) + '/shares/' + str(
            share_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_workspace(self, workspace_id):
        """Delete the specified Workspace and its contents.

        Args:
            workspace_id (int): Workspace ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_workspace')
        _op['method'] = 'DELETE'
        _op['path'] = '/workspaces/' + str(workspace_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_share(self, workspace_id, share_id):
        """Get the specified Share.

        Args:
            workspace_id (int): Workspace ID
            share_id (str): Share ID

        Returns:
            Share
        """
        _op = fresh_operation('get_share')
        _op['method'] = 'GET'
        _op['path'] = '/workspaces/' + str(workspace_id) + '/shares/' + str(
            share_id)

        expected = 'Share'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_workspace(self, workspace_id, load_all=False, include=None):
        """Get the specified Workspace and list its contents.

        Get the specified Workspace and list its contents. By
        default, this operation only returns top-level items in the
        Workspace. To load all of the contents, including nested Folders,
        include the **loadAll** parameter with a value of `true`.

        Args:
            workspace_id (int): Workspace ID
            load_all (bool): Load all contents, including
                nested items.
            include (list[str]): A comma-separated list of
                optional elements to include in the response. Valid list
                values: ownerInfo, source.

        Returns:
            Workspace
        """
        _op = fresh_operation('get_workspace')
        _op['method'] = 'GET'
        _op['path'] = '/workspaces/' + str(workspace_id)
        _op['query_params']['loadAll'] = load_all
        _op['query_params']['include'] = include

        expected = 'Workspace'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_folders(self, workspace_id, page_size=100, page=1,
                     include_all=False):
        """Get a list of top-level child Folders within the specified
        Workspace.

        Args:
            workspace_id (int): Workspace ID
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_folders')
        _op['method'] = 'GET'
        _op['path'] = '/workspaces/' + str(workspace_id) + '/folders'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Folder']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_shares(self, workspace_id, include_workspace_shares=False):
        """Get a list of all Users and Groups to whom the specified Workspace
        is shared, and their access level.

        Args:
            workspace_id (int): Workspace ID

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_shares')
        _op['method'] = 'GET'
        _op['path'] = '/workspaces/' + str(workspace_id) + '/shares'
        if include_workspace_shares:
            _op['query_params']['include'] = 'workspaceShares'

        expected = ['IndexResult', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_workspaces(self, page_size=100, page=1, include_all=False):
        """Get the list of Workspaces the authenticated User may access.

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
        _op = fresh_operation('list_workspaces')
        _op['method'] = 'GET'
        _op['path'] = '/workspaces'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Workspace']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def share_workspace(self, workspace_id, share_obj, send_email=False):
        """Share a Workspace with the specified Users and Groups.

        Args:
            workspace_id (int): Workspace ID
            share_obj (Share): Share object.
            send_email (bool): Either true or false to
                indicate whether or not to notify the user by email. Default
                is false.

        Returns:
            Result
        """
        _op = fresh_operation('share_workspace')
        _op['method'] = 'POST'
        _op['path'] = '/workspaces/' + str(workspace_id) + '/shares'
        _op['query_params']['sendEmail'] = send_email
        _op['json'] = share_obj
        # filter before we go
        _op['json'].pre_request_filter = 'share_workspace'

        expected = ['Result', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_share(self, workspace_id, share_id, share_obj):
        """Update the access level of a User or Group for the specified
        Workspace.

        Args:
            workspace_id (int): Workspace ID
            share_id (str): Share ID
            share_obj (Share): Share object.

        Returns:
            Result
        """
        if not all(val is not None for val in ['workspace_id', 'share_id',
                                               'share_obj']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('update_share')
        _op['method'] = 'PUT'
        _op['path'] = '/workspaces/' + str(workspace_id) + '/shares/' + str(
            share_id)
        _op['json'] = share_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_share'

        expected = ['Result', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_workspace(self, workspace_id, workspace_obj):
        """Update the specified Workspace.

        Args:
            workspace_id (int): Workspace ID
            workspace_obj (Workspace): A Workspace object.

        Returns:
            Result
        """
        _op = fresh_operation('update_workspace')
        _op['method'] = 'PUT'
        _op['path'] = '/workspaces/' + str(workspace_id)
        _op['json'] = workspace_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_workspace'

        expected = ['Result', 'Workspace']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
