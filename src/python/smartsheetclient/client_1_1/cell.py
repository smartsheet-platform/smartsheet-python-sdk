'''
Library for working with Smartsheet's version 1.1 API.

This is HORRIBLY incomplete at the moment.

Author:  Scott Wimer <scott.wimer@smartsheet.com>
'''

import sys
import json
from .smartsheet_exceptions import (SmartsheetClientError, BadCellData,
        DeprecatedAttribute, OperationOnDiscardedObject)
from .base import ContainedThing


class CellTypes(object):
    # TODO: Should this be an enum class?
    TextNumber = 'TEXT_NUMBER'
    Picklist = 'PICKLIST'
    Date = 'DATE'
    ContactList = 'CONTACT_LIST'
    Checkbox = 'CHECKBOX'
    EmptyCell = 'EMPTY_CELL'   # This must not be sent to the server.



class CellHyperlink(object):
    '''
    Represents a cell hyperlink to a URL, Sheet, or Report.
    '''
    def __init__(self, url=None, sheetId=None, reportId=None):
        if 1 != len([x for x in (url, sheetId, reportId) if x is not None]):
            raise SmartsheetClientError("Must specify one of url, sheetId, " +
                    "or reportId for a CellHyperlink")
        self.url = url
        self.sheetId = sheetId
        self.reportId = reportId
        self.fields = {}

    @classmethod
    def newFromAPI(cls, fields):
        link = CellHyperlink(
                url=fields.get('url', None),
                sheetId=fields.get('sheetId', None),
                reportId=fields.get('reportId', None))
        link.fields = fields
        return link


    def flatten(self):
        '''
        "Flatten" the object into a dict.
        '''
        acc = {}
        if self.url is not None:
            acc['url'] = self.url
        elif self.sheetId is not None:
            acc['sheetId'] = self.sheetId
        elif self.reportId is not None:
            acc['reportId'] = self.reportId
        return acc

    def __str__(self):
        return ('<CellHyperlink: url: %r  sheetId: %r  reportId: %r' %
                (self.url, self.sheetId, self.reportId))
    
    def __repr__(self):
        return str(self)



class CellLinkStatus(object):
    '''
    The status of a CellLink (in or out).
    '''
    OK = 'OK'
    BROKEN = 'BROKEN'
    INACCESSIBLE = 'INACCESSIBLE'
    NOT_SHARED = 'NOT_SHARED'
    BLOCKED = 'BLOCKED'
    CIRCULAR = 'CIRCULAR'
    INVALID = 'INVALID'
    DISABLED = 'DISABLED'

    @classmethod
    def isValid(cls, status_code):
        return status_code.upper() in [cls.OK, cls.BROKEN, cls.INACCESSIBLE,
                cls.NOT_SHARED, cls.BLOCKED, cls.CIRCULAR, cls.INVALID,
                cls.DISABLED]


class CellLinkIn(object):
    '''
    A link from a Cell to a Cell in a different Sheet.
    '''
    def __init__(self, sheetId, rowId, columnId, status):
        if not CellLinkStatus.isValid(status):
            raise BadCellData("CellLinkIn status: %r not valid status code." %
                    status)
        self.sheetId = sheetId
        self.rowId = rowId
        self._columnId = columnId
        self.status = status
        self.fields = {}

    @classmethod
    def newFromAPI(cls, fields):
        link = CellLinkIn(fields['sheetId'], fields['rowId'],
                fields['columnId'], fields['status'])
        link.fields = fields
        return link

    def flatten(self):
        '''"Flatten" the object into a dict.'''
        acc = { 'sheetId': self.sheetId,
                'rowId': self.rowId,
                'columnId': self.columnId }
        return acc

    def __str__(self):
        return ('<CellLinkIn: sheetId: %r  rowId: %r  columnId: %r status: %r' %
                (self.sheetId, self.rowId, self.columnId, self.status))

    def __repr__(self):
        return str(self)



class Cell(ContainedThing, object):
    '''
    A Cell on a Row of a Sheet.
    A Cell consists of two types of information, the first is structural and
    the second is value.  A Cell's structure indicates its Row and Column,
    while its value contains its value and displayValue, as well as
    format, formula, and links (hyperlinks and cell links).

    A Cell may be empty, which would be the case in a sparse Sheet, in which
    case the Cell would have structural data, but no value information.

    A Cell does not have a unique ID, instead, each Cell is identified by the
    tuple of (row ID, column ID).
    '''
    Max_Cell_Size = 4000
    Max_Display_Len = 10

    def __init__(self, row, column, value, type=None,
            displayValue=None, hyperlink=None, linkInFromCell=None,
            format=None, link=None, isDirty=True, strict=True):
        '''
        Initialize a new Cell.
        Note that the library user is not able to assign all of the same
        attributes that the API can.

        When a Cell is saved, the type is not passed to the API server, it is
        it is for the benefit of the caller and is used to format the Cell's
        value for saving.

        The displayValue is set by when the Cell is constructed by the server.
        It may also be set by .assign(), but the value chosen by .assign() is
        not authoritative.  When a Cell is saved, the authoritative
        displayValue is set by the server.

        If isDirty is True, then the Cell needs to be saved.  If immediate
        is True, then the Cell will be saved immediately (rather than lazily
        with the Row or Sheet).

        By default, Cells request that the server perform strict validation on
        their value when saved.  This can be overriden by setting strict=False,
        or by specifying strict=False when saving the Cell (or updating, saving
        or adding the Row that the Cell is on).


        @param row The Row this Cell is on.
        @param column The Column this Cell is on.
        @param value The value for this Cell.
        @param type The type of the Cell, uses the Column.type if None.
        @param displayValue The string displayed for this Cell.
        @param hyperlink A CellHyperlink if this Cell links "out"
        @param linkInFromCell A CellLinkIn if this Cell is a link target.
        @param format The format code for this Cell's displayValue.
        @param link Deprecated cell linking attribute.
        @param isDirty True if this Cell's value is not from the server.
        @param strict True to request strict Cell-data validation by the server.
        '''
        self.parent = row
        if link:
            # TODO:  Add Row number and Column index to this message.
            self.logger.warning("Got a 'link' attribute for a Cell")

        if type is None:
            type = column.type

        if hyperlink is not None and not isinstance(hyperlink, CellHyperlink):
            err = "hyperlink parameter must be None or a CellHyperlink object"
            self.logger.error("%s, got: %r", err, hyperlink)
            raise SmartsheetClientError(err)

        if (linkInFromCell is not None and 
                not isinstance(linkInFromCell, CellLinkIn)):
            err = "linkInFromCell parameter must be None or a CellLinkIn object"
            self.logger.error("%s, got: %r", err, linkInFromCell)
            raise SmartsheetClientError(err)

        self._row = row
        self._column = column
        self._columnId = column.id
        self._value = value
        self._displayValue = displayValue
        self.type = type
        self.hyperlink = hyperlink
        self._linkInFromCell = linkInFromCell
        self._linksOutToCells = None # Not settable by library user.
        self.format = format
        self._strict = strict;
        self._formula = None        # Not settable by library user.
        self.link = link            # Deprecated, but can be set by API server.
        self._modifiedAt = None     # Not settable by library user.
        self._modifiedBy = None    # Not settable by library user.
        self._isDirty = isDirty
        self.change = None
        self._fields = {}            # Only set by newFromAPI()
        self.isDeleted = False
        self._discarded = False

    @classmethod
    def newFromAPI(cls, fields, row):
        '''
        Create a new instance from the dict of values from the API.
        '''
        column = row.getColumnById(fields['columnId'])
        if fields.get('hyperlink', None) is not None:
            hyperlink = CellHyperlink.newFromAPI(fields['hyperlink'])
        else:
            hyperlink = None
        if fields.get('linkInFromCell', None) is not None:
            linkInFromCell = CellLinkIn.newFromAPI(fields['linkInFromCell'])
        else:
            linkInFromCell = None

        cell = Cell(row, column, fields.get('value', None), type=fields['type'],
                displayValue=fields.get('displayValue', None),
                hyperlink=hyperlink,
                linkInFromCell=linkInFromCell,
                format=fields.get('format', None),
                link=fields.get('link', None), isDirty=False)
        # Set the attributes that are not exposed by __init__().
        cell._fields = fields
        cell._formula = fields.get('formula', None)
        cell._linksOutToCells = fields.get('linksOutToCells', None),
        cell._modifiedAt = fields.get('modifiedAt', None)
        if 'modifiedBy' in fields:
            cell._modifiedBy = SimpleUser(fields.get('modifiedBy'))
        else:
            cell._modifiedBy = None
        return cell

    @classmethod
    def makeEmptyCell(cls, row, column):
        '''
        Creat a new, empty Cell at the specified position.

        @param row The Row this Cell is on.
        @param column The Column this Cell is in.
        @return A new, empty Cell.
        '''
        return Cell(row, column, None, type=CellTypes.EmptyCell, isDirty=False)

    @property
    def row(self):
        self.errorIfDiscarded()
        return self._row

    @property
    def column(self):
        self.errorIfDiscarded()
        return self._column

    @property
    def value(self):
        '''
        Return the value of the Cell.
        The "value" of a Cell is something of a slippery concept.
        If a Cell is a TEXT_NUMBER Cell, then the value is either a string
        or a numeric type.  If it is a numeric type, then we return the
        numeric type, otherwise we return the string as represented by the
        displayValue from the API.

        For more control over the value obtained from the cell, the
        `realValue` and `displayValue` methods can be used to explicitly
        fetch the value or the displayValue from the API.
        '''
        self.errorIfDiscarded()
        # It would be really nice if this could sensibly handle the fact
        # that a cell containing numeric data will have a string for its
        # displayValue.  It's quite probably that the caller would rather
        # get the numeric value as a numeric type.
        if (self._displayValue is not None and self._value is not None and
                isinstance(self._value, (int, float))):
            return self._value
        if self._displayValue is None and self._value is not None:
            return self._value
        return self._displayValue

    @value.setter
    def value(self, new_value):
        '''
        Assign a new value to the Cell.
        The new value is presumed to be the same type as the original value,
        and the assignment (on the server) does not occur immediately.
        If more control over the assignment process is needed, use the
        `assign` method below.
        '''
        self.errorIfDiscarded()
        self.assign(new_value)
        return

    @property
    def realValue(self):
        '''
        Read the underlying value for the cell.
        If the Cell contains a formula, this will return the formula, instead
        of its computed value (which can be gotten via the `value` property).
        '''
        self.errorIfDiscarded()
        if self.formula:
            return self.formula
        return self._value

    @property
    def displayValue(self):
        self.errorIfDiscarded()
        return self._displayValue

    def assign(self, new_value, displayValue=None, hyperlink=None,
            linkInFromCell=None, strict=True):
        '''
        Assign a new value to the Cell.

        On the server, Cell data is changed a Row-at-a-time.  To save just the
        changes to this Cell, set immediate to True and propagate to False.

        A linkInFromCell can only be set on a Cell in a Row that already
        exists on the server.  Attempting to do so on a new Row raises a
        SheetIntegrityError.

        @param new_value The new value for the Cell.
        @param displayValue The string value of the Cell prior to save().
        @param strict True to request stict processing on save.
        @param hyperlink The CellHyperlink to set.
        @param linkInFromCell The CellLinkIn to set.
        @param strict True to request strict Cell-data validation by the server.
        @return The new Cell.
        @raises SheetIntegrityError
        '''
        self.errorIfDiscarded()

        # TODO:  Treat new_value==None as a delete
        # TODO:  Should a deleted Cell have an attribute indicating that?

        if linkInFromCell and self.row.isNew:
            err = ("%s.assign() linkInFromCell can only be set in a Cell "
                    "on a Row that has been saved to the server, not on a "
                    "new Row." % self)
            self.logger.error(err)
            raise SheetIntegrityError(err)

        new_type = self.type
        if new_type == CellTypes.EmptyCell:
            new_type = self.column.type
        new_cell = Cell(self.row, self.column, new_value, type=new_type,
                displayValue=displayValue, hyperlink=hyperlink,
                linkInFromCell=linkInFromCell, format=self.format,
                isDirty=True)

        new_cell.row.replaceCell(self, new_cell)
        self.discard()
        return new_cell

    def setFormat(self, format, immediate=False, propagate=True):
        '''
        Change the format of the cell.
        '''
        # NOTE: The save data for this requires the value, so capture it.
        raise NotImplementedError("Setting Cell format is not implemented yet")

    def discard(self):
        '''
        Mark this Cell as discarded, further operations on it will fail.
        '''
        self._discarded = True
        return

    def delete(self, immediate=False, propagate=True, strict=True):
        '''
        Delete this Cell.
        @param immediate Apply this update to the sheet immediately.
        @param propagate True to save other changed Cells on this Row.
        @param strict True to request strict Cell-data validation by the server.
        '''
        self.errorIfDiscarded()
        # Deletion works by sending the server a blank Cell.
        blank_cell = Cell(self.row, self.column, None)
        blank_cell.row.replaceCell(self, blank_cell)
        if immediate:
            blank_cell.save(propagate=propagate, strict=strict)
        self.discard()
        return

    @property
    def rowId(self):
        self.errorIfDiscarded()
        return self.row.id

    @property
    def columnId(self):
        self.errorIfDiscarded()
        return self._column.id

    @property
    def linkInFromCell(self):
        self.errorIfDiscarded()
        return self._linkInFromCell

    @property
    def linksOutToCells(self):
        self.errorIfDiscarded()
        return self._linksOutToCells

    @property
    def formula(self):
        self.errorIfDiscarded()
        return self._formula

    @property
    def modifiedAt(self):
        self.errorIfDiscarded()
        return self._modifiedAt

    @property
    def modifiedBy(self):
        self.errorIfDiscarded()
        return self._modifiedBy

    @property
    def strict(self):
        self.errorIfDiscarded()
        return self._strict

    @property
    def isDirty(self):
        return self._isDirty

    @property
    def fields(self):
        self.errorIfDiscarded()
        return self._fields

    def save(self, propagate=True, strict=None):
        '''
        Save the Cell, and potentially any other change Cells on its Row.

        Saving Cell data actually occurs at the Row-level.  While it is
        possible to "apply" multiple changed Cells on a Row as a series
        of saves, doing so ignores the fact that the server responds to each
        save with the new version of the Row.  This means that applying
        multiple changes through multiple saves can result in the local
        state of the Row's structure being out of sync with the structure
        of the Row according to the server.

        To avoid this risk of Row-structure out-of-syncness, saving a Cell
        on a Row results in the replacement of the local copy of the Row.
        By default, any other changed Cells on the Row will also be saved.
        The propagate flag can be set to False to ensure that only this Cell
        will be saved (any other local changes to the Cell's Row will be lost.

        @param propagate True to save any other change Cells on the Row.
        @param strict True to request strict Cell-data validation by server.
        '''
        self.errorIfDiscarded()
        if propagate:
            self.row.save(strict=strict)
        else:
            self.row.save(cell=self, strict=strict)
        return

    def flatten(self, strict=None):
        '''
        Return a flattened form of this Cell, suitable for saving.
        Note that if the Cell has a linkInFromCell, it can't be saved to a new
        Row, it can only be saved into an existing Row.

        @param strict True to request strict Cell-data validation by server.
        @return Dict containing the contents of this Cell.
        '''
        self.errorIfDiscarded()
        acc = {}
        if self.type == CellTypes.EmptyCell:
            return acc

        acc['columnId'] = self.columnId
        acc['value'] = self.value
        if strict is not None:
            acc['strict'] = strict
        else:
            acc['strict'] = self.strict
        if self.format is not None:
            acc['format'] = self.format
        if self.hyperlink is not None:
            acc['hyperlink'] = self.hyperlink.flatten()
        if self.linkInFromCell is not None:
            acc['linkInFromCell'] = self.linkInFromCell.flatten()
        return acc

    def flattenForInsert(self, strict=None):
        '''
        Return a flattened form of this Cell for Row insertion.
        @param strict True to request strict Cell-data validation by server.
        @return Dict containing contents of this Cell (minus linkInFromCell).
        '''
        self.errorIfDiscarded()
        acc = self.flatten(strict=strict)
        if 'linkInFromCell' in acc:
            self.logger.warn("linkInFromCell attribute not supported on Cell "
                    "when inserting a new Row, expect an error.  Cell: %s",
                    str(self))
            del acc['linkInFromCell']
        return acc

    def fetchHistory(self):
        '''
        Fetch the history of the Cell.

        @return List of Cells, one for each version of this Cell.
        '''
        # TODO: Add documentation about exceptions raised.
        # TODO: Consider making Cell.__getitem__ operate over Cell history.
        # That would let a Sheet be treated as a cube: rows x columns x history
        # That operational model might give rise to some interesting uses.
        self.errorIfDiscarded()
        path = '/sheet/%s/row/%s/column/%s/history' % (
                str(self.row.sheet.id), str(self.rowId), str(self.columnId))
        name = "%r.fetchHistory()" % self
        body = self.client.GET(path, name=name)
        return [Cell.newFromAPI(c, self.row) for c in body]

    def errorIfDiscarded(self):
        if self._discarded:
            raise OperationOnDiscardedObject("Cell was discarded.")

    def __str__(self):
        self.errorIfDiscarded()
        if self._displayValue is not None:
            return self._displayValue
        return str(self.value).decode('utf-8')

    def __int__(self):
        '''Try to convert the value to an int.'''
        self.errorIfDiscarded()
        return int(self.value)

    def __long__(self):
        '''Try to convert the value to a long.'''
        self.errorIfDiscarded()
        if sys.version_info.major == 2:
            return long(self.value)
        return int(self.value)

    def __float__(self):
        '''Try to convert the value to a float.'''
        self.errorIfDiscarded()
        return float(self.value)

    # This is a really, quick and dirty approach to supporting math operations
    # when the Cell happens to contain a numeric value.
    # TODO: In particular, the division and mod operations need to be reviewed.
    # TODO: Add support for +=, -=, etc. (__iadd__, __isub__, etc.)
    # TODO: Consider adding support for bitwise operations.
    # These "forward" ops support Cell + Cell or Cell + 5.
    def __add__(self, other): return self.value + other
    def __sub__(self, other): return self.value - other
    def __mul__(self, other): return self.value * other
    def __floordiv__(self, other): return self.value / other
    def __mod__(self, other): return self.value % other
    def __divmod__(self, other): return divmod(self.value, other)
    def __pow__(self, other): return pow(self.value, other)
    def __div__(self, other): return self.value / other

    # The swapped numeric ops support 5 + Cell.
    def __radd__(self, other): return other + self.value    # no-different
    def __rsub__(self, other): return other - self.value
    def __rmul__(self, other): return other * self.value    # no different
    def __rfloordiv__(self, other): return other / self.value
    def __rmod__(self, other): return other % self.value
    def __rdivmod__(self, other): return divmod(other, self.value)
    def __rpow__(self, other): return pow(other, self.value)
    def __rdiv__(self, other): return other / self.value

    # Unary operations
    def __neg__(self): return (- self.value)
    def __pos__(self): return (+ self.value)
    def __abs__(self): return abs(self.value)
    def __invert__(self): return ~self.value

    def __repr__(self):
        self.errorIfDiscarded()
        # TODO:  It would be nice if this specified the Column index also.
        return '<Cell rowId:%r, columnId:%r, type:%r value=%r>' % (
                self.rowId, self.columnId, self.type,
                string_trim(self.value, self.Max_Display_Len))



def string_trim(value, max_len):
    '''
    Return a version of value that fits within max_len characters.
    '''
    if len(str(value)) > max_len:
        return str(value)[:max_len-3] + '...'
    else:
        return value


