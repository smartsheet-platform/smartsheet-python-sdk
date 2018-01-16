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
from .column import Column
from .filter import Filter
from ..types import TypedList
from ..util import prep
import json
import six


class ReportColumn(Column):

    """Smartsheet ReportColumn data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ReportColumn model."""
        super(ReportColumn, self).__init__(props, base_obj)
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
            '_type': [
                'TEXT_NUMBER',
                'DATE',
                'DATETIME',
                'CONTACT_LIST',
                'CHECKBOX',
                'PICKLIST',
                'DURATION',
                'PREDECESSOR',
                'ABSTRACT_DATETIME'],
            'system_column_type': [
                'AUTO_NUMBER',
                'MODIFIED_DATE',
                'MODIFIED_BY',
                'CREATED_DATE',
                'CREATED_BY']}

        self._auto_number_format = None
        self.__filter = None
        self.__format = None
        self.__id = None
        self._hidden = None
        self._index = None
        self._locked = None
        self._locked_for_user = None
        self._options = TypedList(str)
        self._primary = None
        self._sheet_name_column = None
        self._symbol = None
        self._system_column_type = None
        self._tags = TypedList(str)
        self._title = None
        self.__type = None
        self._virtual_id = None
        self._width = None

        if props:
            # account for alternate variable names from raw API response
            if 'autoNumberFormat' in props:
                self.auto_number_format = props['autoNumberFormat']
            if 'auto_number_format' in props:
                self.auto_number_format = props['auto_number_format']
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
            if 'sheetNameColumn' in props:
                self.sheet_name_column = props['sheetNameColumn']
            if 'sheet_name_column' in props:
                self.sheet_name_column = props['sheet_name_column']
            if 'symbol' in props:
                self.symbol = props['symbol']
            if 'systemColumnType' in props:
                self.system_column_type = props['systemColumnType']
            if 'system_column_type' in props:
                self.system_column_type = props['system_column_type']
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
            if 'virtualId' in props:
                self.virtual_id = props['virtualId']
            if 'virtual_id' in props:
                self.virtual_id = props['virtual_id']
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
    def sheet_name_column(self):
        return self._sheet_name_column

    @sheet_name_column.setter
    def sheet_name_column(self, value):
        if isinstance(value, bool):
            self._sheet_name_column = value

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['symbol']:
                raise ValueError(
                    ("`{0}` is an invalid value for ReportColumn`symbol`,"
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
                    ("`{0}` is an invalid value for ReportColumn`system_column_type`,"
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
                    ("`{0}` is an invalid value for ReportColumn`_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['_type']))
            self.__type = value

    @property
    def virtual_id(self):
        return self._virtual_id

    @virtual_id.setter
    def virtual_id(self, value):
        if isinstance(value, six.integer_types):
            self._virtual_id = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if isinstance(value, six.integer_types):
            self._width = value

    def to_dict(self, op_id=None, method=None):
        parent_obj = super(ReportColumn, self).to_dict(op_id, method)
        obj = {
            'autoNumberFormat': prep(self._auto_number_format),
            'format': prep(self.__format),
            'filter': prep(self.__filter),
            'hidden': prep(self._hidden),
            'id': prep(self.__id),
            'index': prep(self._index),
            'locked': prep(self._locked),
            'lockedForUser': prep(self._locked_for_user),
            'options': prep(self._options),
            'primary': prep(self._primary),
            'sheetNameColumn': prep(self._sheet_name_column),
            'symbol': prep(self._symbol),
            'systemColumnType': prep(self._system_column_type),
            'tags': prep(self._tags),
            'title': prep(self._title),
            'type': prep(self.__type),
            'virtualId': prep(self._virtual_id),
            'width': prep(self._width)}
        combo = parent_obj.copy()
        combo.update(obj)
        return combo

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
