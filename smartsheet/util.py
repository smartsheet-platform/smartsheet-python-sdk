# Smartsheet Python SDK.
#
# Copyright 2018 Smartsheet.com, Inc.
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
import warnings
import functools
import re
import six
import inspect

from datetime import date
from datetime import datetime
from .types import TypedList
from .types import EnumeratedValue

_log = logging.getLogger(__name__)
_primitive_types = (six.string_types, six.integer_types, float, bool)
_list_types = (TypedList, list)


def _camel_to_underscore(name):
    camel_pat = re.compile(r'([A-Z])')
    return camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)


def _underscore_to_camel(name):
    under_pat = re.compile(r'_([a-z])')
    return under_pat.sub(lambda x: x.group(1).upper(), name)


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


def get_child_properties(obj):
    retval = []
    prop_list = inspect.getmembers(obj.__class__, inspect.isdatadescriptor)
    for prop in prop_list:
        if isinstance(prop[1], property):
            prop_name = prop[0]
            camel_case = _underscore_to_camel(prop_name)
            camel_case = camel_case.rstrip('_')  # trim trailing '_' from props with names eq. to built-ins
            retval.append((prop_name, camel_case))

    return retval


def serialize(obj):

    retval = None

    if hasattr(obj, 'serialize'):
        retval = obj.serialize()

    elif isinstance(obj, datetime):
        retval = obj.isoformat() + 'Z'

    elif isinstance(obj, date):
        retval = obj.isoformat()

    elif isinstance(obj, _primitive_types):
        retval = obj

    elif hasattr(obj, 'is_explicit_null'):
        retval = obj

    elif isinstance(obj, EnumeratedValue):
        if obj.value is not None:
            retval = obj.value.name

    elif isinstance(obj, _list_types):
        if len(obj):
            retval = []
            for x in obj:
                serialized = serialize(x)
                if not hasattr(serialized, 'is_explicit_null'):
                    retval.append(serialized)
    else:
        retval = {}
        prop_list = get_child_properties(obj)
        for prop in prop_list:
            prop_name = prop[0]
            camel_case = prop[1]
            prop_value = getattr(obj, prop_name)
            if prop_value is not None:
                serialized = serialize(prop_value)
                if hasattr(serialized, 'is_explicit_null'):  # object forcing serialization of a null
                    retval[camel_case] = None
                elif serialized is not None:
                    retval[camel_case] = serialized

    return retval


def deserialize(obj, props):
    if isinstance(props, dict):
        for key, value in props.items():
            key_ = _camel_to_underscore(key)
            if hasattr(obj, key_):
                setattr(obj, key_, value)

            else:
                _log.debug('object \'%s\' is missing property \'%s\'', obj.__class__.__name__, key_)


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
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func
