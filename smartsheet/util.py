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
from datetime import date
from datetime import datetime
import warnings
import functools

LOG = logging.getLogger('util')


def prep(prop, op_id=None, method=None):
    """Serialize a value for JSON transformation."""
    if isinstance(prop, (datetime, date)):
        retval = prop.isoformat()

    elif hasattr(prop, 'to_list'):
        # Export TypedList recursively
        proplist = prop.to_list()
        retval = [prep(x) for x in proplist]

    elif hasattr(prop, 'to_dict'):
        retval = prop.to_dict(op_id, method)

    elif isinstance(prop, list):
        retval = [(x.to_dict(op_id, method) if hasattr(x, 'to_dict') else x) for x in prop]

    else:
        retval = prop

    return retval


def dump_message_headers(request):
    bytearr = bytearray()
    headers = request.headers.copy()
    for name, value in headers.items():
        bytearr.extend(format_header(name, value))
    return bytearr.decode('utf-8')

def coerce_to_bytes(data):
    if not isinstance(data, bytes) and hasattr(data, 'encode'):
        data = data.encode('utf-8')
    return data

def format_header(name, value):
    return (coerce_to_bytes(name) + b': ' + coerce_to_bytes(value) +
            b'\r\n')

def is_multipart(request):
    headers = dump_message_headers(request)
    if 'Content-Type: multipart/form-data' in headers:
        return True
    return False

def deprecated(func):
    '''This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.'''
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning) #turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__), category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning) #reset filter
        return func(*args, **kwargs)

    return new_func
