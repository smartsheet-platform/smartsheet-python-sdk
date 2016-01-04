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


class Token(object):

    """Class for handling Token operations."""

    def __init__(self, smartsheet_obj):
        """Init Token with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def get_access_token(self, client_id, code, _hash, redirect_uri=None):
        """Get an access token, as part of the OAuth process. For more
        information, see [OAuth
        Flow](http://smartsheet-platform.github.io/api-docs/index.html#oauth-flow)

        Args:
            client_id (str)
            code (str)
            _hash (str): SHA-256 hash of your `app_secret`
                concatenated with a pipe and the authorization `code`.
            redirect_uri (str): Redirect URL registered for
                your app, including protocol (e.g. \"http://\"); if not
                provided, the redirect URL set during registration is used.

        Returns:
            AccessToken
        """
        if not all(val is not None for val in ['client_id', 'code', '_hash']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('get_access_token')
        _op['method'] = 'POST'
        _op['path'] = '/token'
        _op['form_data'] = {}
        _op['form_data']['grant_type'] = 'authorization_code'
        _op['form_data']['client_id'] = client_id
        _op['form_data']['code'] = code
        _op['form_data']['redirect_uri'] = redirect_uri
        _op['form_data']['hash'] = _hash
        _op['auth_settings'] = None

        expected = 'AccessToken'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def refresh_access_token(self, client_id, refresh_token, _hash,
                             redirect_uri=None):
        """Refresh an access token, as part of the OAuth process. For more
        information, see [OAuth
        Flow](http://smartsheet-platform.github.io/api-docs/index.html#oauth-flow)

        Args:
            client_id (str)
            refresh_token (str)
            _hash (str): SHA-256 hash of your `app_secret`
                concatenated with a pipe and the refresh token value.
            redirect_uri (str): Redirect URL registered for
                your app, including protocol (e.g. \"http://\"); if not
                provided, the redirect URL set during registration is used.

        Returns:
            AccessToken
        """
        if not all(val is not None for val in ['client_id', 'refresh_token',
                                               '_hash']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('refresh_access_token')
        _op['method'] = 'POST'
        _op['path'] = '/token'
        _op['form_data'] = {}
        _op['form_data']['grant_type'] = 'refresh_token'
        _op['form_data']['client_id'] = client_id
        _op['form_data']['refresh_token'] = refresh_token
        _op['form_data']['redirect_uri'] = redirect_uri
        _op['form_data']['hash'] = _hash

        expected = 'AccessToken'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def revoke_access_token(self):
        """Revoke the access token used to make the request.

        Revoke the access token used to make the request. The
        access token will no longer be valid, and subsequent API calls
        using the token will fail.
        Returns:
            Result
        """
        _op = fresh_operation('revoke_access_token')
        _op['method'] = 'DELETE'
        _op['path'] = '/token'

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
