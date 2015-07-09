'''
Library for working with Smartsheet's version 1.1 API.

This is HORRIBLY incomplete at the moment.

Author:  Scott Wimer <scott.wimer@smartsheet.com>
'''

import json

from .base import (maybeAssignFromDict, isList, isScalar, isGenerator,
        isMapping, isInteger)
from .cell import (Cell, CellTypes)
from .attachment import Attachment, AttachPoint
from .discussion import Discussion
from .smartsheet_exceptions import (SmartsheetClientError, UnknownColumnId,
        OperationOnDiscardedObject, SheetIntegrityError)
from .base import ContainedThing


# FIXME:  Something like this class seems necessary, but this isn't right.
# Perhaps callers should create a RowPositionProperties instance that will
# just "do the right thing" once it has been validated.
# That class could accept either Rows or Row IDs for the parent and sibling
# values.  Even better, it could own the work of flattening this information
# into something that the server can consume.
class RowPositionProperties(object):
    '''
    Rows can be moved based on the following properties.
    Certain properties mutually exclusive, while others can be combined.
    '''
    Top = 'toTop'
    Bottom = 'toBottom'
    Parent = 'parentId'
    Sibling = 'siblingId'
    Default_Position = Bottom

    def __init__(self, sheet, position='toBottom', parent=None, parentId=None,
            sibling=None, siblingId=None):
        '''
        Define the positional properties for a Row or RowWrapper.

        Verifies that the specified properties are a valid combination.

        If the Rows are to be children of a parent Row, then the position is
        relative to the parent Row:
          * position == self.Top     ->  relative to the first child
          * position == self.Bottom  ->  relative to the last child

        The parent or sibling Rows are mutually exclusive and can be specified
        either by passing a Row object or the ID of the desired parent or
        sibling Row.

        If the specified position properties are not valid, an error message
        is logged and SmartsheetClientError is raised.

        @param position Position of the Row 'toTop' or 'toBottom' (default).
        @param parentId The ID of a parent Row.
        @param siblingId The ID of a sibling Row.
        @returns True if the combination is valid.
        @raises SmartsheetClientError
        '''
        self.position = None
        self.parentId = None
        self.siblingId = None

        if position not in (self.Top, self.Bottom, None):
            err = ("position, if specified,  must be '%s' or '%s' got %r" %
                    (self.Top, self.Bottom, position))
            sheet.logger.error(err)
            raise SmartsheetClientError(err)

        if (parent and parentId is not None) and parent.id != parentId:
            err = ("%s.__init__() Specified parent Row: %r did not match "
                    "specified parentId: %r" % (parent, parentId))
            sheet.logger.error(err)
            raise SmartsheetClientError(err)

        if (sibling and siblingId is not None) and sibling.id != siblingId:
            err = ("Specified sibling Row: %r did not match specified "
                    "siblingId: %r" % (sibling, siblingId))
            sheet.logger.error(err)
            raise SmartsheetClientError(err)

        if parent:
            self.parentId = parent.id
        else:
            self.parentId = parentId

        if sibling:
            self.siblingId = sibling.id
        else:
            self.siblingId = siblingId

        if self.parentId is not None and self.siblingId is not None:
            err = "parentId and siblingId are mutually exclusive"
            sheet.logger.error(err)
            raise SmartsheetClientError(err)

        if self.siblingId is not None:
            if position is not None:
                err = "siblingId and position are mutually exclusive"
                sheet.logger.error(err)
                raise SmartsheetClientError(err)

        if self.parentId is not None:
            if position not in (None, self.Bottom):
                err = ("parentId specified, position must be %s or None." %
                        self.Bottom)
                sheet.logger.error(err)
                raise SmartsheetClientError(err)

        if position is None:
            if self.siblingId is None and self.parentId is None:
                self.position = self.Default_Position
        else:
            self.position = position

    def flatten(self):
        '''
        Return a the position information as a dict for sending to the server.

        @return Position information flattened to a dict.
        '''
        acc = {}
        if self.position == self.Top:
            acc[self.Top] = True
        elif self.position == self.Bottom:
            acc[self.Bottom] = True
        if self.parentId is not None:
            acc[self.Parent] = self.parentId
        if self.siblingId is not None:
            acc[self.Sibling] = self.siblingId
        return acc

    def __str__(self):
        return ('<RowPositionProperties %r  parent: %r  sibling: %r>' %
                (self.position, self.parentId or '', self.siblingId or ''))


class RowWrapper(object):
    '''
    Specifies the expansion state and/or position of one or more Rows.
    The Rows are contiguous.

    A RowWrapper can also be a source for generating new Rows -- all the
    Rows generated by a RowWrapper use the same cached CollumnInfo data.
    Using the RowWrapper as the generator for new Rows instead of the Sheet
    eliminates the risk of of surprise when the Columns in the Sheet change
    between creating Rows.

    The RowWrapper will honor the Sheet's cache setting when getting the
    "current" ColumnsInfo data.
    '''

    def __init__(self, sheet, positionProperties, expanded=True, rows=None):
        '''
        Make a RowWrapper suitable for adding one or more Rows to the Sheet.

        The Rows will all be added at the same hierarchical level at the
        position specified in positionProperties.

        @param sheet The sheet this RowWrapper is for.
        @param positionProperties The RowPositionProperties for these Rows.
        @param expanded Whether or not the Rows should be expanded.
        @param rows A list of Rows these position+expansion applies to.
        '''
        self.sheet = sheet
        self.positionProperties = positionProperties
        self.expanded = None
        self.rows = []
        if rows:
            self.rows.extend(rows)
        self._columns_info = self.sheet.getColumnsInfo()
        self._discarded = False

    def makeRow(self, *values_list, **values_dict):
        '''
        Make a Row in this RowWrapper -- with optional initial Cell values.
        Call with either a list of values (as positional parameters or single
        list of values), or a dict of values (as keyword parameters or a
        single dict of values), or neither, but not both.

        @param values_list A list of new Cell values
        @param values_dict A dict of new {(column.title|column.index): value}
        '''

        self.errorIfDiscarded()
        if values_list and values_dict:
            err = ("%s.makeRow() can only have list or dict/key-word values, "
                    "not both" % self)
            self.sheet.logger.error(err)
            raise SmartsheetClientError(err)
        if values_list:
            if len(values_list) == 1 and isMapping(values_list[0]):
                return self.makeRowFromDict(values_list[0])
            return self.makeRowFromList(*values_list)
        elif values_dict:
            return self.makeRowFromDict(**values_dict)
        else:
            return self.makeEmptyRow()

    def makeEmptyRow(self):
        '''
        Make an empty Row object that is suitable for use with this RowWrapper.
        '''
        self.errorIfDiscarded()
        row = Row(self.sheet, self._columns_info)
        return row

    def makeRowFromList(self, *values):
        '''
        Make a partially filled Row from a list of values.
        If values is a one-element list containing a list, the contained list
        is expanded and used as the list of values.

        If values is a generator, it is assumed to produce a list of items
        when passed to list as:  list(values).

        To insert an empty value in a Cell, use None in that position.

        The values are assumed to be in Column.index order.
        NOTE:  this might not be 0 - max Column index
        If the RowWrapper's ColumnsInfo contains only a subset of the Columns
        of the Sheet, then any Cells created will correspond to the indexes
        of those Columns.  In most cases that will be 0 - max Column index,
        but not always.
        The Column indexes used for the assignment are those from the
        RowWrapper's ColumnsInfo.

        @param values A list of values, or a 1-element list containing a list.
        @return A newly created Row in this RowWrapper (but not yet saved).
        '''
        self.errorIfDiscarded()
        if len(values) == 1:
            if isList(values[0]):
                # If the origignal call was with a really deeply nested list,
                # we will blow the call stack. :(
                return self.makeRowFromList(*values[0])
            if isGenerator(values[0]):
                return self.makeRowFromList(*list(values[0]))
            if not isScalar(values[0]):
                err = ("%s.makeRowFromList() can't understand: %r" %
                        (self, values))
                self.sheet.logger.error(err)
                raise SmartsheetClientError(err)

        columns = self._columns_info.columns
        if len(values) > len(columns):
            err = ("%s.makeRowFromList() len(values): %d > len(columns): %d" %
                    (self, len(values), len(columns)))
            self.sheet.logger.error(err)
            raise SmartsheetClientError(err)

        row = self.makeRow()
        for column, value in zip (columns, values):
            row[column.index] = value
        return row

    def makeRowFromDict(self, *values_list,  **values):
        '''
        Make a partially filled Row from a dict of values.
        The dict of values can be given as a dict argument or as name=value
        arguments.
        The keys can be either Column titles or Column indexes.
        If the keys are indexes or Column titles that are not valid Python
        argument names, the name=value approach won't work.
        Multiple dict arguments can be supplied, the Row created will contain
        the values from each -- with later dicts overriding earlier ones.

        @param values_list a list containing dicts (typically just one).
        @param values the values for the Row, as key-value pairs.
        @return A newly created Row in this RowWrapper (but not yet saved).
        @raises IndexError if the titles or index are not valid.
        '''
        self.errorIfDiscarded()
        row = self.makeRow()
        kv_pairs = []
        for item in values_list:
            for key, value in item.items():
                kv_pairs.append((key, value))

        for key, value in values.items():
            kv_pairs.append((key, value))

        for key, value in kv_pairs:
            if isInteger(key):
                index = int(key)
                # Verify that the index is valid.
                self._columns_info.getColumnByIndex(index)
            else:
                index = self._columns_info.getColumnByTitle(key).index
            row[index] = value
        return row

    def addRow(self, row):
        '''
        Add a Row to this RowWrapper.
        '''
        self.errorIfDiscarded()
        self.rows.append(row)
        return self

    def flattenForInsert(self, strict=None):
        '''
        Flatten the RowWrapper for inserting Rows.
        When inserting Rows, the 'expanded' parameter is not permitted.

        This method can only be used when inserting Rows into a Sheet.

        If a Row in the RowWrapper, or any Cell on a Row are discarded,
        then this will fail and raise OperationOnDiscardedObject.

        @param strict True to request strict Cell-data validation by the server.
        @returns dict suitable for sending to the server.
        @raises OperationOnDiscardedObject If a Row or Cell is discarded.
        '''
        self.errorIfDiscarded()
        acc = self.positionProperties.flatten()
        acc['rows'] = []
        for row in self.rows:
            acc['rows'].append(row.flattenForInsert(strict=strict))
        return acc

    def discard(self):
        '''
        Mark each of the Rows as discarded.
        This is called after the RowWrapper has been used and the Rows are
        now incorporated into the Sheet.
        '''
        for row in self.rows:
            row.discard()
        self._discarded = True

    def errorIfDiscarded(self):
        if self._discarded:
            raise OperationOnDiscardedObject("RowWrapper was discarded.")

    def __str__(self):
        self.errorIfDiscarded()
        return ("<RowWrapper position: %s rows=%r>" %
                (self.positionProperties, self.rows))


    def __repr__(self):
        self.errorIfDiscarded()
        return str(self)

class Row(AttachPoint, ContainedThing, object):
    '''
    A Row from a sheet.

    Rows are inserted to a Sheet by Sheet.addRow() or Sheet.addRows().
    Once a Row is part of a Sheet, it can be updated (on the server) by
    calling its .save() method.
    '''
    # Smartsheet is quite Row-centric.  As a result, the Row class is big
    # and busy.

    # Saving changes to new Rows and existing Rows is handled differently.
    # New Rows are sent to the server using a RowWrapper that indicates
    # where the Row (or Rows as a contiguous group) should be placed relative
    # to an existing Row or the top or bottom of the Sheet.
    # In addition, not all Cell values can be assigned to a new Row.
    #
    # Existing Rows are updated without the use of a RowWrapper.  They are
    # updated one at a time, and we only need to specify location/position
    # information for them if the Row is being moved.

    # Whenever a Row is saved to the server, it invalidates all other local
    # Rows.  This is because formulas can result in changes to the other
    # Rows that we can't predict.
    # TODO:  Keep track of how the Row or Sheet was fetched.
    # In order to do equivalent refresh of the Row or Sheet, we need to know
    # what includes it was fetched with.

    # Eventually, it would be nice to be able to tell the server which
    # version we are at and have it send us just the changes between our
    # version and the current version.

    field_names = '''id sheetId rowNumber parentRowNumber cells
                    discussions attachments columns expanded createdAt
                    modifiedAt accessLevel version format filteredOut'''.split()

    def __init__(self, sheet, columns_info=None):
        '''
        Create a new Row object.

        A newly created Row is empty.
        Cells can be added to it prior to saving it, but other objects that
        are "hung off" the Row (such as discussions and attachments) must be
        added after the Row has been saved to the Sheet.
        Cells with linkInFromCell can't be saved to a new Row either.
        '''
        AttachPoint.__init__(self, sheet)
        ContainedThing.__init__(self)
        self._id = -1           # Invalid ID
        self.sheet = sheet
        self.parent = sheet
        self._columns_info = columns_info
        self._rowNumber = -1    # Invalid row number
        self._parentRowNumber = 0   # Initially, no parent Row.
        self._cells = []
        self._discussions = []
        # self._attachments = []
        self._expanded = True
        self._createdAt = None
        self._modifiedAt = None
        self._accessLevel = None
        self._version = None
        self._format = ''
        self._filters = None
        self._filteredOut = None
        self._dirty = True      # Rows created this way need to be saved.
        self._discarded = False
        self._new_position = None
        self._new_expanded = None       # TODO: Implement use of this.
        # Track whether or not this is a new Row.   Some Cell attributes
        # can only be set when the Row already exists, not when it is first
        # being saved.  We could probably use self.id == -1 too.
        self._isNew = True

    @classmethod
    def newFromAPI(cls, fields, sheet, columns_info=None):
        row = Row(sheet)
        row.fields = fields
        row.sheet = sheet
        row.parent = sheet      # The Row belongs to the Sheet.
        row._dirty = False      # Rows from the server don't start dirty.
        row._isNew = False      # Rows from the server are not new.
        row._columns_info = columns_info

        row.sheet.logger.debug("Row.newFromAPI(# %d)", fields['rowNumber'])
        row._id = fields['id']
        row._rowNumber = fields['rowNumber']
        row._parentRowNumber = fields.get('parentRowNumber', 0)
        row._cells = [Cell.newFromAPI(c, row) for c in fields.get('cells', [])]
        row.sort_cells_by_column_index()

        # TODO:  Use the Columns that come with the Row (if any do).
        # When a Row is fetched directly, the caller can choose to get
        # the Columns with the Row.  This data is more current (theoretically)

        # When a Sheet is fetched or a Row is fetched directly, the caller
        # can have the server include the Discussions along with the Row.
        row._discussions = [
                Discussion.newFromAPI(d, sheet) for d in
                    fields.get('discussions', [])
        ]

        # When a Sheet is fetched or a Row is fetched directly, the caller
        # can have the server include the Attachments along with the Row.
        # row._attachments = [
        #         Attachment.newFromAPI(a, sheet) for a in
        #             fields.get('attachments', [])
        #         ]
        row._populate_attachments(fields.get('attachments', []))

        # Set the attributes that can't be set in __init__().
        maybeAssignFromDict(fields, row, 'expanded')
        maybeAssignFromDict(fields, row, 'version')
        maybeAssignFromDict(fields, row, 'format')
        maybeAssignFromDict(fields, row, 'createdAt')
        maybeAssignFromDict(fields, row, 'modifiedAt')
        maybeAssignFromDict(fields, row, 'accessLevel')
        maybeAssignFromDict(fields, row, 'filteredOut')

        return row

    @property
    def id(self):
        self.errorIfDiscarded()
        return self._id

    @property
    def sheetId(self):
        self.errorIfDiscarded()
        return self.sheet.id

    @property
    def rowNumber(self):
        self.errorIfDiscarded()
        return self._rowNumber

    @property
    def parentRowNumber(self):
        self.errorIfDiscarded()
        return self._parentRowNumber

    @property
    def cells(self):
        # TODO:  Consider making cells a dict, but it would return a list here.
        self.errorIfDiscarded()
        return self._cells

    @property
    def discussions(self):
        self.errorIfDiscarded()
        return self._discussions

    # @property
    # def attachments(self):
    #     self.errorIfDiscarded()
    #     return self._attachments

    @property
    def columns(self):
        self.errorIfDiscarded()
        if self._columns_info:
            return self._columns_info.columns
        return self.sheet.columns

    @property
    def maxColumnIndex(self):
        self.errorIfDiscarded()
        if self._columns_info:
            return self._columns_info.maxIndex
        return self.sheet.getColumnsInfo().maxIndex

    def getColumnById(self, column_id):
        '''Return the Column that has the specified ID.'''
        self.errorIfDiscarded()
        if self._columns_info:
            return self._columns_info.getColumnById(column_id)
        return self.sheet.getColumnById(column_id)

    def getColumnByIndex(self, idx):
        '''Return the Column that has the specified index.'''
        self.errorIfDiscarded()
        if self._columns_info:
            return self._columns_info.getColumnByIndex(idx)
        return self.sheet.getColumnByIndex(idx)

    @property
    def expanded(self):
        self.errorIfDiscarded()
        return self._expanded

    @expanded.setter
    def expanded(self, value):
        self.errorIfDiscarded()
        self._new_expanded = value

    @property
    def createdAt(self):
        self.errorIfDiscarded()
        return self._createdAt

    @property
    def modifiedAt(self):
        self.errorIfDiscarded()
        return self._modifiedAt

    @property
    def accessLevel(self):
        self.errorIfDiscarded()
        return self._accessLevel

    @property
    def version(self):
        self.errorIfDiscarded()
        return self._version

    @property
    def format(self):
        self.errorIfDiscarded()
        return self._format

    @property
    def filteredOut(self):
        self.errorIfDiscarded()
        return self._filteredOut

    @property
    def isNew(self):
        self.errorIfDiscarded()
        return self._isNew

    def delete(self):
        '''
        Delete this Row.
        This method executes immediately against the API server (like all
        actions that affect the structure of a Sheet).
        On the server, this deletes all of the Row's children (Cells,
        Attachments, Discussions), and locally these objects are all discarded.
        This operation also clears the Sheet's Row cache.
        Any operations on this Row after deletion will fail.
        '''
        self.errorIfDiscarded()
        sheet = self.sheet.deleteRow(self)
        self.discard()
        return sheet

    def discard(self):
        '''
        Mark the Row and its contained objects as discarded.
        Operations on a discarded item will raise OperationOnDiscardedObject.
        '''
        # We can't access these collections via their properties, because to
        # to so would not be safe if this Row was already discarded.
        for att in self.attachments:
            att.discard()
        for disc in self._discussions:
            disc.discard()
        for cell in self._cells:
            cell.discard()
        self._discarded = True

    def getAttachmentByFileName(self, file_name):
        '''
        Return the named Attachment object, or None if not found.
        '''
        self.errorIfDiscarded()
        for a in self.attachments:
            if a.name == file_name:
                return a
        return None

    def getCellByIndex(self, idx):
        '''
        Get the Cell at the specified index on this Row.
        Columns indexes start at 0.
        If the index is valid but there is no Cell there on this Row,
        an empty Cell is returned.
        Negative indexes return the Cells from the right:
          idx == -1  ->  The last Cell (from the right) of the Row
          idx == -2  ->  The second last Cell (from the right) of the Row
        Raises IndexError if the index is invalid.
        '''
        self.errorIfDiscarded()
        if isinstance(idx, slice):
            err = "Slices of Cell indexes are not supported."
            self.logger.error(err)
            raise NotImplementedError(err)
        try:
            column = self.getColumnByIndex(idx)
        except IndexError:
            if idx > self.maxColumnIndex + 1:
                self.logger.error("%s.getCellByIndex(%r) index is invalid.",
                        self, idx)
            raise
        except Exception as e:
            err = "%s.getCellByIndex(%r) failed: %s" % (self, idx, str(e))
            self.logger.exception(err)
            raise SmartsheetClientError(err)

        try:
            return self.getCellByColumnId(column.id)
        except KeyError:
            err = ("%s.getCellByIndexFailed(%s) %s => unknown Column ID %r" %
                    (self, str(idx), str(idx), column.id))
            self.logger.error(err)
            raise IndexError

    def getCellByColumnId(self, column_id):
        '''
        Get the Cell on this Row at the specified Column ID.
        Returns the Cell at the Column ID, or an empty Cell.
        Raises UnknownColumnId if column_id is unknown.

        @param column_id The ID of the Column
        @param use_cache True to use the Columns cache; False to refetch it
        @return The Cell on the Row at the specified Column
        @raises UnknownColumnId if the specified column_id is unknown
        '''
        self.errorIfDiscarded()
        # TODO:  Consider making self.cells a dict, instead of a list.
        # NOTE:  When we return an empty Cell, that Cell is not added to the
        # set of Cells on the Row until a value is assigned to it.
        for c in self.cells:
            if c.columnId == column_id:
                return c
        column = self.getColumnById(column_id)
        return Cell.makeEmptyCell(self, column)

    def replaceCell(self, original_cell, new_cell):
        '''
        Replace original_cell from this Row with new_cell.
        This updates the local Row, and ensures that the value of new_cell
        will be be sent to the server the next time the Row is saved.
        '''
        self.errorIfDiscarded()
        # * Lots of error checking before anything else:
        #   * Cells are on the right Row
        #   * Cells have matching Columns
        #   * Cells are on a Column that exists
        if self.id != original_cell.rowId:
            err ("%s.replaceCell() original_cell on wrong Row:  %r" %
                    (self, original_cell))
            self.logger.error(err)
            raise SheetIntegrityError(err)

        if self.id != new_cell.rowId:
            err ("%s.replaceCell() new_cell on wrong Row:  %r" %
                    (self, new_cell))
            self.logger.error(err)
            raise SheetIntegrityError(err)

        if original_cell.columnId != new_cell.columnId:
            err ("s.replaceCell() Cells not on same Column: original_cell: "
                    "%r  new_cell: %r" % (self, original_cell, new_cell))
            self.logger.error(err)
            raise SheetIntegrityError(err)

        try:
            col = self.getColumnById(new_cell.columnId)
        except Exception as e:
            err = ("%s.replaceCell() new_cell's columnId: %r not valid: %s" %
                    (self, new_cell.columnId, str(e)))
            self.logger.error(err)
            raise SheetIntegrityError(err)

        for idx, cell in enumerate(self.cells):
            if cell.columnId == new_cell.columnId:
                self.cells[idx] = new_cell
                self.markDirty()
                # We don't need to sort the Cells when just replacing a Cell.
                return
        # There wasn't a match in the current Cells, add the new one.
        # This is odd (unless original_cell was empty).
        if original_cell.type != CellTypes.EmptyCell:
            self.logger.warn("%s.replaceCell() expected to find a matching "
                    "Cell and didn't; appending it to the list of Cells for "
                    "the Row.  %r", self, new_cell)
        self.insertCell(new_cell)
        return self

    def insertCell(self, cell):
        '''
        Insert a Cell into the list of Cells for this Row.

        Preserve the sort-order of the Cells list.

        @param cell The Cell to insert
        @return The Row instance.
        '''
        self.errorIfDiscarded()
        self._cells.append(cell)
        self.markDirty()
        self.sort_cells_by_column_index()
        return self

    def sort_cells_by_column_index(self):
        '''
        Sort the Cells, in place, by the index of the Columns they are in.
        '''

        col_id_order = dict([(column_id, order_pos) for order_pos, column_id in
                enumerate([col.id for col in self.columns])])
        self._cells.sort(key=lambda c: col_id_order[c.columnId])

    def save(self, cell=None, strict=None, client=None):
        '''
        Save this Row to the server.

        If a Cell is specified, then only that Cell is sent to the server,
        and any other changes to Cells on the Row are discarded (with a
        warning written to the log).

        This method should not be used to add new Rows to the Sheet.  To
        add a new Row to the Sheet, use Sheet.addRow() or Sheet.addRows()
        with a RowWrapper.  At present, this will call Sheet.addRow() for
        you, but only after complaining in the logs.

        Any changes (new Cells, format, position, or expansion) on the Row
        are saved to the API server.

        Once saved, this Row is discarded and replaced by the Row constructed
        from the data returned by the server.  The caller should not hold a
        reference to the original Row past calling `save()`.

        @param cell The specific Cell to save (ignoring any others).
        @param strict True to request strict Cell-data validation by the server.
        @param client The optional Client to use (instead the Sheet's).
        @return The Sheet this Row is on.
        '''
        self.errorIfDiscarded()
        # What if other Rows have changed as well?
        # Should we discard them?  What if the user made a bunch of changes
        # to the Sheet and then is saving at the Sheet level (which will call
        # save on each of the Rows that is dirty)?
        # How should Row move be handled?
        # Should Row move be a separate operation that saves automatically?

        # When saving a single Cell on the Row, keep a copy of the other
        # cells so we can discard them later.
        all_cells = []
        if cell is not None:
            all_cells = list(self.cells)
            self._cells = cell if isList(cell) else [cell]

        sheet = self.sheet

        if self.isNew:
            self.logger.warning("Row.save() should not be used for saving "
                    "brand new Rows.  Use Sheet.addRow() or Sheet.addRows() "
                    "instead, they support Row position control.  %r", self)
            sheet = self.sheet.addRow(self)
        else:
            sheet = self.saveUpdate(client=client, strict=strict)

        # Discard the Row and any Cells on it.
        # This shouldn't be necessary, addRow() and saveUpdate() should both
        # call Sheet.clearRowCache(), which should discard all of the Rows on
        # the Sheet.
        self.discard()
        for cell in all_cells:
            cell.discard()
        return sheet

    def saveUpdate(self, client=None, strict=None):
        '''
        Update this Row on the server.

        Any change Cells, position or expansion of the Row will be saved
        to the server.

        @param strict True to request strict Cell-data validation by the server.
        @param client The optional Client to use (instead the Sheet's).
        '''
        self.errorIfDiscarded()
        # How does the caller specify a position change?
        # Will that be by virtue of calling Row.move() or Row.setPosition()
        # or some similar call?
        path = '/sheet/%s/row/%s' % (str(self.sheet.id), str(self.id))
        name = "%s.saveUpdate()" % self
        client = client or self.client
        sheet = self.sheet

        acc = { 'cells': [cell.flatten(strict=strict) for cell in
            self.cells if cell.type != CellTypes.EmptyCell] }
        if self._new_position is not None:
            acc.update(self._new_position.flatten())
        if self._new_expanded is not None:
            acc['expanded'] = self._new_expanded

        body = self.client.PUT(path, extra_headers=self.client.json_headers,
                body=json.dumps(acc))

        # FIXME:  Sheet.clearRowCache vs. saving multiple Rows to the Sheet.
        # We have to clear the Row cache since we can't predict what the
        # updated Row may have changed (due to formulas) or what other
        # changes may have occured to the Sheet (since it doesn't send us
        # deltas).
        self.sheet.clearRowCache()
        # Body should be the fields of the Row object that we just changed.
        # But, it won't contain any of the attachment, discussions, or
        # Column information for the Row. :(
        # Which leaves us with the question of:  What should we do now?
        # The default position would be to simply refetch the whole Sheet
        # with the same parameters used when it was fetched initially.
        # But, if the Sheet was fetched with just a subset of Rows or
        # Columns, then we should probably refetch just that subset.
        # We should also keep track of the subset used in the last refetch of
        # the Sheet -- we need to update this from Sheet.addRows().
        return sheet

    def flattenForInsert(self, strict=None):
        '''
        Flatten this Row's data so it can be inserted (as opposed to saved).
        '''
        self.errorIfDiscarded()
        acc = {'cells': []}
        # FIXME:  Should we really iterate over .cells?
        for cell in self.cells:
            if cell.type != CellTypes.EmptyCell:
                acc['cells'].append(cell.flattenForInsert(strict=strict))
        return acc

    def __getitem__(self, idx):
        '''
        Enable indexing a Row object to fetch the cell in the indicated column.
        This allows a Row to be used like a Python list.
        Column indexes start at 0; negative indexes work as normal for Python.
        Returns the value of the Cell at the specified column
        '''
        self.errorIfDiscarded()
        return self.getCellByIndex(idx).value

    def __setitem__(self, idx, value):
        '''
        Enable indexing a Row object to set the value in the indicated column.
        This allows a Row to be used like a Python list.
        Column indexes start at 0; negative indexes work as normal for Python.
        @param idx The Column-index of the Cell to assign to.
        @param value The value to assign to the Cell.
        @return the value assigned to the Cell.
        '''
        self.errorIfDiscarded()
        cell = self.getCellByIndex(idx)
        cell.assign(value)
        self.markDirty()
        return value

    def __len__(self):
        '''
        Calling len(a_row) will return the # of columns.
        '''
        self.errorIfDiscarded()
        return len(self.columns)

    def errorIfDiscarded(self):
        if self._discarded:
            raise OperationOnDiscardedObject("Row was discarded")

    def __str__(self):
        self.errorIfDiscarded()
        return '<Row id:%r rowNumber:%r>' % (self.id, self.rowNumber)

    def __repr__(self):
        self.errorIfDiscarded()
        return str(self)

    def _get_create_attachment_path(self):
        self.errorIfDiscarded()
        sheet_id = self.sheet._id
        row_id = self._id
        path = 'sheet/{0}/row/{1}/attachments'.format(sheet_id, row_id)
        return path

    def _get_refresh_attachment_path(self):
        return self._get_create_attachment_path()
