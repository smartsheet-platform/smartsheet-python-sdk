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

# pylint: disable=no-member
# known issue regarding ssl module and pylint.

import ssl
import certifi

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

_TRUSTED_CERT_FILE = certifi.where()


class _SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       cert_reqs=ssl.CERT_REQUIRED,
                                       ca_certs=_TRUSTED_CERT_FILE,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def pinned_session(pool_maxsize=8):
    http_adapter = _SSLAdapter(pool_connections=4,
                               pool_maxsize=pool_maxsize)

    _session = requests.session()
    _session.hooks = {'response': redact_token}
    _session.mount('https://', http_adapter)

    return _session

def redact_token(res, *args, **kwargs):
    if 'Authorization' in res.request.headers:
        res.request.headers.update({'Authorization': '[redacted]'})
    return res
