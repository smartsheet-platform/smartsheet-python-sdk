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

from ..util import prep
import json
import six


class ContainerDestination(object):

    """Smartsheet ContainerDestination data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ContainerDestination model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'destination_type': [
                'home',
                'workspace',
                'folder']}

        self._destination_id = None
        self._destination_type = None
        self._new_name = None

        if props:
            # account for alternate variable names from raw API response
            if 'destinationId' in props:
                self.destination_id = props['destinationId']
            if 'destination_id' in props:
                self.destination_id = props['destination_id']
            if 'destinationType' in props:
                self.destination_type = props['destinationType']
            if 'destination_type' in props:
                self.destination_type = props[
                    'destination_type']
            if 'newName' in props:
                self.new_name = props['newName']
            if 'new_name' in props:
                self.new_name = props['new_name']

    @property
    def destination_id(self):
        return self._destination_id

    @destination_id.setter
    def destination_id(self, value):
        if isinstance(value, six.integer_types):
            self._destination_id = value

    @property
    def destination_type(self):
        return self._destination_type

    @destination_type.setter
    def destination_type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['destination_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for ContainerDestination`destination_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['destination_type']))
            self._destination_type = value

    @property
    def new_name(self):
        return self._new_name

    @new_name.setter
    def new_name(self, value):
        if isinstance(value, six.string_types):
            self._new_name = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'destinationId': prep(self._destination_id),
            'destinationType': prep(self._destination_type),
            'newName': prep(self._new_name)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
