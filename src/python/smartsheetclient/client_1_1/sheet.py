'''
Library for working with Smartsheet's version 1.1 API.

This is HORRIBLY incomplete at the moment.

Author:  Scott Wimer <scott.wimer@smartsheet.com>
'''

import json
import copy
import operator
import datetime
import sys
import collections

from .smartsheet_exceptions import OperationOnDiscardedObject
from .base import maybeAssignFromDict, TopLevelThing
from .column import Column
from .row import (Row, RowWrapper, RowPositionProperties)
from .attachment import Attachment, AttachPoint
from .discussion import Discussion


class Sheet(AttachPoint, TopLevelThing, object):
    '''
    The Sheet, it may or may not be fully populated.
    When a Sheet is first fetched, the Rows in it are not fully populated.
    Getting fully populated rows takes either adding Rows or filling it
    with data from the API server.
    '''

    class ColumnsInfo(object):
        '''
        The information about the Columns of a Sheet at version of the Sheet.
        '''
        def __init__(self):
            self.version = None
            self._columns = None
            self.parent = None
            self._max_index = 0
            self.column_id_map = {}
            self.column_index_map = {}
            self.column_title_map = {}

        @classmethod
        def newFromDict(cls, sheet, fields):
            ci = Sheet.ColumnsInfo()
            ci.version = fields['version']
            ci.parent = sheet
            columns = [Column.newFromAPI(col_fields, sheet) for col_fields in
                    fields.get('columns', [])]
            for column in columns:
                ci.column_id_map[column.id] = column
                ci.column_index_map[column.index] = column
                ci.column_title_map[column.title] = column
                if column.index > ci._max_index:
                    ci._max_index = column.index
            return ci

        def initFully(self, version, parent, columns):
            '''
            Init from a list of Column objects.

            @version The version of the Sheet this ColumnsInfo is for.
            @param parent the Parent object, either a Sheet or Row object.
            @param columns A list of Column objects.
            @return The initialized ColumnsInfo object.
            '''
            self.version = version
            self.parent = parent
            self._column_id_map = {}
            self.column_index_map = {}
            self._max_index = 0
            for column in columns:
                self.column_id_map[column.id] = column
                self.column_index_map[column.index] = column
                self.column_title_map[column.title] = column
                if column.index > self._max_index:
                    self._max_index = column.index
            return self

        @property
        def columns(self):
            if self._columns is None:
                self._columns = sorted(list(self.column_id_map.values()),
                        key=operator.attrgetter('index'))
            return self._columns

        def getColumnById(self, column_id):
            return self.column_id_map[column_id]

        def getColumnByIndex(self, idx):
            '''
            Get the Column at the specified index
            Column indexes start at 0.
            This is distinct from Rows whose numbering starts at 1.
            Negative index values return the Columns from the right.
              idx == 0   ->  The primary Column
              idx == -1  ->  The last Column on the right
              idx == -2  ->  The second last Column on the right

            @param idx The index of the Column to get.
            @return The Column at the specified index.
            @raises IndexError if the specified index does not match a Column.
            '''
            if isinstance(idx, slice):
                err = "Slices of Column indexes are not supported."
                self.parent.logger.error(err)
                raise NotImplementedError(err)
            if idx < 0:
                return self.columns[idx]
            if idx in self.column_index_map:
                return self.column_index_map[idx]
            raise IndexError("%r invalid" % idx)

        def getColumnByTitle(self, title):
            '''
            Get the Column with the specified title.

            @param title The title of the Column to return.
            @return The Column with the specified title.
            @raises KeyError if the specified title is not valid.
            '''
            return self.column_title_map[title]


        @property
        def maxIndex(self):
            return self._max_index

        def copy(self):
            '''
            Return a copy of the ColumnsInfo instance.
            '''
            ci = self.__class__()
            ci.initFully(self.version, self.parent, self.columns)
            return ci

        def __str__(self):
            return '<ColumnInfo version:%r>' % self.version


    field_names = '''id name columns rows accessLevel discussions
                    attachments effectiveAttachmentOptions readOnly
                    createdAt modifiedAt permalink ganttEnabled
                    dependenciesEnabled favorite showParentRowsForFilters
                    version workspace totalRowCount'''.split()

    def __init__(self, sheetId, name, logger=None):
        AttachPoint.__init__(self, self)
        self._id = sheetId
        self._name = name
        self.fields = {}
        self.client = None
        self.request_parameters = {}
        self._use_cache = False
        self._discarded = False
        self.columnsInfo = None   # The most recently acquired ColumnsInfo.
        # Columns and Rows can be cached
        self._column_id_map = {}
        self._column_index_map = {}
        self._max_cached_index = -1
        self._row_id_map = {}
        self._row_number_map = {}
        self._discussions = []
        self._effectiveAttachmentOptions = []
        self._readOnly = False
        self._createdAt = datetime.datetime.utcnow().isoformat().split('.')[0]
        self._modifiedAt = self._createdAt
        self._permalink = None
        self._ganttEnabled = False
        self._dependenciesEnabled = False
        self._favorite = True
        self._showParentRowsForFilters = False
        self._version = 0
        self._workspace = None
        self._source = None
        self._totalRowCount = 0
        if logger is not None:
            self.logger = logger
        self.markClean()

    @classmethod
    def newFromAPI(cls, fields, client, request_parameters=None):
        sheet = Sheet(fields['id'], fields['name'])
        sheet.client = client
        sheet.request_parameters = request_parameters
        prior_cache_state = sheet.forceCache()
        sheet._initFromDict(fields)
        sheet.restoreCache(prior_cache_state)
        return sheet

    def _initFromDict(self, fields, isDirty=False):
        '''
        Initialize the Sheet from a dict of fields (such as is returned
        by the API).

        This can be used to "reset" a Sheet for the given dict of fields.
        If initializing from dict of fields not from the API, use isDirty
        to ensure the Sheet is marked as dirty.
        '''
        self.errorIfDiscarded()
        self.fields = fields
        maybeAssignFromDict(fields, self, 'id')
        maybeAssignFromDict(fields, self, 'name')
        maybeAssignFromDict(fields, self, 'version')
        self.columnsInfo = self.ColumnsInfo.newFromDict(self, fields)

        for row_fields in fields.get('rows', []):
            row = Row.newFromAPI(row_fields, self, self.columnsInfo)
            self._addRowToCache(row)

        self._set_attachments([Attachment.newFromAPI(a, self) for a in
                fields.get('attachments', [])])
        self._discussions = [Discussion.newFromAPI(d,self) for d in
                fields.get('discussions', [])]
        maybeAssignFromDict(fields, self, 'effectiveAttachmentOptions')
        maybeAssignFromDict(fields, self, 'readOnly')
        maybeAssignFromDict(fields, self, 'createdAt')
        maybeAssignFromDict(fields, self, 'modifiedAt')
        maybeAssignFromDict(fields, self, 'permalink')
        maybeAssignFromDict(fields, self, 'ganttEnabled')
        maybeAssignFromDict(fields, self, 'dependenciesEnabled')
        maybeAssignFromDict(fields, self, 'favorite')
        maybeAssignFromDict(fields, self, 'showParentRowsForFilters')
        maybeAssignFromDict(fields, self, 'workspace')
        maybeAssignFromDict(fields, self, 'source')
        maybeAssignFromDict(fields, self, 'totalRowCount')
        if isDirty:
            self.markDirty()
        return self

    def refresh(self, client=None, request_parameters=None):
        '''
        Refresh this Sheet.
        '''
        raise NotImplementedError

    @property
    def id(self):
        self.errorIfDiscarded()
        return self._id

    @property
    def name(self):
        self.errorIfDiscarded()
        return self._name

    @property
    def columns(self):
        self.errorIfDiscarded()
        return self.columnsInfo.columns

    @property
    def rows(self):
        self.errorIfDiscarded()
        return sorted(self._row_id_map.values(),
                key=operator.attrgetter('rowNumber'))

    @property
    def _rows(self):
        return sorted(self._row_id_map.values(),
                key=operator.attrgetter('rowNumber'))

    @property
    def accessLevel(self):
        self.errorIfDiscarded()
        return self._accessLevel

    @property
    def discussions(self):
        self.errorIfDiscarded()
        return self._discussions

    @property
    def effectiveAttachmentOptions(self):
        self.errorIfDiscarded()
        return self._effectiveAttachmentOptions

    @property
    def readOnly(self):
        self.errorIfDiscarded()
        return self._readOnly

    @property
    def createdAt(self):
        self.errorIfDiscarded()
        return self._createdAt

    @property
    def modifiedAt(self):
        self.errorIfDiscarded()
        return self._modifiedAt

    @property
    def permalink(self):
        self.errorIfDiscarded()
        return self._permalink

    @property
    def ganttEnabled(self):
        self.errorIfDiscarded()
        return self._ganttEnabled

    @property
    def dependenciesEnabled(self):
        self.errorIfDiscarded()
        return self._dependenciesEnabled

    @property
    def favorite(self):
        self.errorIfDiscarded()
        return self._favorite

    @property
    def showParentRowsForFilters(self):
        self.errorIfDiscarded()
        return self._showParentRowsForFilters

    @property
    def version(self):
        self.errorIfDiscarded()
        return self._version

    @property
    def workspace(self):
        self.errorIfDiscarded()
        # NOTE:  This doesn't seem to be a documented Sheet attribute.
        # TODO:  Determine whether or not the lack of docs is an error.
        return self._workspace

    @property
    def totalRowCount(self):
        self.errorIfDiscarded()
        if self._use_cache:
            return self._totalRowCount
        self._totalRowCount = self.fetchTotalRowCount()
        return self._totalRowCount

    def enableCache(self):
        '''
        Enable caching for read operations; data from server is always cached.

        This causes read operations (getting Rows, Columns, Attachments, etc.)
        to return cached values (if they are available).  If the requested
        value is not found in the cache, then the server will be consulted.

        The data returned from the server is always cached, this only effects
        whether or not it is used for read operations.
        @return The Sheet
        '''
        self.errorIfDiscarded()
        self._use_cache = True
        return self

    def disableCache(self):
        '''
        Disable caching for read operations; data from server is always cached.

        This causes read operations (geting Rows, Columns, Attachments, etc.)
        to ignore any corresponding cached values and directly query the
        server.

        The data returned from the server is always cached, disableCache()
        just prevents read operations from using the cached data.
        @return The Sheet
        '''
        self.errorIfDiscarded()
        self._use_cache = False
        return self

    def forceCache(self):
        '''
        Enable the cache and return the prior cache state.
        @return prior cache state, suitible for passing to restoreCache().
        '''
        self.errorIfDiscarded()
        prior_cache_state = self._use_cache
        self.enableCache()
        return prior_cache_state

    def forceNoCache(self):
        '''
        Disable the cache and return the prior cache state.
        @return prior cache state, suitable for passing to restoreCache().
        '''
        self.errorIfDiscarded()
        prior_cache_state = self._use_cache
        self.disableCache()
        return prior_cache_state

    def restoreCache(self, cache_state):
        '''
        Set the cache state to the passed in value (from forceCache())
        '''
        self.errorIfDiscarded()
        self._use_cache = cache_state
        return self

    def getColumnById(self, column_id):
        '''
        Return the Column that has the specified ID.

        @param column_id The ID of the Column to get
        @return The Column with the specified ID
        @raises UnknownColumnId If a matching Column is not found
        @raises SmartsheetClientError Communication error
        '''
        self.errorIfDiscarded()
        cache_miss = not self._use_cache    # Effectively a "forced" cache miss.
        if self._use_cache:
            try:
                return self.columnsInfo.getColumnById(column_id)
            except KeyError:
                cache_miss = True

        if cache_miss:
            self.logger.debug("%s.getColumnById() refreshing columnsInfo", self)
            self.refreshColumnsInfo()
        try:
            return self.columnsInfo.getColumnById(column_id)
        except KeyError:
            err = ("%s.getColumnById(%r): Column ID not found" %
                    (self, column_id))
            self.logger.error(err)
            raise UnknownColumnId(err)

    def getColumnByIndex(self, idx):
        '''
        Get the Column at the specified index
        Column indexes start at 0.
        This is distinct from Rows whose numbering starts at 1.
        Negative index values return the Columns from the right.
          idx == 0   ->  The first Column on the left (after built-in Columns)
          idx == -1  ->  The last Column on the right (of the fetched Columns)
          idx == -2  ->  The second last Column on the right

        @param idx The index of the Column to get.
        @return The Column at the specified index.
        @raises IndexError if the specified index does not match a Column.
        @raises SmartsheetClientError Communication error.
        '''
        self.errorIfDiscarded()
        cache_miss = not self._use_cache    # Effectively a "forced" cache miss.
        if self._use_cache:
            try:
                return self.columnsInfo.getColumnByIndex(idx)
            except IndexError:
                cache_miss = True

        if cache_miss:
            self.logger.debug("%s.getColumnByIndex() refreshing columnsInfo", self)
            self.refreshColumnsInfo()
        return self.columnsInfo.getColumnByIndex(idx)

    def getColumnsInfo(self):
        '''
        Get the current ColumnsInfo for the Sheet.

        Honor cache settings, but fetch them from the server if we don't have
        a cached copy.
        Note that this does not update the ColumnsInfo that the Sheet is using.
        '''
        self.errorIfDiscarded()
        cache_miss = not self._use_cache    # Effectively a "forced" cache miss.
        if self._use_cache:
            if self.columnsInfo:
                return self.columnsInfo
            else:
                cache_miss = True
        if cache_miss:
            return self.fetchColumnsInfo()

    def fetchColumnsInfo(self):
        '''
        Fetch the list of Columns' information for this Sheet.
        Raises SmartsheetClientError on error.

        @return A list of Column objects.
        @raises SmartsheetClientError
        '''
        self.errorIfDiscarded()
        path = '/sheet/%s?pageSize=1&page=1' % str(self.id)
        name = "%s.fetchColumnsInfo()" % str(self)
        body = self.client.GET(path, name=name)

        ci = self.ColumnsInfo.newFromDict(self, body)
        return ci

    def refreshColumnsInfo(self):
        '''
        Refresh the cached Columns information.
        '''
        self.errorIfDiscarded()
        self.logger.debug("%s.refreshColumnsInfo() calling fetchColumnsInfo()", self)
        self.columnsInfo = self.fetchColumnsInfo()
        return self

    def getRowByRowNumber(self, row_number):
        '''
        Get the Row with the specified Row number.
        The numbering of Rows starts at 1.
        This is distinct from Columns which have indexes that start at 0.
        Negative row_numbers fetch Rows from the bottom of the Sheet.
          row_number == 1   ->  The top Row of the Sheet
          row_number == -1  ->  The last Row of the Sheet
          row_number == -2  ->  The second last Row of the Sheet

        If the Row is fetched from the server, it is cached for later use.

        @param row_number The number of the Row to get.
        @return The Row at row_number.
        @raises IndexError If row_number is not found.
        @raises SmartsheetClientError Communication error.
        '''
        self.errorIfDiscarded()
        if row_number == 0:
            err = ("%s.getRowByRowNumber(%d) 0 is not a valid Row number" %
                    (self, 0))
            self.logger.error(err)
            raise IndexError(err)
        if isinstance(row_number, slice):
            err = "Slices are not supported for Row numbers."
            raise NotImplementedError(err)

        cache_miss = not self._use_cache    # Effectively a "forced" cache miss.
        if self._use_cache:
            if row_number < 0:
                try:
                    return self.rows[row_number]
                except IndexError:
                    # row_number not found in cache; fetch the current data.
                    cache_miss = True
            elif row_number > 0:
                if row_number in self._row_number_map:
                    return self._row_number_map[row_number]
                cache_miss = True

        if cache_miss:
            # TODO: Should we fetch more than just this current Row?
            # Can that be something that we can let the library user configure?
            # Some sort of fetch ratio?
            if row_number < 0:
                prior_cache_state = self.forceNoCache()
                self.restoreCache(prior_cache_state)
                row_number = self.totalRowCount + 1 + row_number
            row = self.fetchRowByNumber(row_number)
            self._addRowToCache(row)
            return row

    def getRowById(self, row_id):
        '''
        Get a Row by its Id.

        If the Row is fetched from the server, it is cached for later use.

        @param row_id The ID of the Row.
        @return The Row identified by row_id.
        @raises KeyError If a matching Row is not found.
        @raises SmartsheetClientError Communication error.
        '''
        self.errorIfDiscarded()
        cache_miss = not self._use_cache    # Effectively a "forced" cache miss.
        if self.use_cache:
            if row_id in self._row_id_map:
                return self._row_id_map[row_id]
            cache_miss = True

        if cache_miss:
            row = self.fetchRowById(row_id)
            self._addRowToCache(row)
            return row

    def fetchRowByNumber(self, row_number):
        '''
        Fetch the specified Row from the server.

        @param row_number The rowNumber of the Row to fetch.
        @return The Row at row_number.
        @raises NotImplementedError - if row_number is an index
        @raises IndexError if the row_number is not found on the Sheet
        @raises SmartsheetClientError Communication error
        @raises Other networking exceptions
        '''
        self.errorIfDiscarded()
        if isinstance(row_number, slice):
            err = "Slices of row numbers are not supported"
            self.logger.error(err)
            raise NotImplementedError(err)
        path = '/sheet/%s?rowNumbers=%s' % (str(self.id), str(row_number))
        name = "%s.fetchRowByNumber(%s)" % (str(self), str(row_number))
        body = self.client.GET(path, name=name)

        rows_fields = body.get('rows', [])
        if not rows_fields:
            err = ("%s does not have a Row number %s, totalRowCount: %d" %
                    (self, str(row_number), body.get['totalRowCount']))
            self.logger.warn(err)
            raise IndexError(err)
        ci = self.ColumnsInfo.newFromDict(self, body)
        row = Row.newFromAPI(rows_fields[0], self, ci)
        return row

    def fetchRowById(self, row_id):
        '''
        Fetch the Row with the specified ID from the server.

        @param row_id The ID of the Row to fetch from the server.
        @return The Row with the ID row_id.
        @raises SmartsheetClientError
        @raises KeyError The specified row_id is invalid.
        '''
        self.errorIfDiscarded()
        # To do this, we have to refetch the sheet, asking for only a specific
        # Row ID.
        # We don't cache off all of the information that we technically could
        # from what the server returns.  That's because I would rather not
        # have the fetch-layer writing directly to the caches.
        path = '/sheet/%s?rowIds=%s' % (str(self.id), str(row_id))
        name = "%s.fetchRowById(%s)" % (self, str(row_id))
        body = self.client.GET(path, name=name)

        rows_fields = body.get('rows', [])
        if not rows_fields:
            err = "%s does not have a Row with ID: %s" % (self, str(row_id))
            self.logger.error(err)
            raise KeyError(err)
        ci = self.ColumnsInfo.newFromDict(self, body)
        row = Row.newFromAPI(rows_fields[0], self, ci)
        return row

    def fetchTotalRowCount(self):
        '''
        Fetch the current total Row count.
        @return The current total Row count
        @raises SmartsheetClientError
        '''
        self.errorIfDiscarded()
        path = '/sheet/%s?pageSize=1&page=1' % str(self.id)
        name = "%s.fetchTotalRowCount()" % self
        body = self.client.GET(path, name=name)
        return body['totalRowCount']

    def _addRowToCache(self, row):
        '''
        Add this Row to the Row cache.
        '''
        self.errorIfDiscarded()
        self._row_number_map[row.rowNumber] = row
        self._row_id_map[row.id] = row
        return self

    def clearRowCache(self):
        '''
        Clear the Row cache.
        '''
        self.errorIfDiscarded()
        # FIXME:  This needs to discard all of the Rows.
        self._row_id_map = {}
        self._row_number_map = {}
        return self

    def __getitem__(self, row_number):
        '''
        Add a list-style interface to fetching a Row.
        The index is the row_number (1-based) and not a classic (0-based) index.
        This forces the use of caching.
        '''
        self.errorIfDiscarded()
        prior_cache = self.forceCache()
        row = self.getRowByRowNumber(row_number)
        self.restoreCache(prior_cache)
        return row

    def __iter__(self):
        # TODO:  Make sure this still works now that Rows are stored in a dict.
        self.errorIfDiscarded()
        return iter(self.rows)

    def __len__(self):
        return self.totalRowCount

    def allDiscussions(self, include_rows=True):
        '''
        Get a list of all the Discussions on the Sheet.
        NOTE: The Sheet must have been fetched with discussions.

        @param include_rows If True, get Sheet and Row-level Discussions
        @return A list of Discussion objects
        '''
        self.errorIfDiscarded()
        acc = []
        acc.extend(self.discussions)
        if include_rows:
            for r in self.rows:
                acc.extend(r.discussions)
        return acc

    def getAttachmentsByFileName(self, name, use_cache=True, client=None):
        '''
        Get the named Attachment objects to the Sheet.
        The returned Attachment objects may be attached to the Sheet, its
        Rows, or Discussions.

        If the information about Attachments if fetched from the API server,
        it is cached for later use.

        When a Sheet if first loaded, it can be fetched with information
        about the Attachments to the Sheet, Rows, and Discussions.
        Those constitute the initial cache of Attachments.

        @param name The name of the attachment
        @param use_cache True to use the cache; False to issue API query
        @param client The client to use instead of sheet.client if not use_cache
        @return A list of Attachment objects
        @raises SmartsheetClientError Communication error
        '''
        self.errorIfDiscarded()
        return [a for a in
                self.getAllAttachments(use_cache=use_cache, client=client)
                if a.name == name]

    def getAttachmentById(self, attachment_id, use_cache=True, client=None):
        '''
        Get the Attachment object with the specified ID.
        The returned Attachment object may be attached directly to the Sheet,
        or to a Row or Discussion.

        If the information about the Attachment is fetched from the API
        server, it is cached for later use.

        If the cache is not used, the info for *all* Attachments is fetched
        and cached for later use.

        @param attachment_id The ID of the attachment
        @param use_cache True to use the cache; False to issue API query
        @param client The client to use instead of sheet.client if not use_cache
        @return An Attachment object, or None
        @raises SmartsheetClientError Communication error
        '''
        self.errorIfDiscarded()
        if use_cache:
            acc = [a for a in self.attachments if a.id == attachment_id]
            if acc:
                return acc[0]
            return None
        else:
            # We could either fetch the info for just this Attachment, or
            # for all Attachments.  since we're caching the info, we'll get
            # the info for all of them.
            attachments = self.fetchAllAttachments(client=client)
            self._set_attachments(attachments)

    def getAllAttachments(self, use_cache=True, client=None):
        '''
        Get all of the Attachment object for this Sheet.

        If the information about Attachments if fetched from the API server,
        it will be cached.
        @param use_cache True to use the cache; False to issue API query
        @param client The client to use instead of sheet.client if not use_cache
        @return A list of Attachment objects
        @raises SmartsheetClientError Communication error
        '''
        self.errorIfDiscarded()
        if use_cache:
            return copy.copy(self.attachments)
        else:
            attachments = self.fetchAllAttachments(client=client)
            self._set_attachments(attachments)
            return self.getAllAttachments(use_cache=True)

    def fetchAllAttachments(self):
        '''
        Fetch the Attachment objects for each Attachment on this Sheet.

        This also fetches the Attachments that are on the Rows and Discussions
        of the Sheet.
        @param client The client to use instead of sheet.client if not use_cache
        @return List of Attachment objects
        @raises SmartsheetClientError
        '''
        self.errorIfDiscarded()
        path = '/sheet/%s/attachments' % str(self.id)
        name = "%s.fetchAllAttachments()" % str(self)
        body = self.client.GET(path, name=name)

        self.logger.debug("Sheet.fetchAllAttachments(%s) succeeded",
                str(self))
        return [Attachment.newFromAPI(a_fields, self) for a_fields in body]

    def makeRowWrapper(self, position=None, parentId=None, siblingId=None):
        '''
        Create a RowWrapper for this Sheet.
        '''
        self.errorIfDiscarded()
        rpprops = RowPositionProperties(self, position=position,
                parentId=parentId, siblingId=siblingId)
        return RowWrapper(self, rpprops)

    def makeRow(self, *values_list, **values_dict):
        '''
        Create a new Row for this Sheet -- with optional intitial Cell values.

        Call with either a list of values (as positional parameters or single
        list of values), or a dict of values (as keyword parameters or a
        single dict of values), or neither, but not both.

        The Row uses the current ColumnsInfo for the Sheet, but it is not
        "attached" to the Sheet (it isn't found in Sheet.rows).
        In order to attach the Row to the Sheet, it must be passed to
        sheet.addRow() or placed in a RowWrapper and passed to sheet.addRows().
        @returns The new Row
        '''
        self.errorIfDiscarded()
        # Enable caching so that the RowWrapper uses the ColumnProperties
        # of the Sheet, instead of fetching the current one from the server.
        cache_state = self.forceCache()
        rpprops = RowPositionProperties(self)
        rw = RowWrapper(self, rpprops)
        row = rw.makeRow(*values_list, **values_dict)
        rw.discard()
        self.restoreCache(cache_state)
        return row

    def addRow(self, row, position=None, parentId=None, siblingId=None,
            strict=True):
        '''
        Add a single Row to the Sheet.

        See the documentation for the RowWrapper class for details on the
        placement arguments: 'position', 'parentId', and 'siblingId'.

        @param row The Row to add - the Row may be empty.
        @param position Where to insert the Row ('toTop' or 'toBottom')
        @param parentId ID of the parent Row to insert `row` under.
        @param siblingID ID of the Row to insert `row` next to
        @param strict True for the API server to do strict Cell parsing.
        @return The Sheet.
        @raises SmartsheetClientError for Communications errors
        '''
        self.errorIfDiscarded()
        rpprops = RowPositionProperties(self, position=position,
                parentId=parentId, siblingId=siblingId)
        row_wrapper = RowWrapper(self, rpprops, rows=[row])
        return self.addRows(row_wrapper, strict=strict)

    def addRows(self, row_wrapper, strict=True):
        '''
        Add the Row(s) in the RowWrapper to the Sheet.
        The RowWrapper specifies *where* in the Sheet the Row(s) should be
        added.
        @param row_wrapper The Rows with their position information.
        @param strict True for the API server to do strict Cell parsing.
        @return The Sheet.
        '''
        # FIXME: Inserting Rows can cause Cell changes behind the scenes.
        # That's due, at a minimum, to Formula changes.
        # The only safe way to handle this is to refetch the Sheet after
        # adding Rows.  However, that might not work well if the Sheet was
        # fetched with only a subset of the Rows (via rowIds or rowNumbers).
        # I don't have a good solution to this problem today, I'm not sure
        # there is one short of essentially reimplementing the web client,
        # and while that is a "solution", it doesn't seem like a "good" one.
        #
        # If the Sheet was fetched with a subset of Rows, then we should add
        # these newly inserted Rows to that subset.  This way, when the Sheet
        # is refreshed, it will contain the Rows the caller just added to it.
        # That seems like if follows the principle of least astonishment.
        self.errorIfDiscarded()
        path = '/sheet/%s/rows' % str(self.id)
        name = "%s.addRows(%s,strict=%r)" % (self, str(row_wrapper), strict)

        body = self.client.POST(path, extra_headers=self.client.json_headers,
                body=json.dumps(row_wrapper.flattenForInsert()), name=name)
        self.clearRowCache()
        row_wrapper.discard()
        self.clearRowCache()
        return self

    def deleteRow(self, row):
        '''
        Delete the Row (and any of its children) from the Sheet.
        The "children" of the Row include any Rows for whom this Row
        is an ancestor, as well as any Attachments, Formats, and
        Dicussions attached to this Row.
        This method (like all structural change methods) results in an
        immediate update of the Sheet.
        Any unsaved changes to the Row (Cell values, format, etc.) are lost.

        @param row The Row to delete.
        @return The Sheet.
        @raises SmartsheetClientError
        '''
        self.errorIfDiscarded()
        return self.deleteRowById(row.id)

    def deleteRowById(self, row_id):
        '''
        Delete the Row (and any of its children) from the Sheet.
        The "children" of the Row include any Rows for whom this Row
        is an ancestor, as well as any Attachments, Formats, and
        Dicussions attached to this Row.
        This method (like all structural change methods) results in an
        immediate update of the Sheet.
        Any unsaved changes to the Row (Cell values, format, etc.) are lost.

        @param row_id The ID of the Row to delete.
        @return The Sheet.
        @raises SmartsheetClientError
        '''
        self.errorIfDiscarded()
        path = '/sheet/%s/row/%s' % (str(self.id), str(row_id))
        name = "%s.deleteRowById(%s)" % (self, str(row_id))
        body = self.client.DELETE(path, name=name)
        self.clearRowCache()
        # FIXME:  Deleting 1 Row results in no more cached Rows.
        # When caching is enabled, we might want to refetch the cached Rows.
        # We also need to be able to iterate over the Rows of a Sheet,
        # deleting them as we go, without having to constantly clear and
        # refetch the Row cache.
        return self

    def insertColumn(self, column, index=-1):
        '''
        Insert a Column to the Sheet at the specified index.
        Negative index values count "back" from the far-right Column.
        To append a Column to the far-right, use 'index=-1' (the default).
        If the index specified is outside of the Sheet's current indexes, it
        will still be used -- the API server may accept it.

        @param column The Column to insert
        @param index The index to inser column at (-1 means far-right)
        @return The Sheet
        '''
        self.errorIfDiscarded()
        path = '/sheet/%s/columns' % str(self.id)
        name = "%s.insertColumn(%s, %s)" % (self, column, str(index))
        col_fields = column.flattenForInsert()
        ins_index = index
        if index < 0:
            tmp_col = self.getColumnByIndex(index)
            ins_index = tmp_col.index + 1
        col_fields['index'] = ins_index

        body = self.client.POST(path, extra_headers=self.client.json_headers,
                body=json.dumps(col_fields))

        # Structure changed, update it.
        self.logger.debug("%s.insertColumn() refreshing columns_info", self)
        self.refreshColumnsInfo()
        return self

    def deleteColumn(self, column):
        '''
        Delete the specified Column from the Sheet.
        @param column The Column to delete.
        @returns The Sheet
        @raises SmartsheetClientError
        '''
        self.errorIfDiscarded()
        return self.deleteColumnById(column.id)

    def deleteColumnById(self, column_id):
        '''
        Delete the specified Column from the Sheet.
        @param column_id The ID of the Column to delete.
        @returns The Sheet
        @raises SmartsheetClientError
        '''
        self.errorIfDiscarded()
        path = '/sheet/%s/column/%s' % (str(self.id), str(column_id))
        name = "%s.deleteColumnById(%s)" % str(column_id)
        body = self.DELETE(path, name=name)
        self.logger.debug("%s.deleteColumnById() refreshing columns_info", self)
        self.refreshColumnsInfo()
        return self

    def updateColumn(self, column):
        '''
        Update the specified Column in the Sheet.
        @param column The Column to update.
        @return The Sheet.
        @raises SmartsheetClientError
        '''
        self.errorIfDiscarded()
        path = '/sheet/{sheetId}/column/{columnId}'.format(
                sheetId=self.id, columnId=column.id)
        name = '{sheet}.updateColumnn({columnId})'.format(
                sheet=self, columnId=column.id)
        body = self.client.PUT(path, name=name,
                extra_headers=self.client.json_headers,
                body=json.dumps(column.flattenForUpdate()))
        self.logger.debug('%s.updateColumn() refreshing columns_info', self)
        self.refreshColumnsInfo()

    def refetch(self):
        '''
        Refetch the Sheet - using the original fetch options.
        Returns a new instance of the Sheet.
        It unfortunately does not do an in-place refresh.
        NOTE: May only fetch a subset of the Sheet (depending on original fetch)
        '''
        raise NotImplementedError("Sheet.refetch() not implemented")
        # return self.client.fetchSheetById(self.id, **self.request_parameters)

    def discard(self):
        '''
        Mark this Sheet as discarded.
        Operations on it after this should fail.
        '''
        self._discarded = True
        self.client = None      # Not very nice, but it'll work for now.
        for row in self._rows:
            row.discard()
        self._force_discard_attachments()
        for discussion in self._discussions:
            discussion.discard()

    def delete(self):
        '''
        Delete the Sheet.
        Returns True on success, raise SmartsheetClientError otherwise.
        '''
        self.errorIfDiscarded()
        path = '/sheet/%s' % str(self.id)
        name = "%s.delete()" % self
        body = self.client.DELETE(path, name=name)
        self.discard()
        return True

    def errorIfDiscarded(self):
        if self._discarded:
            raise OperationOnDiscardedObject("Sheet was discarded.")

    def __str__(self):
        return '<Sheet id:%r, name:%r>' % (self.id, self.name)

    def __repr__(self):
        return str(self)

    def _get_create_attachment_path(self):
        self.errorIfDiscarded()
        sheet_id = self.id
        path = 'sheet/{0}/attachments'.format(sheet_id)
        return path

    def _get_refresh_attachment_path(self):
        return self._get_create_attachment_path()

    def addDiscussion(self, title, initial_comment, client=None):
        self.errorIfDiscarded()
        # this is woefully incomplete
        client = client or self.client
        body = {}
        body['title'] = title
        body['comment'] = {'text': initial_comment}
        path = 'sheet/{0}/discussions'.format(self.id)
        body = json.dumps(body)
        response = client.POST(path,
                extra_headers=None,
                body=body)
        tmp = Discussion.newFromAPI(response['result'], self)
        self.discussions.append(tmp)
        return tmp

    def removeDiscussion(self, obj, client=None):
        self.errorIfDiscarded()
        client = client or self.client
        if not isinstance(obj, Discussion):
            raise TypeError("The first argument of Sheet.removeDiscussion"
                    " must be a Discussion")
        self._discussions.remove(obj)
        path = 'sheet/{0}/discussion/{1}'.format(self.id, obj.id)
        self.client.DELETE(path)

    def fetchDiscussionById(self, discussion_id, client=None):
        self.errorIfDiscarded()
        client = client or self.client
        path = 'sheet/{0}/discussion/{1}'.format(self.id, discussion_id)
        response = client.GET(path)
        d = Discussion.newFromAPI(response, self)
        for i, j in enumerate(self.discussions):
            if j.id == d.id:
                self.discussions[i] == d
                break
        else:
            self.discussions.append(d)
        return d

    def fetchAllDiscussions(self, client=None):
        self.errorIfDiscarded()
        client = client or self.client
        path = 'sheet/{0}/discussions'.format(self.id)
        response = client.GET(path)
        self._discussions = [Discussion.newFromAPI(i, self) for i in response]
        return self.discussions


class SheetInfo(TopLevelThing, object):
    '''
    The most basic information about a sheet.
    '''
    field_names = 'id name accessLevel permalink'.split()
    def __init__(self, fields, client):
        self.fields = fields
        self.client = client
        self._dirty = False

    @property
    def id(self):
        return self.fields['id']

    @property
    def name(self):
        return self.fields['name']

    @property
    def accessLevel(self):
        return self.fields.get('accessLevel', '')

    @property
    def permalink(self):
        return self.fields.get('permalink', '')

    def loadSheet(self, discussions=False, attachments=False,
            format=False, filters=False, source=None, rowNumbers=None,
            rowIds=None, columnIds=None, pageSize=None, page=None):

        '''
        Load the Sheet this SheetInfo object is about.
        The optional parameters are the same as those for
        SmartsheetClient.fetchSheetById().
        Returns the corresponding Sheet.
        '''
        return self.client.fetchSheetById(self.id, discussions=discussions,
                attachments=attachments, format=format, filters=filters,
                source=source, rowNumbers=rowNumbers, rowIds=rowIds,
                columnIds=columnIds, pageSize=pageSize, page=page)

    def __str__(self):
        return '<SheetInfo id:%r, name: %r, accessLevel: %r, permalink:%r>' % (
                self.id, self.name, self.accessLevel, self.permalink)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        '''
        Enable == comparisons between SheetInfo objects.
        '''
        return (self.id == other.id and
                self.name == other.name and
                self.accessLevel == other.accessLevel and
                self.permalink == other.permalink)

    def __ne__(self, other):
        '''
        Enable != comparisons between SheetInfo objects.
        '''
        return (self.id != other.id or
                self.name != other.name or
                self.accessLevel != other.accessLevel or
                self.permalink != other.permalink)

