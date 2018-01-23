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

import six
import json

from .auto_number_format import AutoNumberFormat
from .contact_option import ContactOption
from ..types import TypedList
from ..util import serialize
from ..util import deserialize


class Column(object):

    """Smartsheet Column data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Column model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'symbol': [
                'STAR',
                'FLAG',
                'HARVEY_BALLS',
                'PRIORITY',
                'RYG',
                'PRIORITY_HML',
                'DECISION_SYMBOLS',
                'DECISION_SHAPES',
                'VCR',
                'RYGB',
                'RYGG',
                'WEATHER',
                'PROGRESS',
                'ARROWS_3_WAY',
                'ARROWS_4_WAY',
                'ARROWS_5_WAY',
                'DIRECTIONS_3_WAY',
                'DIRECTIONS_4_WAY',
                'SKI',
                'SIGNAL',
                'STAR_RATING',
                'HEARTS',
                'MONEY',
                'EFFORT',
                'PAIN'],
            'system_column_type': [
                'AUTO_NUMBER',
                'MODIFIED_DATE',
                'MODIFIED_BY',
                'CREATED_DATE',
                'CREATED_BY'],
            '_type': [
                'TEXT_NUMBER',
                'DATE',
                'DATETIME',
                'CONTACT_LIST',
                'CHECKBOX',
                'PICKLIST',
                'DURATION',
                'PREDECESSOR',
                'ABSTRACT_DATETIME']}

        self._auto_number_format = None
        self._contact_options = TypedList(ContactOption)
        self._format_ = None
        self._hidden = None
        self._id_ = None
        self._index = None
        self._locked = None
        self._locked_for_user = None
        self._options = TypedList(str)
        self._primary = None
        self._symbol = None
        self._system_column_type = None
        self._tags = TypedList(str)
        self._title = None
        self._type_ = None
        self._width = None
        self._validation = None

        if props:
            deserialize(self, props)
        
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'format':
            return self.format_
        elif key == 'id':
            return self.id_
        elif key == 'type':
            return self.type_
        else:
            raise AttributeError(key)
        
    def __setattr__(self, key, value):
        if key == 'format':
            self.format_ = value 
        elif key == 'id':
            self.id_ = value
        elif key == 'type':
            self.type_ = value
        else:
            super(Column, self).__setattr__(key, value)
    
    @property
    def auto_number_format(self):
        return self._auto_number_format

    @auto_number_format.setter
    def auto_number_format(self, value):
        if isinstance(value, AutoNumberFormat):
            self._auto_number_format = value
        else:
            self._auto_number_format = AutoNumberFormat(value, self._base)

    @property
    def contact_options(self):
        return self._contact_options

    @contact_options.setter
    def contact_options(self, value):
        self._contact_options.load(value)

    @property
    def format_(self):
        return self._format_

    @format_.setter
    def format_(self, value):
        if isinstance(value, six.string_types):
            self._format_ = value

    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, value):
        if isinstance(value, bool):
            self._hidden = value

    @property
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, value):
        if isinstance(value, six.integer_types):
            self._id_ = value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if isinstance(value, six.integer_types):
            self._index = value

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        if isinstance(value, bool):
            self._locked = value

    @property
    def locked_for_user(self):
        return self._locked_for_user

    @locked_for_user.setter
    def locked_for_user(self, value):
        if isinstance(value, bool):
            self._locked_for_user = value

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options.load(value)

    @property
    def primary(self):
        return self._primary

    @primary.setter
    def primary(self, value):
        if isinstance(value, bool):
            self._primary = value

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['symbol']:
                raise ValueError(
                    ("`{0}` is an invalid value for Column`symbol`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['symbol']))
            self._symbol = value

    @property
    def system_column_type(self):
        return self._system_column_type

    @system_column_type.setter
    def system_column_type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['system_column_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Column`system_column_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['system_column_type']))
            self._system_column_type = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags.load(value)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, six.string_types):
            self._title = value

    @property
    def type_(self):
        return self._type_

    @type_.setter
    def type_(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Column`_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['_type']))
            self._type_ = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if isinstance(value, six.integer_types):
            self._width = value

    @property
    def validation(self):
        return self._validation

    @validation.setter
    def validation(self, value):
        if isinstance(value, bool):
            self._validation = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
