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

try:
    # For Python versions 2.7 and 3.3 to 3.9, import from collections
    from collections import MutableSequence
except ImportError:
    # For Python version >= 3.10 import from collections.abc
    from collections.abc import MutableSequence

import importlib
import json
import logging
import six

from datetime import datetime
from dateutil.parser import parse
from enum import Enum


class TypedList(MutableSequence):

    def __init__(self, item_type):
        self.item_type = item_type
        self.__store = []
        self._log = logging.getLogger(__name__)
        if isinstance(self.item_type, six.string_types):
            self.item_type = getattr(
                importlib.import_module(
                    __package__ + '.models.' + self.item_type.lower()
                ), self.item_type)

    def __len__(self):
        return len(self.__store)

    def __getitem__(self, idx):
        return self.__store[idx]

    def __setitem__(self, idx, value):
        self._log.debug('__setitem__, %s, %s', idx, value)
        self.__store[idx] = self.convert(value)

    def __delitem__(self, idx):
        del self.__store[idx]

    def insert(self, idx, value):
        self.__store.insert(idx, self.convert(value))

    def convert(self, item):
        """Convert the input item to the desired object type."""
        try:
            if isinstance(item, self.item_type):
                return item
            # allow explicit null to be passed through to the list
            elif hasattr(item, 'is_explicit_null'):
                return item
        except TypeError:
            raise

        try:
            retval = self.item_type(item)
            self._log.debug('item converted to %s: %s -> %s',
                            self.item_type, item, retval)
            return retval
        except (ValueError, TypeError):
            raise ValueError(
                "Can't convert %s to %s in TypedList", item, self.item_type)

    def purge(self):
        """Zero out the underlying list object."""
        del self.__store[:]

    def to_list(self):
        return self.__store

    def load(self, value):
        if isinstance(value, list):
            self.purge()
            self.extend([
                (item if isinstance(item, self.item_type) else self.item_type(item)) for item in value
            ])
        elif isinstance(value, TypedList):
            self.purge()
            self.extend(value.to_list())
        elif isinstance(value, self.item_type):
            self.purge()
            self.append(value)
        elif hasattr(value, 'is_explicit_null'):
            self.purge()
            self.append(value)
        else:
            raise ValueError("Can't load to TypedList(%s) from '%s'", self.item_type, value)

    def __repr__(self):
        tmp = json.dumps(self.__store)
        return "TypedList(item_type=%s, contents=%s)" % (self.item_type, tmp)

    def __str__(self):
        return json.dumps(self.__store)


class TypedObject(object):

    def __init__(self, object_type):
        self.object_type = object_type
        self._value = None
        self._log = logging.getLogger(__name__)
        if isinstance(self.object_type, six.string_types):
            self.object_type = getattr(
                importlib.import_module(
                    __package__ + '.models.' + self.object_type.lower()
                ), self.object_type)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, self.object_type):
            self._value = value
        elif isinstance(value, dict):
            self._value = self.object_type(value)
        elif hasattr(value, 'is_explicit_null'):
            self._value = value
        else:
            raise ValueError("`{0}` invalid type for {1} value".format(value, self.object_type))

    def __str(self):
        return json.dumps(self._value)


class Number(object):

    def __init__(self, initial_value=None):
        self._value = None
        if initial_value:
            self.value = initial_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            self._value = None
        elif isinstance(value, (six.integer_types, float)):
            self._value = value
        else:
            raise ValueError("`{0}` invalid type for Number value".format(value))

    def __str__(self):
        return str(self.value)


class String(object):

    def __init__(self, initial_value=None, accept=None):
        self._value = None
        if initial_value:
            self.value = initial_value
        self._accept = None
        if accept:
            self.accept = accept

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            self._value = None
        elif isinstance(value, six.string_types):
            if self.accept and value not in self._accept:
                raise ValueError(
                    "`{0}` is not in accept list, must be one of {1}".format(
                        value, self.accept))
            self._value = value
        else:
            raise ValueError("`{0}` invalid type for String value".format(value))

    @property
    def accept(self):
        return self._accept

    @accept.setter
    def accept(self, value):
        if isinstance(value, list):
            self._accept = value
        elif isinstance(value, six.string_types):
            self._accept = [value]
        else:
            raise ValueError("`{0}` invalid type for accept".format(value))

    def __str__(self):
        return self._value


class Boolean(object):

    def __init__(self, initial_value=None):
        self._value = None
        if initial_value:
            self.value = initial_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            self._value = None
        elif isinstance(value, bool):
            self._value = value
        else:
            raise ValueError("`{0}` invalid type for Boolean value".format(value))

    def __str__(self):
        return str(self._value)


class Timestamp(object):

    def __init__(self, initial_value=None):
        self._value = None
        if initial_value:
            self.value = initial_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            self._value = None
        elif isinstance(value, datetime):
            self._value = value
        elif isinstance(value, six.string_types):
            value = parse(value)
            self._value = value
        else:
            raise ValueError("`{0}` invalid type for Timestamp value".format(value))

    def __str__(self):
        return str(self._value)


class EnumeratedValue(object):

    def __init__(self, enum, value=None):
        self.__enum = enum
        self._value = None
        if value:
            self.set(value)

    @property
    def value(self):
        return self._value

    def set(self, value):
        if isinstance(value, six.string_types):
            try:
                self._value = self.__enum[value]
            except KeyError:
                self._value = None
        elif isinstance(value, Enum):
            self._value = value;
        else:
            self._value = None

    def __eq__(self, other):
        if isinstance(other, Enum) or other is None:
            return self._value == other
        elif isinstance(other, six.string_types):
            return self._value == self.__enum[other]
        NotImplemented

    def __str__(self):
        if self._value is not None:
            return self._value.name
        else:
            return str(None)


class EnumeratedList(TypedList):

    def __init__(self, enum):
        super(EnumeratedList, self).__init__(EnumeratedValue)
        self.__enum = enum

    def load(self, value):
        if isinstance(value, TypedList):
            value = value.to_list()

        if isinstance(value, list):
            self.purge()
            self.extend([
                (EnumeratedValue(self.__enum, item)) for item in value
            ])
        else:
            self.purge()
            self.append(EnumeratedValue(self.__enum, value))
