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
from datetime import datetime
from . import fresh_operation


class Search(object):

    """Class for handling Search operations."""

    def __init__(self, smartsheet_obj):
        """Init Search with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def search(self, query, include=None, location=None, modified_since=None, scopes=None):
        """Search all Sheets the User can access for the specified text.

        Args:
            query (str): Text with which to perform the search.
            include (str): when specified with a value of 'favoriteFlag',
                response indicates which returned items are favorites
            location (str): when specified with a value of 'personalWorkspace',
                limits the response to only those items in the user's Workspaces
            modified_since (str): includes items that are modified on or after the
                date and time specified
            scopes (str): comma-separated list of search filters:
                attachments
                cellData
                comments
                folderNames
                profileFields
                reportNames
                sheetNames
                sightNames
                templateNames
                workspaceNames

        Returns:
            SearchResult
        """
        _op = fresh_operation('search')
        _op['method'] = 'GET'
        _op['path'] = '/search'
        _op['query_params']['query'] = query
        _op['query_params']['include'] = include
        _op['query_params']['location'] = location
        _op['query_params']['scopes'] = scopes
        if isinstance(modified_since, datetime):
            _op['query_params']['modifiedSince'] = modified_since.isoformat()

        expected = 'SearchResult'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def search_sheet(self, sheet_id, query):
        """Search the specified Sheet for the specified text.

        Args:
            sheet_id (int): Sheet ID
            query (str): Text with which to perform the
                search.

        Returns:
            SearchResult
        """
        _op = fresh_operation('search_sheet')
        _op['method'] = 'GET'
        _op['path'] = '/search/sheets/' + str(sheet_id)
        _op['query_params']['query'] = query

        expected = 'SearchResult'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
