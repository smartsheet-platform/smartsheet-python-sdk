# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2019 Smartsheet.com, Inc.
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

from ..types import *
from ..util import serialize
from ..util import deserialize


class EventResult(object):

    """Smartsheet EventResult data model."""

    def __init__(self, props=None, dynamic_data_type=None, base_obj=None):
        """Initialize the EventResult model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._dynamic_data_type = None
        if dynamic_data_type is not None:
            self._dynamic_data_type = dynamic_data_type

        self._data = TypedList(object)
        self._more_available = Boolean()
        self._next_stream_position = String()

        if props:
            deserialize(self, props)
            # account for alternate variable names from raw API response

        # requests package Response object
        self.request_response = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        class_ = getattr(importlib.import_module(
            'smartsheet.models'), self._dynamic_data_type)
        if isinstance(value, list):
            self._data = [class_(x, self._base) for x in value]
        else:
            self._data = class_(value, self._base)

    @property
    def more_available(self):
        return self._more_available.value

    @more_available.setter
    def more_available(self, value):
        self._more_available.value = value

    @property
    def next_stream_position(self):
        return self._next_stream_position.value

    @next_stream_position.setter
    def next_stream_position(self, value):
        self._next_stream_position.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
