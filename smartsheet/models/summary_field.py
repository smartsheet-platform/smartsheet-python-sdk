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

from .contact import Contact
from .enums.column_type import ColumnType
from .hyperlink import Hyperlink
from .image import Image
from .user import User
from ..object_value import assign_to_object_value
from ..types import *
from ..util import serialize
from ..util import deserialize


class SummaryField(object):

    """Smartsheet SummaryField data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SummaryField model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._contact_options = TypedList(Contact)
        self._created_at = Timestamp()
        self._created_by = TypedObject(User)
        self._display_value = String()
        self._format_ = String()
        self._formula = String()
        self._hyperlink = TypedObject(Hyperlink)
        self._id_ = Number()
        self._image = TypedObject(Image)
        self._index = Number()
        self._locked = Boolean()
        self._locked_for_user = Boolean()
        self._modified_at = Timestamp()
        self._modified_by = TypedObject(User)
        self._object_value = None
        self._options = TypedList(str)
        self._symbol = String()
        self._title = String()
        self._type_ = EnumeratedValue(ColumnType)
        self._validation = Boolean()

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
            super(SummaryField, self).__setattr__(key, value)

    @property
    def contact_options(self):
        return self._contact_options

    @contact_options.setter
    def contact_options(self, value):
        self._contact_options.load(value)

    @property
    def created_at(self):
        return self._created_at.value

    @created_at.setter
    def created_at(self, value):
        self._created_at.value = value

    @property
    def created_by(self):
        return self._created_by.value

    @created_by.setter
    def created_by(self, value):
        self._created_by.value = value

    @property
    def display_value(self):
        return self._display_value.value

    @display_value.setter
    def display_value(self, value):
        self._display_value.value = value

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
    def hyperlink(self):
        return self._hyperlink.value

    @hyperlink.setter
    def hyperlink(self, value):
        self._hyperlink.value = value

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def image(self):
        return self._image.value

    @image.setter
    def image(self, value):
        self._image.value = value

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
    def modified_at(self):
        return self._modified_at.value

    @modified_at.setter
    def modified_at(self, value):
        self._modified_at.value = value

    @property
    def modified_by(self):
        return self._modified_by.value

    @created_by.setter
    def modified_by(self, value):
        self._modified_by.value = value

    @property
    def object_value(self):
        return self._object_value

    @object_value.setter
    def object_value(self, value):
        self._object_value = assign_to_object_value(value)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options.load(value)

    @property
    def symbol(self):
        return self._symbol.value

    @symbol.setter
    def symbol(self, value):
        self._symbol.value = value

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
    def validation(self):
        return self._validation.value

    @validation.setter
    def validation(self, value):
        self._validation.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
