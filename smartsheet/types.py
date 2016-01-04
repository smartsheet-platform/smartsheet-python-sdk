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

import collections
import importlib
import json
import logging
import six


class TypedList(collections.MutableSequence):

    def __init__(self, item_type):
        self.item_type = item_type
        self.__store = []
        self._log = logging.getLogger(__name__)
        if isinstance(self.item_type, six.string_types):
            self.item_type = getattr(
                importlib.import_module(
                    __package__ + '.models.' + self.item_type.lower()
                ), self.item_type)
        self._log.debug('TypedList item type is %s', self.item_type)

    def __len__(self):
        return len(self.__store)

    def __getitem__(self, idx):
        # self._log.debug('__getitem__, %s', idx)
        return self.__store[idx]

    def __setitem__(self, idx, value):
        self._log.debug('__setitem__, %s, %s', idx, value)
        self.__store[idx] = self.convert(value)

    def __delitem__(self, idx):
        del self.__store[idx]

    def insert(self, idx, value):
        self._log.debug('insert called with %s, %s', idx, value)
        self.__store.insert(idx, self.convert(value))

    def convert(self, item):
        """Convert the input item to the desired object type."""
        try:
            if isinstance(item, self.item_type):
                self._log.debug('item is %s: %s', self.item_type, item)
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

    def __repr__(self):
        tmp = json.dumps(self.__store)
        return "TypedList(item_type=%s, contents=%s)" % (self.item_type, tmp)

    def __str__(self):
        return json.dumps(self.__store)
