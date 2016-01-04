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
from .models.sheet import Sheet
import logging
import os.path
import six
from . import fresh_operation


class Home(object):

    """Class for handling Home operations."""

    def __init__(self, smartsheet_obj):
        """Init Home with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def create_folder(self, folder_obj):
        """Creates a Folder in the user's Sheets folder (Home).

        Args:
            folder_obj (Folder): Folder object.

        Returns:
            Result
        """
        if isinstance(folder_obj, str):
            folder_obj = Folder({
                'name': folder_obj
            })

        _op = fresh_operation('create_folder')
        _op['method'] = 'POST'
        _op['path'] = '/home/folders'
        _op['json'] = folder_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_folder'

        expected = ['Result', 'Folder']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def create_sheet(self, sheet_obj):
        """Create a Sheet from scratch in the user's Sheets folder within
        Home.

        Args:
            sheet_obj (Sheet): Sheet object.

        Returns:
            Result
        """
        if isinstance(sheet_obj, dict):
            sheet_obj = Sheet(sheet_obj)

        _op = fresh_operation('create_sheet')
        _op['method'] = 'POST'
        _op['path'] = '/sheets'
        _op['json'] = sheet_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_sheet'

        expected = ['Result', 'Sheet']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def create_sheet_from_template(self, sheet_obj, include=None):
        """Create a Sheet in the Sheets folder from the specified Template.

        The Sheet object should be limited to the following
        attributes:

        name (required): need not be unique.
        fromId (required): the ID of the Template to use in creating the
        Sheet.

        The optional Include parameter is a list of elements to copy from
        the Template. It may include: data, attachments, discussions,
        cellLinks, forms

        Args:
            sheet_obj (Sheet): Sheet object.
            include (list[str]): A list of optional elements
                to include from the source Template. Valid list values:
                data, attachments, discussions, cellLinks, forms.

        Returns:
            Result
        """
        _op = fresh_operation('create_sheet_from_template')
        _op['method'] = 'POST'
        _op['path'] = '/sheets'
        _op['query_params']['include'] = include
        _op['json'] = sheet_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_sheet_from_template'

        expected = ['Result', 'Sheet']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_all_contents(self, include=None):
        """Get a nested list of all Home objects, including Sheets,
        Workspaces, Folders, Reports and Templates.

        Args:
            include (list[str]): A comma-separated list of
                optional elements to include in the response. Valid list
                values: ownerInfo, source.

        Returns:
            Home
        """
        _op = fresh_operation('list_all_contents')
        _op['method'] = 'GET'
        _op['path'] = '/home'
        _op['query_params']['include'] = include

        expected = 'Home'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_folders(self, page_size=100, page=1, include_all=False):
        """Gets a list of top-level child Folders within the user's Sheets
        folder.

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
        _op = fresh_operation('list_folders')
        _op['method'] = 'GET'
        _op['path'] = '/home/folders'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Folder']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
