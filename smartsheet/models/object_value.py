# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
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

import json
import six

from .explicit_null import ExplicitNull
from ..util import get_child_properties
from ..util import serialize

DATE = 1
DATETIME = 2
ABSTRACT_DATETIME = 3
CONTACT = 4
DURATION = 5
PREDECESSOR_LIST = 6
MULTI_CONTACT = 7
MULTI_PICKLIST = 8
NUMBER = 9
BOOLEAN = 10
STRING = 11

OBJECT_VALUE = {
    'object_type': [
        'DATE',
        'DATETIME',
        'ABSTRACT_DATETIME',
        'CONTACT',
        'DURATION',
        'PREDECESSOR_LIST',
        'MULTI_CONTACT',
        'MULTI_PICKLIST'
    ]}

_typeToName = {
    DATE: 'DATE',
    DATETIME: 'DATETIME',
    ABSTRACT_DATETIME: 'ABSTRACT_DATETIME',
    CONTACT: 'CONTACT',
    DURATION: 'DURATION',
    PREDECESSOR_LIST: 'PREDECESSOR_LIST',
    MULTI_CONTACT: 'MULTI_CONTACT',
    MULTI_PICKLIST: 'MULTI_PICKLIST'
}

_nameToType = {
    'DATE': DATE,
    'DATETIME': DATETIME,
    'ABSTRACT_DATETIME': ABSTRACT_DATETIME,
    'CONTACT': CONTACT,
    'DURATION': DURATION,
    'PREDECESSOR_LIST': PREDECESSOR_LIST,
    'MULTI_CONTACT': MULTI_CONTACT,
    'MULTI_PICKLIST': MULTI_PICKLIST
}


def enum_object_value_type(object_type=None):
    return _nameToType.get(object_type)


class ObjectValue(object):
    """Smartsheet ObjectValue data model."""

    def __init__(self, object_type=None, base_obj=None):
        """Initialize the ObjectValue model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._object_type = object_type

        self.__initialized = True

    @property
    def object_type(self):
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        if isinstance(value, six.string_types):
            self._object_type = _nameToType.get(value)
        else:
            self._object_type = value

    def serialize(self):
        # when serializing an objectValue object, change objectType to a string value
        retval = {}
        prop_list = get_child_properties(self)
        for prop in prop_list:
            prop_name = prop[0]
            camel_case = prop[1]
            prop_value = getattr(self, prop_name)
            if prop_value is not None:
                serialized = serialize(prop_value)
                if isinstance(serialized, ExplicitNull):  # object forcing serialization of a null
                    retval[camel_case] = None
                elif serialized is not None:
                    retval[camel_case] = serialized

        retval['objectType'] = _typeToName.get(self._object_type)
        return retval

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
