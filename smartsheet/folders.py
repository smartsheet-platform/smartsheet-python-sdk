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


class Folders(object):

    """Class for handling Folders operations."""

    def __init__(self, smartsheet_obj):
        """Init Folders with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def copy_folder(self, folder_id, container_destination_obj,
                    include=None, skip_remap=None):
        """Creates a copy of the specified Folder.

        Args:
            folder_id (int): Folder ID
            container_destination_obj
                (ContainerDestination): Container Destination object.
            include (list[str]): A comma separated list of
                elements to copy. Valid list values: data, attachments,
                discussions, cellLinks, forms, all.
            skip_remap (list[str]): A comma separated list
                of references to NOT re-map for the newly created resource.
                Valid list items: cellLinks, reports, sheetHyperlinks

        Returns:
            Result
        """
        _op = fresh_operation('copy_folder')
        _op['method'] = 'POST'
        _op['path'] = '/folders/' + str(folder_id) + '/copy'
        _op['query_params']['include'] = include
        _op['query_params']['skipRemap'] = skip_remap
        _op['json'] = container_destination_obj

        expected = ['Result', 'Folder']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def create_folder_in_folder(self, folder_id, folder_obj):
        """Create a Folder in the specified Folder

        Args:
            folder_id (int): Folder ID
            folder_obj (Folder): Folder object.

        Returns:
            Result
        """
        if isinstance(folder_obj, str):
            folder_obj = Folder({
                'name': folder_obj
            })

        _op = fresh_operation('create_folder_in_folder')
        _op['method'] = 'POST'
        _op['path'] = '/folders/' + str(folder_id) + '/folders'
        _op['json'] = folder_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_folder_in_folder'

        expected = ['Result', 'Folder']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def create_sheet_in_folder(self, folder_id, sheet_obj):
        """Create a Sheet from scratch in the specified Folder.

        Args:
            folder_id (int): Folder ID
            sheet_obj (Sheet): Sheet object.

        Returns:
            Result
        """
        _op = fresh_operation('create_sheet_in_folder')
        _op['method'] = 'POST'
        _op['path'] = '/folders/' + str(folder_id) + '/sheets'
        _op['json'] = sheet_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_sheet_in_folder'

        expected = ['Result', 'Sheet']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    # pylint: disable=invalid-name
    def create_sheet_in_folder_from_template(self, folder_id, sheet_obj,
                                             include=None):
        """Create a Sheet in the specified Folder from the specified Template.

        The Sheet object should be limited to the following
        attributes:

        name (required): need not be unique.
        fromId (required): the ID of the Template to use in creating the
        Sheet.

        The optional Include parameter is a list of elements to copy from
        the Template. It may include: data, attachments, discussions,
        cellLinks, forms

        Args:
            folder_id (int): Folder ID
            sheet_obj (Sheet): Sheet object.
            include (list[str]): A list of optional elements
                to include from the source Template. Valid list values:
                data, attachments, discussions, cellLinks, forms.

        Returns:
            Result
        """
        _op = fresh_operation('create_sheet_in_folder_from_template')
        _op['method'] = 'POST'
        _op['path'] = '/folders/' + str(folder_id) + '/sheets'
        _op['query_params']['include'] = include
        _op['json'] = sheet_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_sheet_in_folder_from_template'

        expected = ['Result', 'Sheet']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    # pylint: enable=invalid-name

    def delete_folder(self, folder_id):
        """Delete the Folder (and its contents) specified in the request.

        Args:
            folder_id (int): Folder ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_folder')
        _op['method'] = 'DELETE'
        _op['path'] = '/folders/' + str(folder_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_folder(self, folder_id, include=None):
        """Get the specified Folder (and list its contents).

        Args:
            folder_id (int): Folder ID
            include (list[str]): A comma-separated list of
                optional elements to include in the response. Valid list
                values: ownerInfo, source.

        Returns:
            Folder
        """
        _op = fresh_operation('get_folder')
        _op['method'] = 'GET'
        _op['path'] = '/folders/' + str(folder_id)
        _op['query_params']['include'] = include

        expected = 'Folder'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_folders(self, folder_id, page_size=100, page=1,
                     include_all=False):
        """Get a list of top-level child Folders within the specified Folder.

        Args:
            folder_id (int): Folder ID
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
        _op['path'] = '/folders/' + str(folder_id) + '/folders'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Folder']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def move_folder(self, folder_id, container_destination_obj):
        """Moves the specified Folder to another location.

        Args:
            folder_id (int): Folder ID
            container_destination_obj
                (ContainerDestination): Container Destination object.

        Returns:
            Result
        """
        _op = fresh_operation('move_folder')
        _op['method'] = 'POST'
        _op['path'] = '/folders/' + str(folder_id) + '/move'
        _op['json'] = container_destination_obj
        # filter before we go
        _op['json'].pre_request_filter = 'move_folder'

        expected = ['Result', 'Folder']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_folder(self, folder_id, folder_obj):
        """Update the specified Folder.

        Args:
            folder_id (int): Folder ID
            folder_obj (Folder): Folder object.

        Returns:
            Result
        """
        if isinstance(folder_obj, str):
            folder_obj = Folder({
                'name': folder_obj
            })

        _op = fresh_operation('update_folder')
        _op['method'] = 'PUT'
        _op['path'] = '/folders/' + str(folder_id)
        _op['json'] = folder_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_folder'

        expected = ['Result', 'Folder']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
