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

from __future__ import absolute_import
import logging
from .models import JSONObject
from . import fresh_operation


class Passthrough(object):

    """Class for handling Sheets operations."""

    def __init__(self, smartsheet_obj):
        """Init Sheets with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def get(self, endpoint, query_params=None):
        """Issue a GET request on the specified URL.

        Args:
            endpoint (str): Endpoint URL (relative to base), e.g. '/sheets'
            query_params (dict): Optional dictionary of additional query parameters

        Returns:
            JSONObject
        """
        _op = fresh_operation('get_passthrough')
        _op['method'] = 'GET'
        _op['path'] = endpoint
        _op['query_params'] = query_params

        expected = 'JSONObject'

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def post(self, endpoint, payload, query_params=None):
        """Issue a POST request on the specified URL.

        Args:
            endpoint (str): Endpoint URL (relative to base), e.g. '/sheets'
            payload (str, dict, or JSONObject): JSON payload
            query_params (dict): Optional dictionary of additional query parameters

        Returns:
            JSONObject
        """
        _op = fresh_operation('post_passthrough')
        _op['method'] = 'POST'
        _op['path'] = endpoint
        if not isinstance(payload, JSONObject):
            payload = JSONObject(payload)
        _op['json'] = payload
        _op['query_params'] = query_params

        expected = 'JSONObject'

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def put(self, endpoint, payload, query_params=None ):
        """Issue a PUT request on the specified URL.

        Args:
            endpoint (str): Endpoint URL (relative to base), e.g. '/sheets/{id}'
            payload (str, dict or JSONObject): JSON payload
            query_params (dict): Optional dictionary of additional query parameters

        Returns:
            JSONObject
        """
        _op = fresh_operation('put_passthrough')
        _op['method'] = 'PUT'
        _op['path'] = endpoint
        if not isinstance(payload, JSONObject):
            payload = JSONObject(payload)
        _op['json'] = payload
        _op['query_params'] = query_params

        expected = 'JSONObject'

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete(self, endpoint):
        """Issue a DELETE request on the specified URL.

        Args:
            endpoint (str): Endpoint URL (relative to base), e.g. '/sheets/{id}'

        Returns:
            JSONObject
        """
        _op = fresh_operation('get_passthrough')
        _op['method'] = 'DELETE'
        _op['path'] = endpoint

        expected = 'JSONObject'

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
