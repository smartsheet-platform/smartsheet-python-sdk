'''
Library for working with Smartsheet's version 1.1 API.

This is HORRIBLY incomplete at the moment.

Author:  Scott Wimer <scott.wimer@smartsheet.com>
'''

import httplib2
import json


from .cell import (CellTypes)

from .base import (ContainedThing, maybeAssignFromDict)
from .smartsheet_exceptions import OperationOnDiscardedObject


class Column(ContainedThing, object):
    '''
    Track the details, but not data, of a column in a Sheet.
    Many of the fields are optional.
    '''
    # TODO:  Should the Column know the URL path to change itself?
    # I think probably so.
    field_names = '''id index title primary type options hidden symbol
                    systemColumnType autoNumberFormat tags width format
                    filter'''.split()
    # TODO:  Track separately the set of fields that are user setable.
    # Those are the ones that __init__ should accept.
    # There might actually be three sets of fields:
    #   * All the fields
    #   * Fields settable at Column creation time
    #   * Fields that are mutable
    # We might then have different flatten() implementations for new Columns
    # and Column change requests.

    def __init__(self, title, index=-1, type=CellTypes.TextNumber,
            primary=False, symbol=None, options=None, systemColumnType=None,
            autoNumberFormat=None, width=None, sheet=None):
        '''
        The Column attributes that can be set when creating a Column are
        available via initialization.
        '''
        self._title = title
        self._type = type
        self._primary = primary
        self._options = options or []
        self._symbol = symbol
        self._systemColumnType = systemColumnType
        self._autoNumberFormat = autoNumberFormat
        self._width = width
        self.sheet = sheet
        self._id = -1           # Undefined except by API
        self._index = index
        self._hidden = False    # Undefined except by API
        self._tags = []         # Undefined except by API
        self._format = None     # Undefined except by API
        self._filter = None
        self.parent = sheet
        self.fields = {}
        self._discarded = False

    @classmethod
    def newFromAPI(cls, fields, sheet):
        col = Column(title=fields['title'], type=fields['type'],
                primary=fields.get('primary', False),
                symbol=fields.get('symbol', None),
                options=fields.get('options', list()),
                systemColumnType=fields.get('systemColumnType', None),
                autoNumberFormat=fields.get('autoNumberFormat', None),
                width=fields.get('width', None), sheet=sheet)
        col._id = fields['id']
        col._index = fields['index']
        maybeAssignFromDict(fields, col, 'hidden')
        maybeAssignFromDict(fields, col, 'tags')
        maybeAssignFromDict(fields, col, 'format')
        maybeAssignFromDict(fields, col, 'filter')
        col.fields = fields
        return col

    @property
    def title(self):
        self.errorIfDiscarded()
        return self._title

    @title.setter
    def title(self, value):
        self.errorIfDiscarded()
        self._title = value

    @property
    def type(self):
        self.errorIfDiscarded()
        return self._type

    @type.setter
    def type(self, value):
        self.errorIfDiscarded()
        self._type = value

    @property
    def primary(self):
        self.errorIfDiscarded()
        return self._primary

    @property
    def options(self):
        self.errorIfDiscarded()
        return self._options

    @options.setter
    def options(self, value):
        self.errorIfDiscarded()
        self._options = value

    @property
    def symbol(self):
        self.errorIfDiscarded()
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        self.errorIfDiscarded()
        self._symbol = value

    @property
    def systemColumnType(self):
        self.errorIfDiscarded()
        return self._systemColumnType

    @systemColumnType.setter
    def systemColumnType(self, value):
        self.errorIfDiscarded()
        self._systemColumnType = value

    @property
    def autoNumberFormat(self):
        self.errorIfDiscarded()
        return self._autoNumberFormat

    @autoNumberFormat.setter
    def autoNumberFormat(self, value):
        self.errorIfDiscarded()
        self._autoNumberFormat = value

    @property
    def width(self):
        self.errorIfDiscarded()
        return self._width

    @width.setter
    def width(self, value):
        self.errorIfDiscarded()
        self._width = value

    @property
    def id(self):
        self.errorIfDiscarded()
        return self._id

    @property
    def index(self):
        self.errorIfDiscarded()
        return self._index

    @index.setter
    def index(self, value):
        self.errorIfDiscarded()
        self._index = value

    @property
    def hidden(self):
        self.errorIfDiscarded()
        return self._hidden

    @property
    def tags(self):
        self.errorIfDiscarded()
        return self._tags

    @property
    def format(self):
        self.errorIfDiscarded()
        return self._format

    @format.setter
    def format(self, value):
        self.errorIfDiscarded()
        self._format = value

    @property
    def filter(self):
        self.errorIfDiscarded()
        return self._filter

    def flatten(self):
        '''
        Return a dict containing the attributes used by the API for Columns.
        Use flattenForInsert() if inserting the Column into the Sheet.
        '''
        self.errorIfDiscarded()
        acc = {'title': self.title, 'type': self.type }
        if self.index >= 0:
            acc['index'] = self.index
        if self.primary:
            acc['primary'] = True
        if self.symbol:
            acc['symbol'] = self.symbol
        if self.options:
            acc['options'] = self.options
        if self.systemColumnType:
            acc['systemColumnType'] = self.systemColumnType
        if self.autoNumberFormat:
            acc['autoNumberFormat'] = self.autoNumberFormat
        if self.width is not None:
            acc['width'] = self.width
        if self.format is not None:
            acc['format'] = self.format
        return acc

    def flattenForInsert(self):
        '''
        Return a dict of Column attributes suitable for insertion into a Sheet.
        Notably, this dict does not include the 'format' attribute.
        '''
        self.errorIfDiscarded()
        acc = self.flatten()
        if 'format' in acc:
            self.logger.warn("Collumn attribute 'format' not supported when "
                    "inserting a Column into a sheet.  Expect an error.  "
                    "Column: %s", str(self))
        return acc

    def flattenForUpdate(self):
        '''
        Return a dict of Column attributes suitable for update.
        Notably, this dict contains the Sheet ID and omits the 'primary'
        attribute.
        '''
        self.errorIfDiscarded()
        acc = self.flatten()
        if self.sheet is not None and self.sheet.id is not None:
            acc['sheetId'] = self.sheet.id
        if 'primary' in acc:
            del acc['primary']
        return acc

    def discard(self):
        '''
        Discard this Column, further operations on it will fail.
        '''
        self._discarded = True
        return

    def delete(self, client=None):
        '''
        Delete this Column.
        '''
        self.errorIfDiscarded()
        column_id = self.id
        self.discard()
        return self.sheet.deleteColumnById(self, column_id, client=client)

    def update(self):
        '''
        Update this Column.
        '''
        self.errorIfDiscarded()
        return self.sheet.updateColumn(self)

    def errorIfDiscarded(self):
        if self._discarded:
            raise OperationOnDiscardedObject("Column was discarded.")

    def __str__(self):
        self.errorIfDiscarded()
        return '<Column id:%d index:%r title:%r type:%r>' % (
                self.id, self.index, self.title, self.type)

    def __repr__(self):
        self.errorIfDiscarded()
        return str(self)

