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


class Contacts(object):

    """Class for handling Contacts operations."""

    def __init__(self, smartsheet_obj):
        """Init Contacts with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def get_contact(self, contact_id):
        """Get the specified Contact.

        Args:
            contact_id (str): Contact ID

        Returns:
            Contact
        """
        _op = fresh_operation('get_contact')
        _op['method'] = 'GET'
        _op['path'] = '/contacts/' + str(contact_id)

        expected = 'Contact'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_contacts(self, page_size=None, page=None, include_all=None):
        """Get a list of the user's Smartsheet Contacts.

        Args:
            page_size (int): The maximum number of items to
                return per page.
            page (int): Which page to return.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_contacts')
        _op['method'] = 'GET'
        _op['path'] = '/contacts'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Contact']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
