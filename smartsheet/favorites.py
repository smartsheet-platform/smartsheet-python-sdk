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


class Favorites(object):

    """Class for handling Favorites operations."""

    def __init__(self, smartsheet_obj):
        """Init Favorites with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def add_favorites(self, favorite_obj):
        """Add one or more items to the user's list of Favorite items.

        Adds one or more items to the user's list of Favorite
        items. This operation supports both single-object and bulk
        semantics. If called with a single Favorite object, and that
        favorite already exists, error code 1129 will be returned. If
        called with an array of Favorite objects, any objects specified in
        the array that are already marked as favorites will be ignored and
        ommitted from the response.

        Args:
            favorite_obj (list[Favorite]): Array of one or
                more Favorite objects

        Returns:
            Result
        """
        _op = fresh_operation('add_favorites')
        _op['method'] = 'POST'
        _op['path'] = '/favorites'
        _op['json'] = favorite_obj

        expected = ['Result', 'Favorite']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_favorites(self, page_size=100, page=1, include_all=False):
        """Get a list of all the user's Favorite items.

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
        _op = fresh_operation('list_favorites')
        _op['method'] = 'GET'
        _op['path'] = '/favorites'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Favorite']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def remove_favorites(self, favorite_type, object_ids):
        """Delete one or more of Favorite objects of the specified type.

        Specify a favorite type of: folder, report, sheet,
        template, workspace. The object IDs passed in will be deleted in a
        batch operation.

        Args:
            favorite_type (str): Name of favorite type to
                manipulate.
            object_ids (list[int]): a comma-separated list
                of object IDs representing the items to work on.

        Returns:
            Result
        """
        _op = fresh_operation('remove_favorites')
        _op['method'] = 'DELETE'
        _op['path'] = '/favorites/' + str(favorite_type)
        _op['query_params']['objectIds'] = object_ids

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
