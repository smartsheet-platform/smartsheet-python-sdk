'''
Library for working with Smartsheet's version 1.1 API.

This is HORRIBLY incomplete at the moment.

Author:  Scott Wimer <scott.wimer@smartsheet.com>
'''

import httplib2
import json


from cell import (CellTypes)

from base import (ContainedThing, maybeAssignFromDict)


class Column(ContainedThing, object):
    '''
    Track the details, but not data, of a column in a Sheet.
    Many of the fields are optional.
    '''
    # TODO:  Make the Column type immutable.
    # Along with that, provide a mechanism to change the attributes that
    # can be changed.
    # TODO:  Should the Column know the URL path to change itself?
    # I think probably so.
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
        self._hidden = False
        self._tags = []
        self._format = None
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
                width=fields.get('width', None),
                sheet=sheet)
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
        return self._title

    @property
    def type(self):
        return self._type

    @property
    def primary(self):
        return self._primary

    @property
    def options(self):
        return self._options

    @property
    def symbol(self):
        return self._symbol

    @property
    def systemColumnType(self):
        return self._systemColumnType

    @property
    def autoNumberFormat(self):
        return self._autoNumberFormat

    @property
    def width(self):
        return self._width

    @property
    def id(self):
        return self._id

    @property
    def index(self):
        return self._index

    @property
    def hidden(self):
        return self._hidden

    @property
    def tags(self):
        return self._tags

    @property
    def format(self):
        return self._format

    @property
    def filter(self):
        return self._filter

    def flatten(self):
        '''
        Return a dict containing the attributes used by the API for Columns.
        Use flattenForInsert() if inserting the Column into the Sheet.
        '''
        acc = {'title': self.title, 'type': self.type }
        if self.index:
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
            acc['autoNumberFormat'] = self.autonumberFormat
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
        acc = self.flatten()
        if 'format' in acc:
            self.logger.warn("Collumn attribute 'format' not supported when "
                    "inserting a Column into a sheet.  Expect an error.  "
                    "Column: %s", str(self))
        return acc

    def discard(self):
        '''
        Discard this Column, further operations on it should fail.
        '''
        self._discarded = True
        return

    def delete(self, client=None):
        '''
        Delete this Column.
        '''
        column_id = self.id
        self.discard()
        return self.sheet.deleteColumnById(self, column_id, client=client)

    def __str__(self):
        return '<Column id:%d index:%r title:%r type:%r>' % (
                self.id, self.index, self.title, self.type)

    def __repr__(self):
        return str(self)

