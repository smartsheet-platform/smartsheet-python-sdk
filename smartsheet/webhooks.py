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

class Webhooks(object):

    """Class for handling Webhooks operations."""

    def __init__(self, smartsheet_obj):
        """Init Webhooks with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def list_webhooks(self, page_size=100, page=1,
                    include_all=False):
        """Get the list of all Webhooks the User has access to, in alphabetical
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
        _op = fresh_operation('list_webhooks')
        _op['method'] = 'GET'
        _op['path'] = '/webhooks'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Webhook']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_webhook(self, webhook_id):
        """Get the specified Webhook.

        Args:
            webhook_id (int): Webhook ID

        Returns:
            Webhook
        """
        _op = fresh_operation('get_webhook')
        _op['method'] = 'GET'
        _op['path'] = '/webhooks/' + str(webhook_id)

        expected = 'Webhook'

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def create_webhook(self, webhook_obj):
        """Creates the specified Webhook.

        Args:
            webhook_obj (Webhook): Webhook object.

        Returns:
            Result
        """
        _op = fresh_operation('create_webhook')
        _op['method'] = 'POST'
        _op['path'] = '/webhooks'
        _op['json'] = webhook_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_webhook'

        expected = ['Result', 'Webhook']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_webhook(self, webhook_id, webhook_obj):
        """Updates the specified Webhook.

        Args:
            webhook_id (int): Webhook ID
            webhook_obj (Webhook): Webhook object.

        Returns:
            Result
        """
        _op = fresh_operation('update_webhook')
        _op['method'] = 'PUT'
        _op['path'] = '/webhooks/' + str(webhook_id)
        _op['json'] = webhook_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_webhook'

        expected = ['Result', 'Webhook']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_webhook(self, webhook_id):
        """Delete the specified Webhook.

        Args:
            webhook_id (int): Webhook ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_webhook')
        _op['method'] = 'DELETE'
        _op['path'] = '/webhooks/' + str(webhook_id)

        expected = 'Result'

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def reset_shared_secret(self, webhook_id):
        """Resets the shared secret for the specified Webhook.

        Args:
            webhook_id (int): Webhook ID

        Returns:
            Webhook
        """
        _op = fresh_operation('reset_webhook')
        _op['method'] = 'POST'
        _op['path'] = '/webhooks/' + str(webhook_id) + '/resetsharedsecret'

        expected = ['Result', 'WebhookSecret']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response