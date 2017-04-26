# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
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

from .auto_number_format import AutoNumberFormat
from .filter import Filter
from .contact_option import ContactOption
from ..types import TypedList
from ..util import prep
import json
import logging
import six

class Column(object):

    """Smartsheet Column data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Column model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

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
        self.__filter = None
        self.__format = None
        self._hidden = None
        self.__id = None
        self._index = None
        self._locked = None
        self._locked_for_user = None
        self._options = TypedList(str)
        self._primary = None
        self._symbol = None
        self._system_column_type = None
        self._tags = TypedList(str)
        self._title = None
        self.__type = None
        self._width = None

        if props:
            # account for alternate variable names from raw API response
            if 'autoNumberFormat' in props:
                self.auto_number_format = props[
                    'autoNumberFormat']
            if 'auto_number_format' in props:
                self.auto_number_format = props[
                    'auto_number_format']
            if 'contactOptions' in props:
                self.contact_options = props['contactOptions']
            if 'contact_options' in props:
                self.contact_options = props['contact_options']
            if 'filter' in props:
                self._filter = props['filter']
            if '_filter' in props:
                self._filter = props['_filter']
            if 'format' in props:
                self._format = props['format']
            if '_format' in props:
                self._format = props['_format']
            if 'hidden' in props:
                self.hidden = props['hidden']
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'index' in props:
                self.index = props['index']
            if 'locked' in props:
                self.locked = props['locked']
            if 'lockedForUser' in props:
                self.locked_for_user = props['lockedForUser']
            if 'locked_for_user' in props:
                self.locked_for_user = props['locked_for_user']
            if 'options' in props:
                self.options = props['options']
            if 'primary' in props:
                self.primary = props['primary']
            if 'symbol' in props:
                self.symbol = props['symbol']
            if 'systemColumnType' in props:
                self.system_column_type = props[
                    'systemColumnType']
            if 'system_column_type' in props:
                self.system_column_type = props[
                    'system_column_type']
            if 'tags' in props:
                self.tags = props['tags']
            if 'title' in props:
                self.title = props['title']
            if 'type' in props:
                self._type = props['type']
            if '_type' in props:
                self._type = props['_type']
            if 'width' in props:
                self.width = props['width']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'filter':
            return self._filter
        elif key == 'format':
            return self._format
        elif key == 'id':
            return self._id
        elif key == 'type':
            return self._type
        else:
            raise AttributeError(key)

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
        if isinstance(value, list):
            self._contact_options.purge()
            self._contact_options.extend([
                (ContactOption(x)
                 if not isinstance(x, ContactOption) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._contact_options.purge()
            self._contact_options = value.to_list()
        elif isinstance(value, ContactOption):
            self._contact_options.purge()
            self._contact_options.append(value)

    @property
    def _filter(self):
        return self.__filter

    @_filter.setter
    def _filter(self, value):
        if isinstance(value, Filter):
            self.__filter = value
        else:
            self.__filter = Filter(value, self._base)

    @property
    def _format(self):
        return self.__format

    @_format.setter
    def _format(self, value):
        if isinstance(value, six.string_types):
            self.__format = value

    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, value):
        if isinstance(value, bool):
            self._hidden = value

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

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
        if isinstance(value, list):
            self._options.purge()
            self._options.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._options.purge()
            self._options = value.to_list()
        elif isinstance(value, str):
            self._options.purge()
            self._options.append(value)

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
        if isinstance(value, list):
            self._tags.purge()
            self._tags.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._tags.purge()
            self._tags = value.to_list()
        elif isinstance(value, str):
            self._tags.purge()
            self._tags.append(value)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, six.string_types):
            self._title = value

    @property
    def _type(self):
        return self.__type

    @_type.setter
    def _type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Column`_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['_type']))
            self.__type = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if isinstance(value, six.integer_types):
            self._width = value

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        if self.auto_number_format is not None:
            self.auto_number_format.pre_request_filter = value
        if self._filter is not None:
            self._filter.pre_request_filter = value
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        req_filter = self.pre_request_filter
        if req_filter:
            if self.auto_number_format is not None:
                self.auto_number_format.pre_request_filter = req_filter
            if self._filter is not None:
                self._filter.pre_request_filter = req_filter

        obj = {
            'autoNumberFormat': prep(self._auto_number_format),
            'contactOptions': prep(self._contact_options),
            'filter': prep(self.__filter),
            'format': prep(self.__format),
            'hidden': prep(self._hidden),
            'id': prep(self.__id),
            'index': prep(self._index),
            'locked': prep(self._locked),
            'lockedForUser': prep(self._locked_for_user),
            'options': prep(self._options),
            'primary': prep(self._primary),
            'symbol': prep(self._symbol),
            'systemColumnType': prep(self._system_column_type),
            'tags': prep(self._tags),
            'title': prep(self._title),
            'type': prep(self.__type),
            'width': prep(self._width)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'add_columns':
            permitted = ['title', 'type', 'symbol',
                         'options', 'index', 'systemColumnType', 'autoNumberFormat',
                         'width', 'locked', 'hidden', 'contactOptions']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'create_sheet':
            permitted = ['title', 'primary', 'type',
                         'symbol', 'options', 'systemColumnType', 'autoNumberFormat',
                         'width', 'hidden', 'contactOptions']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'create_sheet_in_folder':
            permitted = ['title', 'primary', 'type',
                         'symbol', 'options', 'systemColumnType', 'autoNumberFormat',
                         'width', 'hidden', 'contactOptions']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'create_sheet_in_workspace':
            permitted = ['title', 'primary', 'type',
                         'symbol', 'options', 'systemColumnType', 'autoNumberFormat',
                         'width', 'hidden', 'contactOptions']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'update_column':
            permitted = ['index', 'title', 'type', 'symbol',
                         'options', 'systemColumnType', 'autoNumberFormat', 'width',
                         'locked', 'hidden', 'contactOptions']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

            if self.type != 'PICKLIST':
                del obj['options']

        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
