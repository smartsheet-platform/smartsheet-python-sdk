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

from .auto_number_format import AutoNumberFormat
from .contact import Contact
from .enums import ColumnType, Symbol, SystemColumnType
from ..types import *
from ..util import serialize
from ..util import deserialize


class Column(object):

    """Smartsheet Column data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Column model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._auto_number_format = TypedObject(AutoNumberFormat)
        self._contact_options = TypedList(Contact)
        self._description = String()
        self._format_ = String()
        self._formula = String()
        self._hidden = Boolean()
        self._id_ = Number()
        self._index = Number()
        self._locked = Boolean()
        self._locked_for_user = Boolean()
        self._options = TypedList(str)
        self._primary = Boolean()
        self._symbol = EnumeratedValue(Symbol)
        self._system_column_type = EnumeratedValue(SystemColumnType)
        self._tags = TypedList(str)
        self._title = String()
        self._type_ = EnumeratedValue(ColumnType)
        self._width = Number()
        self._validation = Boolean()
        self._version = Number()

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
        return self._auto_number_format.value

    @auto_number_format.setter
    def auto_number_format(self, value):
        self._auto_number_format.value = value

    @property
    def contact_options(self):
        return self._contact_options

    @contact_options.setter
    def contact_options(self, value):
        self._contact_options.load(value)

    @property
    def description(self):
        return self._description.value

    @description.setter
    def description(self, value):
        self._description.value = value

    @property
    def format_(self):
        return self._format_.value

    @format_.setter
    def format_(self, value):
        self._format_.value = value

    @property
    def formula(self):
        return self._formula.value

    @formula.setter
    def formula(self, value):
        self._formula.value = value

    @property
    def hidden(self):
        return self._hidden.value

    @hidden.setter
    def hidden(self, value):
        self._hidden.value = value

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def index(self):
        return self._index.value

    @index.setter
    def index(self, value):
        self._index.value = value

    @property
    def locked(self):
        return self._locked.value

    @locked.setter
    def locked(self, value):
        self._locked.value = value

    @property
    def locked_for_user(self):
        return self._locked_for_user.value

    @locked_for_user.setter
    def locked_for_user(self, value):
        self._locked_for_user.value = value

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options.load(value)

    @property
    def primary(self):
        return self._primary.value

    @primary.setter
    def primary(self, value):
        self._primary.value = value

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        self._symbol.set(value)

    @property
    def system_column_type(self):
        return self._system_column_type

    @system_column_type.setter
    def system_column_type(self, value):
        self._system_column_type.set(value)

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags.load(value)

    @property
    def title(self):
        return self._title.value

    @title.setter
    def title(self, value):
        self._title.value = value

    @property
    def type_(self):
        return self._type_

    @type_.setter
    def type_(self, value):
        self._type_.set(value)

    @property
    def width(self):
        return self._width.value

    @width.setter
    def width(self, value):
        self._width.value = value

    @property
    def validation(self):
        return self._validation.value

    @validation.setter
    def validation(self, value):
        self._validation.value = value

    @property
    def version(self):
        return self._version.value

    @version.setter
    def version(self, value):
        self._version.value = value;

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
