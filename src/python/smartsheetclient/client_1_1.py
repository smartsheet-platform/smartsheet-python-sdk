'''
Library for working with Smartsheet's version 1.1 API.

This is HORRIBLY incomplete at the moment.

Author:  Scott Wimer <scott.wimer@smartsheet.com>
'''

import httplib2
import json
import os
import copy
import time
import logging
import collections

# Things that I know need to be fixed.
# TODO:  Create exception classes and use them to pass errors to the caller.
# TODO:  Log when deprecated things (attributes and paths) are used.
# TODO:  Add OAuth support.

# All Exceptions raised by the client will inherit from this class.
class SmartsheetClientError(Exception): pass

class ReadOnlyClientError(SmartsheetClientError):
    '''
    An attempt was made to write using a client in read-only mode.
    '''
    pass

class APIRequestError(SmartsheetClientError):
    '''
    The Smartsheet API request failed for any reason other than rate limit.
    The exception object contains the error information set by the API server.
    '''
    def __init__(self, hdr):
        self.hdr = hdr

    def __str__(self):
        return '<APIRequestError status: %s  error_code: %r  message: %r>' % (
                self.hdr.status, self.hdr.error_code, self.hdr.error_message)

class SheetIntegrityError(SmartsheetClientError):
    '''
    A Sheet or something related to it had data in an inconsistent state.
    Any further processing would have undefined behavior and be unsafe.
    '''
    pass

class UnknownColumnId(SmartsheetClientError):
    '''
    The specified Column ID did not correspond to a columnId on the Sheet.
    This could occur for a valid Column ID if the Sheet was fetched with
    only a subset of the total Columns.  Generally though, if that happens,
    no Cell returned with the Sheet would be referring to the Column ID in
    the first place
    '''
    pass

class InvalidColumnIndex(SmartsheetClientError):
    '''
    The specified column index was not found in the Sheet.
    This could occur for a valid column index if the Sheet was fetched with
    only a subset of the total columns.
    '''
    pass

class InvalidRowNumber(SmartsheetClientError):
    '''
    The specified row number was not found in the Sheet.
    This could occur for a valid row number if the Sheet was fetched with
    only a subset of the total Rows.
    '''
    pass

class SheetHasNoRows(SmartsheetClientError):
    '''
    The Sheet has no Rows and a method that required rows was used.
    '''
    pass

class InvalidOperationOnUnattachedRow(SmartsheetClientError):
    '''
    An operation was attempted on a Row that was not "attached" to a Sheet.
    Rows can be fetched separately from their Sheet -- this is a problem for
    operations that require access to Sheet attributes (such as the list of
    columns).  Those operations will raise this exception.
    '''
    pass

class BadCellDataTypeError(SmartsheetClientError):
    '''
    An attempt was made to store invalid data to a cell.
    '''
    pass


class BadCellData(SmartsheetClientError):
    '''
    The data assigned to a Cell does not meet the default/strict format rules.
    '''
    pass

class DeprecatedAttribute(SmartsheetClientError):
    '''
    A deprecated attribute of the API was used.
    '''
    pass


class HttpRequestInfo(object):
    '''
    A log entry of information about an HTTP request.
    '''
    def __init__(self, method, url, headers, body=''):
        self.start_time = time.time()
        self.method = method
        self.url = url
        self.request_headers = headers
        self.request_body = body
        self.try_count = 0
        self.end_time = None

    def markRequestAttempt(self):
        self.try_count += 1
        return self

    def addResponse(self, hdr, body):
        self.response_header = hdr
        self.response_body = body
        return self

    def end(self):
        self.end_time = time.time()
        return self

    @property
    def duration(self):
        return self.end_time - self.start_time


def join_url_path(base_url, path):
    '''
    Join the base URL and path
    '''
    # if path.startswith('/'):
        # path = path[1:]

    if path:
        if base_url.endswith('/'):
            if path.startswith('/'):
                full_url = base_url + path[1:]
            else:
                full_url = base_url + path
        else:
            if path.startswith('/'):
                full_url = base_url + path
            else:
                full_url = base_url + '/' + path
    else:
        full_url = url
    return full_url



class SmartsheetClient(object):
    '''
    Simple client for interacting with Smartsheet sheets using the API v1.1.
    '''
    base_url = 'https://api.smartsheet.com/1.1/'
    version = '1.1'

    def __init__(self, token=None, rate_limit_sleep=10, logger=None,
            read_only=False, retry_limit=3, request_log_len=20):
        '''
        Create a new SmartsheetClient.

        @param token The API Access token.
        @param rate_limit_sleep Number of seconds to sleep when rate-limited.
        @param logger the logger to log to.
        @param read_only True to prevent any write/update/delete operations.
        @param retry_limit Number of times to retry queries.
        @param request_log_len Store the last N queries' HttpRequestInfo.
        '''
        self.token = token
        self.rate_limit_sleep = rate_limit_sleep
        self.logger = logger or logging.getLogger('SmartsheetClient')
        self.read_only = read_only
        self.retry_limit = retry_limit
        self._sheet_list_cache = []
        self.user = None
        self.handle = None
        self.request_count = 0
        self.request_error_count = 0
        self.json_headers = {'Content-Type': 'application-json'}
        self.request_log = collections.deque(maxlen=request_log_len)


    def connect(self):
        '''
        Connect to the Smartsheet API, verifying that the token works.
        This fetches the profile for the current user.
        '''
        self.handle = httplib2.Http()
        self.user = self.fetchUserProfile()
        return self


    def default_headers(self):
        return {'Authorization': 'Bearer %s' % self.token}


    def raw_request(self, url, path, method='GET', headers=None, body=None):
        '''
        Make a request with no API headers added.
        Returns the response header and body.
        '''
        req_headers = headers or {}
        req_url = join_url_path(url, path)

        if not self.handle:
            self.connect()
            # FIXME: There's a bit of conflation here.
            # raw_request is also used to talk to other servers, and connect()
            # contacts the API server.

        self.logger.debug('req_url: %r', req_url)
        if body:
            self.logger.debug('req_body: %r', body)
        resp, content = self.handle.request(req_url, method, body=body,
                headers=req_headers)
        self.logger.debug('resp: %r',  resp)
        self.logger.debug('content: %r', content)
        return (resp, content)


    def request(self, path, method='GET', extra_headers=None, body=None):
        '''
        Make an API request.
        Caller may specify a different method and additional headers to send.
        API requests that fail due to rate limiting will be retried after a
        brief sleep.
        Returns a SmartsheetAPIResponseHeader and a body (typically a dict).
        On failure raises the APIRequestError exception.
        '''
        headers = self.default_headers()
        if extra_headers:
            headers.update(extra_headers)
    
        req_info = HttpRequestInfo(method, join_url_path(self.base_url,path),
                headers, body)
        self.request_log.append(req_info)

        if self.read_only and (method != 'GET' or method != 'HEAD'):
            self.logger.error("Client is read only, request (%s %s %s) " +
                    "not permitted.", method, self.base_url, path)
            raise ReadOnlyClientError(("Client is read only, request " +
                    "(%s %s %s) not permitted.") %(method, self.base_url, path))

        while True:
            req_info.markRequestAttempt()
            (resp, content) = self.raw_request(self.base_url, path, method,
                    headers=headers, body=body)
            req_info.addResponse(resp, content)
            hdr = SmartsheetAPIResponseHeader(resp, content, self)
            body = {}

            if hdr.isOK():
                req_info.end()      # Request succeeded.
                if content:
                    body = json.loads(content)
                else:
                    self.logger.warn('Request succeeded, with no response body')
                break
            self.request_error_count += 1
            if req_info.try_count > self.retry_limit:
                self.logger.error(('Retry limit %d reached, abandoning ' +
                        'request for %r'), self.retry_limit, path)
                raise APIRequestError(hdr)

            if hdr.rateLimitExceeded():
                self.logger.warn('Hit the rate limit, sleeping for %f seconds.',
                        self.rate_limit_sleep)
                time.sleep(self.rate_limit_sleep)
            elif hdr.isTransientError():
                self.logger.warn('Transient error: %s, retrying in %f seconds.',
                        str(hdr), self.rate_limit_sleep)
                time.sleep(self.rate_limit_sleep)
            else:
                self.logger.error("Request error: %r", hdr)
                raise APIRequestError(hdr)
        self.logger.info("Request for %r took: %d tries and %f seconds",
                path, req_info.try_count, req_info.duration)
        return hdr, body


    def fetchUserProfile(self, user='me'):
        '''
        Fetch information about a user.
        By default, the user is determined by the token -- the 'me' user.
        '''
        path = 'user/' + user
        hdr, body = self.request(path, 'GET')
        if hdr.isOK():
            user_profile = UserProfile(body)
            return user_profile


    def fetchSheetList(self, use_cache=False):
        '''
        Fetch a list of sheets.
        The list returned may be cached to avoid repeated redundant requests.
        The sheets are returned as SheetInfo objects.
        '''
        path = 'sheets'
        sheet_list = []
        if not (use_cache and len(self._sheet_list_cache) != 0):
            hdr, body = self.request(path, 'GET')
            for sheet_info in body:
                sheet_list.append(SheetInfo(sheet_info, self))
            if use_cache:
                self._sheet_list_cache = copy.copy(sheet_list)
        if use_cache:
            return copy.copy(self._sheet_list_cache)
        else:
            return sheet_list


    def fetchSheetInfoByName(self, name, use_cache=False):
        '''
        Fetch the SheetInfo for all sheets that have the given name.
        Set use_cache=True to avoid refetching the list of all the SheetInfos.
        May return 0, 1 or more SheetInfo objects in a list.
        '''
        sheets = self.fetchSheetList(use_cache=use_cache)
        matches = [si for si in sheets if si.name == name]
        return matches


    def fetchSheetInfoByPermalink(self, permalink, use_cache=False):
        '''
        Fetch the SheetInfo for the sheet that has the specified permalink.
        Set use_cache=True to avoid refetching the list of all the SheetInfos.
        Returns exactly 0 or 1 SheetInfo objects.
        '''
        sheets = self.fetchSheetList(use_cache=use_cache)
        matches = [si for si in sheets if si.permalink == permalink.strip()]
        if len(matches) > 1:
            raise SheetIntegrityError("Multiple sheets had the same " +
                    "permalink: %r" % [str(si) for si in matches])
        return matches[0]


    def fetchSheetByPermalink(self, permalink, use_cache=False,
            discussions=False, attachments=False, format=False,
            filters=False, rowIds=None, columnIds=None, pageSize=None,
            page=None):
        '''
        Fetch the specified Sheet.
        May optionally fetch a variety of attributes:
            discussions, attachments, format, filters, rowIds, and columnIds
        NOTE:  Does not support pagination at the moment.
        Returns the Sheet with the specified permalink.
        '''
        si = self.fetchSheetInfoByPermalink(permalink, use_cache=use_cache)
        return self.fetchSheetById(si.id, discussions=discussions,
                attachments=attachments, format=format, filters=filters,
                rowIds=rowIds, columnIds=columnIds, pageSize=pageSize,
                page=page)


    def fetchSheetById(self, sheet_id, discussions=False, attachments=False,
            format=False, filters=False, source=None, rowNumbers=None,
            rowIds=None, columnIds=None, pageSize=None, page=None):
        '''
        Fetch the specified Sheet.
        May optionally fetch a variety of attributes:
            discussions, attachments, format, filters, rowIds, and columnIds
        NOTE:  Does not support pagination at the moment.
        Returns the specified Sheet.
        '''
        path = 'sheet/' + str(sheet_id)
        path_params = []

        include = []
        if discussions: include.append('discussions')
        if attachments: include.append('attachments')
        if format:
            include.append('format')
            self.logger.warn('SDK support for formats is MASSIVELY incomplete.')
        if filters: include.append('filters')
        if rowNumbers: include.append(','.join(rowNumbers))
        # FIXME: rowNumbers support is completely untested.
        path_params.append("include=" + ','.join(include))

        if rowIds:
            path_params.append('rowIds=' + 
                    ','.join([str(r) for r in rowIds]))
        if columnIds:
            path_params.append('columnIds=' + 
                    ','.join([str(c) for c in columnIds]))

        if path_params:
            path += '?' + ','.join(path_params)

        hdr, body = self.request(path, 'GET')
        if hdr.isOK():
            request_parameters = {
                    'discussions': discussions, 'attachments': attachments,
                    'format': format, 'filters': filters, 'rowIds': rowIds,
                    'columnIds': columnIds, 'pageSize': pageSize, 'page': page}
            sheet = Sheet(body, self, request_parameters)
            return sheet
        else:
            raise Exception("Unable to fetch sheet by ID" + str(hdr))


    def createSheet(self, name, columns, location=''):
        '''
        Create a new sheet in Smartsheet.
        Returns the SheetInfo object (from which the whole Sheet can be
        loaded using the `.loadSheet()` method).
        At least one column must be specified -- as a Column instance with
        a None sheet value.
        Valid location values are:
         * '' - the default location for sheets.
         * Folder().location - To create a sheet in a folder
         * Workspace().location - To create a sheet in a workspace.
        Note that the Sheet starts out with no Rows.
        Raises SmartsheetClientError if it is unable to create the Sheet.
        '''
        if len(columns) < 1:
            err = "Must specify at least 1 column"
            self.logger.error(err)
            raise SmartsheetClientError(err)
        path = location + '/sheets'
        acc = {'name': name, 
                'columns': [col.flattenToCreationFields() for col in columns]}
        hdr, body = self.request(path,
                method='POST',
                extra_headers={'Content-Type': 'application/json'},
                body=json.dumps(acc))
        if hdr.isOK():
            return SheetInfo(body['result'], self)
        else: 
            self.logger.error("Failed creating sheet: %s", str(hdr))
            raise SmartsheetClientError("Failed creating sheet: %s" % str(hdr))

    def __str__(self):
        return '<SmartsheetClient user:%r>' % self.user


    def __repr__(self):
        return str(self)



class Folder(object):
    # FIXME:  This class is massively incomplete.
    def __init__(self, folderId):
        self.folderId = folderId
        self.location = '/folder/%s' % str(self.folderId)



class Workspace(object):
    # FIXME:  This class is massively incomplete.
    def __init__(self, workspaceId):
        self.workspaceId = workspaceId
        self.location = '/workspace/%s' % str(self.workspaceId)




class TopLevelThing(object):
    '''
    Some objects in the Smartsheet API more "naturally" have a client
    associated with them than others.  In general, the objects that can
    contain other objects are TopLevelThings.  Naturally, all objects
    exposed by the API can be fetched directly, but most are encountered
    as the result of fetching some other object (such as a Sheet, a
    Container, or a Workspace).

    The principal aspect of a TopLevelThing is that it has direct access
    to a SmartsheetClient instance.  Non-TopLevelThings that need a client
    must either be provided the client instance by the caller or "get to"
    a client instance.
    '''
    # TODO:  This class needs a better name than 'TopLevelThing'
    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client):
        self._client = client
        return self._client

    @property
    def parent(self):
        return None

    @parent.setter
    def parent(self, parent):
        raise Exception("Can't set .parent on a TopLevelThing")

    @property
    def logger(self):
        return self.client.logger

    @logger.setter
    def logger(self, logger):
        raise Exception("Only the client should set .logger")

    def markDirty(self):
        '''
        Mark this object as having a new value that should be saved.
        If this is a composite object, it may contain objects to be saved.
        '''
        self._dirty = True
        return self

    def isDirty(self):
        '''
        Return True if this object should be saved.
        '''
        return self._dirty

    def markClean(self):
        '''
        Mark this object as clean -- it doesn't need to be saved.
        '''
        self._dirty = False
        return self



class ContainedThing(object):
    '''
    Most objects in the Smartsheet API are "naturally" contained within
    other objects.  A ContainedThing that needs a client instance must
    either be passed it by the caller or "get to" a client instance by 
    traversing "up" (or down, depending on how you see object trees being
    rooted) to the TopLevelThing instance that has a client instance.
    '''
    # TODO:  This class needs a better name than 'ContainedThing'.
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
        return self._parent

    @property
    def client(self):
        return self.parent.client

    @client.setter
    def client(self, client):
        # NOTE:  This might be incorrect.
        raise Exception("Can't set .client on a ContainedThing")

    @property
    def logger(self):
        return self.client.logger

    @logger.setter
    def logger(self, logger):
        raise Exception("Can't set .logger on a ContainedThing")

    def markDirty(self):
        '''
        Mark this object as having a new value that should be saved.
        '''
        self._dirty = True
        self.parent.markDirty()
        return self

    def isDirty(self):
        '''
        Return True if this object is dirty and should be saved.
        '''
        return self._dirty

    def markClean(self):
        '''
        Mark this object as clean -- it doesn't need to be saved.
        '''
        self._dirty = False
        return self



class Sheet(TopLevelThing, object):
    '''
    The Sheet, it may or may not be fully populated.
    When a Sheet is first fetched, the Rows in it are not fully populated.
    Getting fully populated rows takes 
    '''
    field_names = '''id name columns rows accessLevel discussions
                    attachments effectiveAttachmentOptions readOnly
                    createdAt modifiedAt permalink ganttEnabled
                    dependenciesEnabled favorite showParentRowsForFilters
                    version workspace totalRowCount'''.split()
    # TODO: Can the user supply a default value for EmptyCells?
    # This would let the caller avoid having to deal with None values if
    # they are "walking through" Cells.

    def __init__(self, fields, client, request_parameters=None):
        self.fields = fields
        self.client = client
        self.request_parameters = request_parameters or {}
        self._columns = None
        self._column_id_map = None
        self._rows = None
        self._attachments = None
        self._discussions = None
        self._dirty = False

    @property
    def id(self):
        return self.fields['id']

    @property
    def name(self):
        return self.fields['name']

    @property
    def columns(self):
        if self._columns is None:
            self._columns = [
                    Column.newFromAPI(c, self) for c in 
                        self.fields.get('columns', [])]
            self._column_id_map = dict([(c.id, c) for c in self._columns])
        return self._columns

    @property
    def rows(self):
        # TODO: On the first access of any Row, all of the Rows get built.
        # It might be nicer to do a more on-demand construction of the rows.
        # TODO: Should we keep SheetRows?
        # I don't know that there's really a point to it anymore.
        if self._rows is None:
            self._rows = [Row.newFromAPI(r, self) for r in 
                    self.fields.get('rows', [])]
        return self._rows

    @property
    def accessLevel(self):
        return self.fields.get('accessLevel')

    @property
    def discussions(self):
        if self._discussions is None:
            self._discussions = [Discussion(d,
                AncillaryObjectSourceSheet(self), self) for d
                    in self.fields.get('discussions', []) ]
        return self._discussions

    @property
    def attachments(self):
        if self._attachments is None:
            self._attachments = [Attachment(a,
                AncillaryObjectSourceSheet(self), self) for a
                    in self.fields.get('attachments', []) ]
        return self._attachments

    @property
    def effectiveAttachmentOptions(self):
        return self.fields.get('effectiveAttachmentOptions', [])

    @property
    def readOnly(self):
        return self.fields.get('readOnly', False)

    @property
    def createdAt(self):
        return self.fields.get('createdAt')

    @property
    def modifiedAt(self):
        return self.fields.get('modifiedAt')

    @property
    def permalink(self):
        return self.fields.get('permalink')
 
    @property
    def ganttEnabled(self):
        return self.fields.get('ganttEnabled')

    @property
    def dependenciesEnabled(self):
        return self.fields.get('dependenciesEnabled')

    @property
    def favorite(self):
        return self.fields.get('favorite', False)

    @property
    def showParentRowsForFilters(self):
        return self.fields.get('showParentRowsForFilters', False)

    @property
    def version(self):
        return self.fields.get('version')

    @property
    def workspace(self):
        # NOTE: This doesn't seem to be a documented Sheet attribute.
        return self.fields.get('workspace')

    @property
    def totalRowCount(self):
        return self.fields.get('totalRowCount')

    def allDiscussions(self, include_rows=True):
        '''
        Get a list of all the Discussions on the Sheet.
        NOTE: The Sheet must have been fetched with discussions.
        '''
        acc = []
        acc.extend(self.discussions)
        if include_rows:
            for r in self.rows:
                acc.extend(r.discussions)
        return acc

    def getColumnById(self, column_id):
        '''
        Return the Column that has the specified ID.
        '''
        try:
            if self._column_id_map is None:
                list(self.columns)
            return self._column_id_map[column_id]
        except KeyError, e:
            raise UnknownColumnId("Column ID: %r is not in current columns.")

    def getColumnByIndex(self, column_index):
        '''
        Get the Column at the specified index, or return None if not found.
        '''
        try:
            found = False
            col = self.columns[column_index]
            if col.index == column_index:
                found = True
            else:
                for col in self.columns:
                    if col.index == column_index:
                        found = True
                        break
            if found:
                return col
            return None
        except IndexError:
            return None

    def allAttachments(self, include_rows=True, include_discussions=False):
        '''
        Get a list of all the Attachments to the Sheet.
        NOTE: The way the Sheet was fetched impacts whether or not all all of
              the Attachments are available.  For ALL Attachments to be
              available, it must have been fetched with:
                'include=discussions,attachments,...'
        To get ALL of the attachments, both the 'include_rows' and
        'include_discussions' parameters need to be true.  Without
        'include_discussions' being true, then only the attachements on the
        Sheet directly or on Rows directly will be returned.
        '''
        acc = []
        acc.extend(self.attachments)
        if include_rows:
            for r in self.rows:
                acc.extend(r.attachments)
        if include_discussions:
            for d in self.discussions:
                acc.extend(d.commentAttachments)
            if include_rows:
                for r in self.rows:
                    for d in r.discussions:
                        acc.extend(d.commentAttachments)
        return acc

    def getAttachmentByFileName(self, file_name, include_rows=False,
            include_comments=False):
        '''
        Find the named attachment, looking, potentially, at rows and comments.
        Returns the corresponding Attachment object.
        NOTE: The Sheet must have been fetched with attachment info.
        '''
        for a in self.attachments:
            if a.name == file_name:
                return a
        if include_rows:
            for r in self.rows:
                a = r.getAttachmentByFileName(file_name)
                if a:
                    return a
        if include_comments:
            raise NotImplementedError("Attachments on Comments not supported")

    def getRowByRowNumber(self, row_number):
        '''
        Fetch the Row with the specified row number.
        The numbering for rows starts at 1.
        This is distinct from Columns which have indexes that start at 0.
        Returns the Row.
        Raises an IndexError exception if the Row is not found.
        '''
        if not self.rows:
            err = "Sheet %r has no Rows" % self
            self.logger.error(err)
            raise IndexError(err)
        if row_number < 1:
            err = ("Row # %d invalid for Sheet %r, row numbers start at 1" %
                    (row_number, self))
            self.logger.error(err)
            raise IndexError(err)

        # Optimize for having all of the Rows and them being in order.
        if self.rows[0].rowNumber == 1:
            idx = row_number - 1
            if idx <= len(self.rows):
                if self.rows[idx].rowNumber == row_number:
                    return self.rows[idx]

        for row in self.rows:
            if row.rowNumber == row_number:
                return row
        raise IndexError("Row # %d not found." % row_number)

    def getRowById(self, rowId):
        '''
        Fetch a Row by its ID.
        '''
        matches = [row for row in self.rows if row.id == rowId]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            err = "Sheet.getRowById(): Multiple rows with ID %r" % rowId
        else:
            err = "Sheet.getRowById(): No row with ID %r" % rowId
        self.logger.warn(err)
        raise SmartsheetClientError(err)

    def __getitem__(self, row_number):
        '''
        Add a list-style interface to fetching a Row.
        The index is the row_number (1-based) and not a classic (0-based) index.
        '''
        return self.getRowByRowNumber(row_number)

    def __iter__(self):
        return iter(self._rows)

    def __len__(self):
        return len(self.rows)

    def makeRow(self):
        '''
        Create a new Row.

        The Row uses the Sheet (for column information), but is not
        "attached" to the Sheet (it isn't found in Sheet.rows()).
        In order to attach the Row to the Sheet, it must be placed in a
        RowWrapper and the RowWrapper passed to the `addRows()` method on
        the Sheet.
        '''
        return Row(self)

    def addRow(self, row, position='toBottom', parentId=None, siblingId=None,
            client=None, strict=True):
        '''
        Add a single Row to the Sheet.

        See the documentation for the RowWrapper class for details on the
        placement arguments: 'position', 'parentId', and 'siblingId'.
        
        @param row The Row to add - the Row may be empty.
        @param position Where to insert the Row ('toTop' or 'toBottom')
        @param parentId ID of the parent Row to insert `row` under.
        @param siblingID ID of the Row to insert `row` next to 
        @param client The client to use (if not using sheet.client).
        @param strict True for the API server to do strict Cell parsing.
        @return The Sheet.
        '''
        row_wrapper = RowWrapper(self, position=position, parentId=parentId,
                siblingId=siblingId)
        row_wrapper.addRow(row)
        return self.addRows(row_wrapper, client=client, strict=strict) 

    def addRows(self, row_wrapper, client=None, strict=True):
        '''
        Add the Row(s) in the RowWrapper to the Sheet.
        The RowWrapper specifies *where* in the Sheet the Row(s) should be
        added.
        @param row_wrapper The Rows with their position information.
        @param client The client to use (if not using sheet.client).
        @param strict True for the API server to do strict Cell parsing.
        @return The Sheet.
        '''
        path = '/sheet/%s/rows' % str(self.id)
        client = client or self.client
        hdr, body = client.request(path, 'POST',
                extra_headers=client.json_headers,
                body=json.dumps(row_wrapper.flattenForInsert()))

        if not hdr.isOK():
            err = "Sheet.addRows() failed: %s" % str(hdr)
            self.logger.error(err)
            raise SmartsheetClientError(err)

        self.logger.debug("Sheet.addRows() succeeded")
        row_wrapper.discard()
        if isinstance(body['result'], list):
            for row_fields in body['result']:
                new_row = Row.newFromAPI(row_fields, self)
                # It's worth noting that the order of the .rows array can get
                # all out of whack with respect to Row.rowNumber as we add
                # and move and remove Rows this way.  Perhaps there should
                # be a periodic resorting of it.
                self.rows.append(new_row)
        else:
            err = ("Unexpected body type returned: %r, %s" % 
                    (type(body['result']), body))
            self.logger.error(err)
            raise SmartsheetClientError(err)
        return self

    def _replaceRow(self, new_row):
        '''
        Replace a row with a different version of it.
        '''
        # FIXME:  Should this method be exposed to library users?
        # I think it is only needed internally to handle incorporation of
        # the updated Row from saving a Row.
        replace_idx = None
        orig_row = self.getRowById(new_row.id)
        for idx, row in enumerate(self.rows):
            if row.id == new_row.id:
                replace_idx = idx
                break
        if replace_idx is not None:
            self.rows[replace_idx] = new_row
        orig_row.discard()
        return self

    def refetch(self, client=None):
        '''
        Refetch the Sheet - using the original fetch options.
        Returns a new instance of the Sheet.
        It unfortunately does not do an in-place refresh.
        '''
        client = client or self.client
        return client.fetchSheetById(self.id, **self.request_parameters)

    def __str__(self):
        return '<Sheet id:%r, name:%r>' % (self.id, self.name)

    def __repr__(self):
        return str(self)

    def __getitem__(self, row_number):
        '''
        Add a list-style interface to fetching a Row from the sheet.
        The index is the row_number (1-based) and not a classic (0-based) index.
        '''
        return self.getRowByRowNumber(row_number)

    def __iter__(self):
        return iter(self.rows)
 


class RowWrapper(object):
    '''
    Specifies the expansion state and/or position of one or more Rows.
    The Rows are contiguous.
    '''
    def __init__(self, sheet, position='toBottom', expanded=True, parentId=None,
            siblingId=None, *rows):
        '''
        If the Rows are to be children of a parent Row, then the position is
        relative to the parent Row (either the first children
        (position=='toTop'), or the last children (position=='toBottom')).
        `parentId` and `siblingId` are mutually exclusive.

        @param sheet The sheet this RowWrapper is for.
        @param position 'toBottom' (default) or 'toTop'
        @param expanded Whether or not the Rows should be expanded.
        @param parentId Put the Rows as children of this Row.id.
        @param siblingId Put the Rows as the next sibling of this Row.id.
        @param rows A list of Rows these position+expansion applies to.
        '''
        # TODO: Should we let the caller pass us a Row for parent or sibling?
        # This might be less annoying for them than passing us a_row.id.
        if position not in ('toBottom', 'toTop'):
            err = "position must be 'toBottom' or 'toTop', got %r" % position
            sheet.logger.error(err)
            raise SmartsheetClientError(err)
        if parentId is not None and siblingId is not None:
            err = "parentId and siblingId are mutually exclusive"
            sheet.logger.error(err)
            raise SmartsheetClientError(err)

        self.position = position
        self.parentId = parentId
        self.siblingId = siblingId
        self.expanded = expanded
        self.rows = []
        self.rows.extend(rows)

    def addRow(self, row):
        '''
        Add a Row to this RowWrapper.
        '''
        self.rows.append(row)
        return self

    def flatten(self, strict=True):
        '''
        Flatten the RowWrapper.
        '''
        acc = {}
        if self.position == 'toTop':
            acc['toTop'] = True
        else:
            acc['toBottom'] = True
        if self.expanded is not None:
            acc['expanded'] = self.expanded
        if self.parentId is not None:
            acc['parentId'] = self.parentId
        if self.siblingId is not None:
            acc['siblingId'] = self.siblingId

        acc['rows'] = []
        for row in self.rows:
            acc['rows'].append(row.flattenForInsert(strict=strict))
        return acc

    def flattenForInsert(self, strict=True):
        '''
        Flatten the RowWrapper for inserting Rows.
        When inserting Rows, the 'expanded' parameter is not permitted.
        '''
        acc = self.flatten(strict=strict)
        if 'expanded' in acc:
            del acc['expanded']
        return acc

    def discard(self):
        '''
        Mark each of the Rows as discarded.
        This is called after the RowWrapper has been used and the Rows are 
        now incorporated into the Sheet.
        '''
        for row in self.rows:
            row.discard()



class CellTypes(object):
    # TODO: Should this be an enum class?
    TextNumber = u'TEXT_NUMBER'
    Picklist = u'PICKLIST'
    Date = u'DATE'
    ContactList = u'CONTACT_LIST'
    Checkbox = u'CHECKBOX'
    EmptyCell = u'EMPTY_CELL'   # This must not be sent to the server.



class Row(ContainedThing, object):
    '''
    A row from a sheet.
    '''
    field_names = '''id sheetId rowNumber parentRowNumber cells
                    discussions attachments columns expanded createdAt
                    modifiedAt accessLevel version format filteredOut'''.split()

    def __init__(self, sheet):
        '''
        Create a new Row object.

        A newly created Row is empty.
        Cells can be added to it prior to saving it, but other objects that
        are "hung off" the Row (such as discussions and attachments) must be
        added after the Row has been saved to the Sheet.
        '''
        # TODO: Make discarding a Row actually matter.
        self._id = -1           # Invalid ID
        self.sheet = sheet
        self.parent = sheet
        self._rowNumber = -1    # Invalid row number
        self._parentRowNumber = 0   # Initially, no parent Row.
        self._cells = []
        self._discussions = []
        self._attachments = []
        self._columns = None
        self._column_id_map = None
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
        self.change = None

    @classmethod
    def newFromAPI(cls, fields, sheet):
        row = Row(sheet)
        row.fields = fields
        row.sheet = sheet
        row.parent = sheet     # The Row belongs to the Sheet.

        row._id = fields['id']
        row._rowNumber = fields['rowNumber']
        row._parentRowNumber = fields.get('parentRowNumber', 0)
        row._cells = [Cell.newFromAPI(c, row) for c in fields.get('cells', [])]

        # When a Row is fetched directly, the caller can choose to get
        # the Columns with the Row.  Use them if they show up.
        row._columns = [
                Column.newFromAPI(c, row) for c in fields.get('columns', [])
        ]
        row._column_id_map = dict([(c.id, c) for c in row._columns])

        # When a Sheet is fetched or a Row is fetched directly, the caller
        # can have the API include the Discussions along with the Row.
        row._discussions = [
                Discussion(d, 
                    AncillaryObjectSourceRow(sheet, row), sheet)
                for d in fields.get('discussions', [])
        ]

        # When a Sheet is fetched or a Row is fetched directly, the caller
        # can have the API include the Attachments along with the Row.
        row._attachments = [
                Attachment(a,
                    AncillaryObjectSourceRow(sheet, row), sheet)
                for a in fields.get('attachments', [])
                ]

        if 'expanded' in fields:
            row._expanded = fields['expanded']
        if 'version' in fields:
            row._version = fields['version']
        if 'format' in fields:
            row._format = fields['format']
        if 'createdAt' in fields:
            row._createdAt = fields['createdAt']
        if 'modifiedAt' in fields:
            row._modifiedAt = fields['modifiedAt']
        if 'accessLevel' in fields:
            row._accessLevel = fields['accessLevel']
        if 'filteredOut' in fields:
            row._filteredOut = fields['filteredOut']

        # Rows from the API don't start out dirty.
        row._dirty = False
        return row


    @property
    def id(self):
        return self._id

    @property
    def sheetId(self):
        return self.sheet.id

    @property
    def rowNumber(self):
        return self._rowNumber

    @property
    def parentRowNumber(self):
        return self._parentRowNumber

    @property
    def cells(self):
        return self._cells

    @property
    def discussions(self):
        return self._discussions

    @property
    def attachments(self):
        return self._attachments

    @property
    def columns(self):
        if self._columns:
            return self._columns
        return self.sheet.columns

    def getColumnById(self, column_id):
        '''Return the Column that has the specified ID.'''
        # Use the local columns info if it exists, otherwise use the Sheet.
        if self._columns:
            return self._column_id_map[column_id]
        return self.sheet.getColumnById(column_id)

    @property
    def expanded(self):
        return self._expanded

    @property
    def createdAt(self):
        return self._createdAt

    @property
    def modifiedAt(self):
        return self._modifiedAt

    @property
    def accessLevel(self):
        return self._accessLevel

    @property
    def version(self):
        return self._version

    @property
    def format(self):
        return self._format

    @property
    def filteredOut(self):
        return self._filteredOut

    def discard(self):
        '''
        Mark the row and its contained objects as discarded.
        Operations on a discarded item will raise SheetIntegrityErrors.
        TODO: This doesn't do anything yet, it just no-ops.
        '''
        self._discarded = True


    def getAttachmentByFileName(self, file_name):
        '''
        Return the named Attachment object, or None if not found.
        '''
        for a in self.attachments:
            if a.name == file_name:
                return a
        return None

    def getColumnByIndex(self, idx):
        '''
        Find the Column on this Row at the specified index.
        Returns the Column with the given index or raises IndexError.

        This method is only defined for Rows that either have a valid
        Sheet reference or were fetched with their columns information.
        @param idx
        '''
        if not self._columns:
            return self.sheet.getColumnByIndex(idx)

        if idx < 0:
            raise IndexError("Negative column indexes are not supported.")

        # Short circuit for when all the columns were fetched with the Row.
        # Theoretically, this should be the common case.
        if idx < len(self.columns):
            col = self.columns[idx]
            if col.index == idx:
                return col

        try:
            for col in self._columns:
                if col.index == idx:
                    return col
        except IndexError, e:
            # We raise StopIteration so list(a_row) and [x in a_row) work.
            raise StopIteration
        err = "Column index %r not found on Row: %r" % (idx, self)
        self.logger.error(err)
        raise IndexError(err)

    def getCellByIndex(self, idx):
        '''
        Get the Cell at the specified index on this Row.
        Columns indexes start at 0.
        If the index is valid but there is no Cell there on this Row,
        an empty Cell is returned.
        Raises IndexError if the index is invalid.
        '''
        column = self.getColumnByIndex(idx)
        if column is None:
            raise IndexError
        cell = self.getCellByColumnId(column.id)
        if cell is None:
            cell = Cell(self, column, None, type=CellTypes.EmptyCell,
                    isDirty=False)
        return cell

    def getCellByColumnId(self, column_id):
        '''
        Get the Cell on this row at the specified Column ID.
        Returns the Cell or None if there is no Cell at that Column ID.
        '''
        # TODO: Consider having a map of columnId to Cell
        for c in self.cells:
            if c.columnId == column_id:
                return c
        return None

    def addSaveData(self, rowchange):
        '''
        If this Row has changed, add its change data to the RowChangeSaveData.
        '''
        if not self.isDirty():
            return
        rowchange.addRowChange(self.change)
        return self

    def save(self, client=None):
        '''
        Save this Row to the server.

        Any changes (new Cells, format, position, or expansion) on the Row
        are saved to the API server.

        Once saved, this Row is replaced by the Row constructed from the
        data returned by the server.  The caller should not hold a reference
        to it past calling `save()`.
        @return The Row constructed from the data returned by the server.
        '''
        client = client or self.client
        path = ('/sheet/%s/row/%s' %
                (str(self.sheet.id), str(self.id)))
        rc = RowChangeSaveData(self)
        self.addSaveData(rc)
        for cell in self.cells:
            cell.addSaveData(rc)
        return self.saveRowChange(rc, client=client)

    def saveRowChange(self, row_change, client=None):
        '''
        Save a Row that has been changed (as opposed to a newly created Row).
        @param row_change The RowChangeSaveData for the changed Row.
        @return The Row constructed from the data returned by the server.
        '''
        client = client or self.client
        path = ('/sheet/%s/row/%s' %
                (str(self.sheet.id), str(self.id)))
        hdr, body = client.request(path, 'PUT',
                extra_headers=client.json_headers,
                body=row_change.toJSON())

        if not hdr.isOK():
            err = "Row.save() failed: %s" % str(hdr)
            self.logger.error(err)
            raise SmartsheetClientError(err)

        self.logger.debug("Row.save() succeeded")

        if isinstance(body['result'], list):
            if len(body['result']) != 1:
                self.logger.warn("Expected 1 row, got %d", len(body['result']))
            new_row = Row.newFromAPI(body['result'][0], self.sheet)
            self.sheet._replaceRow(new_row)
            return new_row
        else:
            err = ("Unexpected body type returned: %r, %s" % 
                    (type(body['result']), body))
            self.logger.error(err)
            raise SmartsheetClientError(err)

    def flattenForInsert(self, strict=True):
        '''
        Flatten this Row's data so it can be inserted (as opposed to saved).
        '''
        acc = {'cells': []}
        for cell in self.cells:
            if cell.type != CellTypes.EmptyCell or cell.value is not None:
                acc['cells'].append(cell.flattenForInsert(strict=strict))
        return acc

    def __getitem__(self, idx):
        '''
        Enable indexing a Row object to fetch the cell in the indicated column.
        This allows a Row to be used like a Python list.
        Column indexes start at 0.
        NOTE:  Negative indexes are not supported.
        Returns the Cell at the specified column
        '''
        if idx >= 0:
            return self.getCellByIndex(idx).value
        raise Exception("Invalid column index: %r" % idx)

    def __setitem__(self, idx, value):
        '''
        Enable indexing a Row object to set the value in the indicated column.
        This allows a Row to be used like a Python list.
        Column indexes start at 0.
        NOTE:  Negative indexes are not supported.
        '''
        if idx >= 0:
            cell = self.getCellByIndex(idx)
            cell.assign(value)
            self.markDirty()
        else:
            raise IndexError("Invalid column index: %r" % idx)

    def __len__(self):
        '''
        Calling len(a_row) will return the # of columns.
        '''
        return len(self.sheet.columns)

    def __str__(self):
        return '<Row id:%r rowNumber:%r>' % (self.id, self.rowNumber)

    def __repr__(self):
        return str(self)



class Column(ContainedThing, object):
    '''
    Track the details, but not data, of a column in a Sheet.
    Many of the fields are optional.
    '''
    field_names = '''id index title primary type options hidden symbol
                    systemColumnType autoNumberFormat tags width format
                    filter'''.split()

    def __init__(self, title, type=CellTypes.TextNumber, primary=False,
            symbol=None, options=None, systemColumnType=None,
            autoNumberFormat=None, width=None, sheet=None):
        '''
        The Column attributes that can be set when creating a Column are
        available via initialization.
        '''
        self.title = title
        self.type = type
        self.primary = primary
        self.options = options or []
        self.symbol = symbol
        self.systemColumnType = systemColumnType
        self.autoNumberFormat = autoNumberFormat
        self.width = width
        self.sheet = sheet
        self.id = -1            # Undefined
        self.index = None       # FIXME: can we know this at creation time?
        self.hidden = False
        self.tags = []
        self.format = None
        self.filter = None
        self.parent = sheet
        self.fields = {}

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
        col.id = fields['id']
        col.index = fields['index']
        maybeAssignFromDict(fields, col, 'hidden')
        maybeAssignFromDict(fields, col, 'tags')
        maybeAssignFromDict(fields, col, 'format')
        maybeAssignFromDict(fields, col, 'filter')
        col._dirty = False
        col.fields = fields
        return col

    def flattenToCreationFields(self):
        '''
        Return a dict containing the fields used by the API for Column creation.
        '''
        acc = {'title': self.title,
                'primary': self.primary,
                'type': self.type }
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
        return acc

    def __str__(self):
        return '<Column id:%d index:%r type:%r>' % (
                self.id, self.index, self.type)

    def __repr__(self):
        return str(self)



class CellHyperlink(object):
    def __init__(self, url=None, sheetId=None, reportId=None):
        if 1 != len([x for x in (rule, sheetId, reportId) if x is not None]):
            raise SmartsheetClientError("Must specify one of url, sheetId, " +
                    "or reportId")
        self.url = url
        self.sheetId = sheetId
        self.reportId = reportId

    def flatten(self):
        acc = {}
        if self.url is not None:
            acc['url'] = self.url
        elif self.sheetId is not None:
            acc['sheetId'] = self.sheetId
        elif self.reportId is not None:
            acc['reportId'] = self.reportId
        return acc

    def toJSON(self):
        '''Return as a JSON blob suitable for passing to the API server.'''
        json.dumps(self.flatten())

    def __str__(self):
        return ('<CellHyperlink: url: %r  sheetId: %r  reportId: %r' %
                (self.url, self.sheetId, self.reportId))
    
    def __repr__(self):
        return str(self)



class CellLinkIn(object):
    def __init__(self, sheetId, rowId, columnId):
        self.sheetId = sheetId
        self.rowId = rowId
        self.columnId = columnId

    def flatten(self):
        acc = { 'sheetId': self.sheetId,
                'rowId': self.rowId,
                'columnId': self.columnId }
        return acc

    def toJSON(self):
        return json.dumps(self.flatten())

    def __str__(self):
        return ('<CellLinkIn: sheetId: %r  rowId: %r  columnId: %r' %
                (self.sheetId, self.rowId, self.columnId))



class CellChange(object):
    '''
    The data about a change to a Cell.
    '''
    # FIXME: Error 1115 says mixing link and value updates is not accepted.
    # Is this restriction Cell-scoped or Row scoped (can I update the value
    # of one Cell on a Row and the link in a different Cell on the same Row)?

    # FIXME: Error 1109 - 1113 should probably be addressed prior to save.
    # When changing multiple Cells on a Row, it may take multiple save
    # operations -- that's going to be problematic since each save operation
    # replaces the live Row on the Sheet.  We need to at least detect that
    # we have orphaned change operations.

    def __init__(self, cell, new_value, strict=None, format=None,
            hyperlink=None, linkInFromCell=None):
        self.cell = cell
        self.new_value = new_value
        self.strict = strict
        self.format = format
        self.hyperlink = hyperlink
        self.linkInFromCell = linkInFromCell

    def flatten(self):
        acc = { 'columnId': self.cell.columnId,
                'value': self.new_value }
        if self.strict:
            acc['strict'] = True
        else:
            acc['strict'] = False
        if self.format:
            acc['format'] = unicode(self.format)
        if self.hyperlink:
            acc['hyperlink'] = self.hyperlink.flatten()
        if self.linkInFromCell:
            acc['linkInFromCell'] = self.linkInFromCell.flatten()
        return acc

    def toJSON():
        return json.dumps(self.flatten())



class Cell(ContainedThing, object):
    '''
    A Cell on a Row in a Sheet.
    A Cell consists of two types of information, the first is structural and
    the second is value.  A Cell's structure indicates its Row and Column,
    while its value contains its value and displayValue, as well as
    format, formula, and links (hyperlinks and cell links).

    A Cell may be empty, which would be the case in a sparse Sheet, in which
    case the Cell would have structural data, but no value information.

    A Cell does not have a unique ID, instead, each Cell is identified by the
    tuple of (row ID, column ID).
    '''
    max_display_len = 10
    def __init__(self, row, column, value, type=None,
            displayValue=None, hyperlink=None, linkInFromCell=None,
            format=None, link=None, isDirty=True, immediate=False):
        '''
        Initialize a new Cell.
        Note that the library user is not able to assign all of the same
        attributes that the API can.
        If isDirty is True, then the Cell needs to be saved.  If immediate
        is True, then the Cell will be saved immediately (rather than lazily
        with the Row or Sheet).
        '''
        if link:
            raise DeprecatedAttribute("'link' attribute of Cell is deprecated")

        if type is None:
            type = column.type

        if hyperlink is not None and not isinstance(hyperlink, CellHyperlink):
            err = "hyperlink must be None or a CellHyperlink object"
            self.logger.error("%s, got: %r", err, hyperlink)
            raise SmartsheetClientError(err)

        if (linkInFromCell is not None and 
                not isinstance(linkInFromCell, CellLinkIn)):
            err = "linkInFromCell must be None or a CellLinkIn object"
            self.logger.error("%s, got: %r", err, linkInFromCell)
            raise SmartsheetClientError(err)

        self.row = row
        self.parent = row
        self.columnId = column.id
        self._value = value
        self._displayValue = displayValue
        self.type = type
        self.hyperlink = hyperlink
        self.linkInFromCell = linkInFromCell
        self.linksOutToCells = None # Not settable by library user.
        self.format = format
        self.formula = None        # Not settable by library user.
        self.link = None
        self.modifiedAt = None      # Not settable by library user.
        self.modifiedBy = None      # Not settable by library user.
        self._dirty = isDirty
        self.change = None
        self.isDeleted = False

        if immediate:
            # FIXME: Save this Cell right now.
            raise NotImplementedError("immediate save of Cell not implemented")

    @classmethod
    def newFromAPI(cls, fields, row):
        '''
        Create a new instance from the dict of values from the API.
        '''
        column = row.sheet.getColumnById(fields['columnId'])
        cell = Cell(row, column, fields.get('value', None), type=fields['type'],
                displayValue=fields.get('displayValue', None),
                hyperlink=fields.get('hyperlink', None),
                linkInFromCell=fields.get('linkInFromCell', None),
                format=fields.get('format', None),
                link=fields.get('link', None), isDirty=False,
                immediate=False)
        # Not all attributes are setable with __init__().
        cell.formula = fields.get('formula', None)
        cell.linksOutToCells = fields.get('linksOutToCells', None),
        cell.modifiedAt = fields.get('modifiedAt', None)
        if 'modifiedBy' in fields:
            cell.modifiedBy = SimpleUser(fields.get('modifiedBy'))
        else:
            cell.modifiedBy = None
        return cell

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
        # It would be really nice if this could sensibly handle the fact
        # that a cell containing numeric data will have a string for its
        # displayValue.  It's quite probably that the caller would rather
        # get the numeric value as a numeric type.
        if (self._displayValue is not None and self._value is not None and
                isinstance(self._value, (int, long, float))):
            return self._value
        if self._displayValue is None and self._value is not None:
            return self._value
        return self._displayValue

    @value.setter
    def value(self, new_value):
        '''
        Assign a new value to the Cell.
        The new value is presumed to be the same type as the original value,
        and the assignment does not occur immediately.
        If more control over the assignment process is needed, use the
        `assign` method below.
        '''
        return self.assign(new_value)

    @property
    def realValue(self):
        '''
        Read the underlying value for the cell.
        If the Cell contains a formula, this will return the formula, instead
        of its computed value (which can be gotten via the `value` property).
        '''
        if self.formula:
            return self.formula
        return self._value

    @property
    def displayValue(self):
        return self._displayValue

    def assign(self, new_value, displayValue=None, strict=True, hyperlink=None,
            linkInFromCell=None, immediate=False, propagate=True):
        '''
        Assign a new value to the Cell.
        @param new_value The new value for the Cell.
        @param displayValue The string value of the Cell prior to save().
        @param strict True to request stict processing on save.
        @param hyperlink The CellHyperlink to set.
        @param linkInFromCell The CellLinkIn to set.
        @param immediate Apply this update to the sheet immediately.
        @param propagate When saving, (if immediate), save all changes on Row.
        '''
        if self.formula is not None:
            raise SmartsheetClientError("API does not permit formula changes")
        if len(unicode(new_value)) > 4000:
            self.logger.warn("API will truncate new cell value longer than " +
                    "4000 chars: %r", cell)
        self.change = CellChange(self, new_value, strict=strict,
                hyperlink=hyperlink, linkInFromCell=linkInFromCell)
        self._value = new_value
        if displayValue is None:
            self._displayValue = unicode(new_value)
        else:
            self._displayValue = displayValue

        # The Row is stored sparse -- we have to add formerly empty Cells.
        # A Column may only appear once on the Row, make sure we don't add
        # a duplicate.
        # TODO: Consider making Row.cells a dict.
        if self.type == CellTypes.EmptyCell:
            replace_idx = None
            for idx, cell in enumerate(self.row.cells):
                if self.columnId == cell.columnId:
                    replace_idx = idx
                    break
            if replace_idx is not None:
                self.row.cells[replace_idx] = self
            else:
                self.row.cells.append(self)

        self.markDirty()
        if immediate:
            self.save(propagate=propagate)

    def setFormat(self, format, immediate=False):
        '''
        Change the format of the cell.
        '''
        # NOTE: The save data for this requires the value, so capture it.
        raise NotImplementedError("Setting Cell format is not implemented yet")

    def delete(self, immediate=False):
        '''
        Delete this Cell.
        @param immediate Apply this update to the sheet immediately.
        '''
        # TODO: This needs to make all of the value and links fields be None.
        self.isDeleted = True
        self._value = self._displayValue = self.linkInFromCell = None
        self.linksOutToCells = self.format = self.link = self.formula = None
        self.hyperlink = self.modifiedAt = self.modifiedBy = None
        if immediate:
            # TODO: Implement Cell deletion
            raise NotImplementedError("Cell deletion is not implemented yet")

    @property
    def rowId(self):
        return self.row.id

    @property
    def column(self):
        return self.row.getColumnById(self.columnId)

    def addSaveData(self, rowchange):
        '''
        If this Cell has changed, add its change data to the RowChangeSaveData.
        '''
        if not self.isDirty():
            return
        rowchange.addCellChange(self.change)
        return self

    def save(self, client=None, propagate=True):
        '''
        Save the Cell if it has been changed.
        Successfully saving any Cell on a Row results in the full
        replacement of the Row the Cell was on.  If you are saving each
        Cell as you change it, (either by directly calling save or with the
        `immediate` flag in `assign`), that most likely won't result in
        unexpected behavior.  If, on the other hand, you are "batching up"
        Cell changes, the changes will be lost if this Cell is saved without
        `propagate` set to True.

        @param client (optional) Use a different SmartsheetClient instance.
        @param propagate (optional) False to not save any other changes on Row.
        @return The newly updated Row, or raises SmartsheetClientError.
        '''
        client = client or self.client
        path = ('/sheet/%s/row/%s' %
                (str(self.row.sheet.id), str(self.rowId)))
        rc = RowChangeSaveData(self.row)
        if propagate:       # Get all changes on this Row.
            self.row.save()
        else:               # Only worry about this Cell.
            self.addSaveData(rc)
        return self.row.saveRowChange(rc, client=client)

    def flattenForInsert(self, strict=True):
        '''
        Return a flattened form of this Cell for Row insertion.
        '''
        # TODO: consider using this approach for saving changed Cells.
        acc = {}
        if self.type == CellTypes.EmptyCell and self.value is None:
            return acc
        acc['columnId'] = self.columnId
        acc['value'] = self.value
        acc['strict'] = strict
        if self.format is not None:
            acc['format'] = self.format
        if self.hyperlink is not None:
            acc['hyperlink'] = self.hyperlink.flatten()
        # FIXME: What about linkInFromCell?
        # Is that supported for Row insertion, or only as a change to an
        # existing Cell?
        return acc
        
    def fetchHistory(self, client=None):
        '''
        Fetch the history of the Cell.
        '''
        # TODO: Consider making Cell.__getitem__ operate over Cell history.
        # That would let a Sheet be treated as a cube rows x columns x history
        # That operational model might give rise to some interesting uses.
        path = '/sheet/%s/row/%s/column/%s/history' % (
                str(self.row.sheet.id), str(self.rowId), str(self.columnId))
        client = client or self.client
        hdr, body = client.request(path, 'GET')
        if hdr.isOK():
            return [Cell.newFromAPI(c, self.row) for c in body]
        self.logger.error("Unable to fetch Cell %s history: %s", cell, str(hdr))
        raise Exception("Error fetching Cell history: %s" % str(hdr))

    def __str__(self):
        if self._displayValue is not None:
            return unicode(self._displayValue)
        return unicode(self.value)

    def __int__(self):
        '''Try to convert the value to an int.'''
        return int(self.value)

    def __long__(self):
        '''Try to convert the value to a long.'''
        return long(self.value)

    def __float__(self):
        '''Try to convert the value to a float.'''
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
        return '<Cell rowId:%r, columnId:%r, type:%r value=%r>' % (
                self.rowId, self.columnId, self.type,
                string_trim(self.value, self.max_display_len))



class RowChangeSaveData(object):
    '''
    Captures the data about changes to a Row, sufficient for saving it.
    The API manipulates certain data a Row at a time:
     * Row position (obviously)
     * Row expanded or not
     * Format
     * Cells
    '''
    # These are the potential row positions
    toTop = 'toTop'
    toBottom = 'toBottom'
    toParent = 'toParent'
    toSibling = 'toSibling'
    position_options = (toTop, toBottom, toParent, toSibling)

    def __init__(self, row):
        self.row = row
        self.cells = []
        self.expanded = None
        self.format = None
        self.position = None
        self.relative_to = None

    def addCellChange(self, cell_data):
        self.cells.append(cell_data)

    def addRowChange(self, row_data):
        # TODO: Handle format, expanded, position, and relative_to.
        pass

    def flatten(self):
        acc = {}
        if self.cells:
            acc['cells'] = [cd.flatten() for cd in self.cells]
        return acc

    def toJSON(self):
        return json.dumps(self.flatten())



class Discussion(object):
    '''
    Information about a discussion.
    Depending on how the fields were obtained, the Discussion may or may not
    contain the comments and attachments from the discussion.

    The comments and attachment information can be obtained later using
    the .refresh() method.
    '''
    field_names = '''id title comments createdBy lastCommentedAt
                lastCommentedUser commentAttachments commentsj'''.split()

    def __init__(self, fields, source, sheet):
        self.fields = fields
        self.source = source
        self.sheet = sheet
        self._attachments = None
        self._comments = None
        self._dirty = False

    @property
    def id(self):
        return self.fields['id']

    @property
    def title(self):
        return self.fields['title']

    @property
    def comments(self):
        return self.fields.get('comments', [])

    @property
    def commentAttachments(self):
        if self._attachments is None:
            self._attachments = [Attachment(a, self.source, self.sheet) for a 
                    in self.fields.get('commentAttachments', []) ]
        return self._attachments

    @property
    def lastCommentedAt(self):
        return self.fields.get('lastCommentedAt')

    @property
    def lastCommentedUser(self):
        return self.fields.get('lastCommentedUser')

    @property
    def createdBy(self):
        return SimpleUser(self.fields.get('createdBy'))

    def getAttachmentByFileName(self, file_name):
        '''
        Return the named Attachment object, or None if not found.
        '''
        for a in self.commentAttachments:
            if a.name == file_name:
                return a
        return None

    def __str__(self):
        return '<Discussion id:%r title:%r>' % (self.id, self.title)

    def __repr__(self):
        return str(self)



class Attachment(ContainedThing, object):
    '''
    Information about an attachment.
    '''
    field_names = '''attachmentType attachmentSubType createdAt createdBy
                    id mimeType name sizeInKb parentType parentId'''.split()

    def __init__(self, fields, source, sheet):
        self.fields = fields
        self.source = source
        self.parent = source
        self.sheet = sheet
        self._dirty = False

    @property
    def attachmentType(self):
        return self.fields['attachmentType']

    @property
    def attachmentSubType(self):
        return self.fields.dat('attachmentSubType', None)

    @property
    def createdAt(self):
        return self.fields.get('createdAt')

    @property
    def createdBy(self):
        return SimpleUser(self.fields.get('createdBy'))

    @property
    def id(self):
        return self.fields['id']

    @property
    def mimeType(self):
        return self.fields.get('mimeType')

    @property
    def name(self):
        return self.fields['name']

    @property
    def sizeInKb(self):
        return self.fields.get('sizeInKb')

    @property
    def parentType(self):
        return self.fields.get('parentType', '')

    @property
    def parentId(self):
        return self.fields.get('parentId', '')

    @property
    def fetchPath(self):
        return 'sheet/%s/attachment/%s' % (str(self.source.sheetId),
                str(self.id))

    @property
    def replacePath(self):
        return self.source.replacePath()

    @property
    def newVersionPath(self):
        return 'sheet/%s/attachment/%s/versions' % (str(source.sheetId),
                str(self.id))

    @property
    def sourceInfo(self):
        '''
        Human usable information about the source of the attachment.
        '''
        return self.source.infoForHuman

    def getVersionList(self, client=None):
        '''
        Get a list of all versions of the attachment.
        Returns the list of Attachment objects.
        NOTE:  these Attachment objects have additional fields that regular
        Attachment objects don't: 'parentType' and 'parentId'
        '''
        # FIXME: How should we handle an error with this?
        path = 'sheet/%s/attachment/%s/versions' % (str(self.sheet.id),
                str(self.id))
        client = client or self.client
        hdr, body = client.request(path, 'GET')
        if hdr.isOK():
            return [Attachment(a, self.source, self.sheet) for a in body]
        raise Exception("Request error: %s" % str(hdr))
        

    def getDownloadInfo(self, client=None):
        '''
        Fetch the AttachmentDownloadInfo for this Attachment.
        Return the URL used to fetch the attachment.
        '''
        path = 'sheet/%s/attachment/%s' % (str(self.sheet.id), str(self.id))
        client = client or self.client
        hdr, body = client.request(path, 'GET')
        if hdr.isOK():
            return AttachmentDownloadInfo(body, self.sheet)
        else:
            raise Exception("Unable to get download info for attachment" + 
                    str(hdr))

    def download(self, client=None):
        '''
        Download the attachment, into a populated AttachmentDownloadInfo object.
        The attachment contents are available at .data on the returned object.
        '''
        client = client or self.client
        di = self.getDownloadInfo(client)
        di.download(client)
        return di

    def downloadAndStore(self, client=None, base_path=''):
        '''
        Download and store an attachment.
        The attachment contents are also available at .data on the returned
        AttachmentDownloadInfo object.
        '''
        client = client or self.client
        di = self.download(client)
        di.save(base_path)
        return di

    def uploadNewVersion(self, content, client=None, content_type=None):
        '''
        Upload a new version of the attachment.
        The new version has the same file name, and will, by default have
        the same Content-Type, but with the new content.

        Note that uploading an attachment is an "expensive" operation,
        and as such may fail because too many operations have been performed
        within a small time window.  At present, only 300 operations are
        permitted per minute, and uploading an attachment counts as 10
        operations.
        '''
        if self.attachmentType != 'FILE':
            raise Exception("Only can replace 'FILE' type attachments")
        path = 'sheet/%s/attachment/%s/versions' % (
                str(self.sheet.id), str(self.id))
        headers = {'Content-Type': self.mimeType,
                    'Content-Length': str(len(content)),
                    'Content-Disposition': 
                            'attachment; filename="%s"' % (self.name),
                  }
        client = client or self.client
        hdr, body = client.request(path, 'POST', extra_headers=headers,
                body=content)
        if hdr.isOK():
            # The returned body should include the Attachment object for the
            # new version as the 'result' member of the returned body dict.
            return Attachment(body['result'], source=self.source,
                    sheet=self.sheet)
        raise Exception("Failed to upload new version: %r" % str(hdr))
                 
    def __str__(self):
        return '<Attachment id:%r, name:%r, type:%r:%r created:%r' % (
                self.id, self.name, self.attachmentType, self.mimeType,
                self.createdAt)

    def __repr__(self):
        return str(self)



class AttachmentDownloadInfo(ContainedThing, object):
    '''
    Information about downloading an attachment.
    '''
    field_names = '''name url attachmentType mimeType id
                    urlExpiresInMillis'''.split()
    # NOTE: Presently (January, 2015), the API only supports Attachments that
    #       are attached to a Sheet directly or indirectly (Row or
    #       Discussion comment).  The application supports Workspace-level
    #       attachments.  It may be that the AttachmentDownloadInfo object
    #       will need to take an AncillarySourceObject in the future if the
    #       API expands to support other Attachments.

    def __init__(self, fields, sheet):
        self.fields = fields
        self.sheet = sheet
        self.parent = sheet     # Owned by a sheet.
        self._data = None   # The downloaded attachment.
        self._download_response = None

    @property
    def name(self):
        return self.fields['name']

    @property
    def url(self):
        return self.fields['url']

    @property
    def attachmentType(self):
        return self.fields['attachmentType']

    @property
    def mimeType(self):
        return self.fields['mimeType']

    @property
    def id(self):
        return self.fields['id']

    @property
    def urlExpiresInMillis(self):
        return self.fields.get('urlExpiresInMillis')

    @property
    def data(self):
        return self._data
    
    def checkAttachment(self, client=None):
        '''
        Issue a HEAD request on the attachment -- this will let us get the
        etag, which is an MD5 checksum of the attachment's contents (assuming
        the attachment was stored in Amazon S3 using PUT or POST Object
        operations.
        Sadly, the Signature in the URL this doesn't work
        '''
        path = 'sheet/%s/attachment/%s' % (str(self.sheet.id), str(self.id))
        client = client or self.client
        resp, body = client.raw_request(self.url, '', 'HEAD')
        self.logger.debug("HTTP HEAD request for attachment, resp: %r", resp)
        self.logger.debug("HTTP HEAD request for attachment, body: %r", body)

    def download(self, client=None):
        '''
        Download the attachment, and store it in self._data
        '''
        path = 'sheet/%s/attachment/%s' % (str(self.sheet.id), str(self.id))
        client = client or self.client
        resp, self._data = client.raw_request(self.url, '', 'GET')
        self._download_resp = resp
        resp = HttpResponse(resp)
        if resp.isOK():
            return True
        raise Exception("Attachment download failed: %r: %s" % (self.id, resp))

    def save(self, base_path=''):
        '''
        Write the download attachment to disk.
        '''
        path = os.path.join(base_path, self.name)
        with file(path, 'w') as fh:
            fh.write(self.data)
        return True

    def getEtag(self):
        '''
        After the attachment has been downloaded, we can get the etag, which
        contains the MD5 hash (as of December 2014).
        Returns the etag , or ''.
        '''
        if self._download_response:
            return self._download_response.get('etag', '')
        return ''

    def __str__(self):
        return ('<AttachmentDownloadInfo id:%r, name:%r, url:%r, has_data:%r>' %
                (self.id, self.name, self.url, (not self._data is None)))

    def __repr__(self):
        return str(self)



class AncillaryObjectSource(ContainedThing, object):
    '''
    Specify the source of an ancillary object (attachment, discussion, etc.).
    '''
    @property
    def sheetId(self):
        raise NotImplementedError("AncillaryObjectSource specialization error")

    @property
    def infoForHuman(self):
        raise NotImplementedError("AncillaryObjectSource specialization error")

    def __str__(self):
        return '<%s %s>' % (self.__class__.__name__, self.infoForHuman)

    def __repr__(self):
        return str(self)



class AncillaryObjectSourceSheet(AncillaryObjectSource):
    '''
    Source information for Sheet-level ancillary objects.
    '''
    def __init__(self, sheet):
        self.sheet = sheet
        self.parent = sheet     # This belongs to a sheet.

    @property
    def sheetId(self):
        return self.sheet.id

    @property
    def infoForHuman(self):
        return "Sheet '%s'" % self.sheet.name
    


class AncillaryObjectSourceRow(AncillaryObjectSource):
    '''
    Source information for Row-level ancillary objects.
    '''
    def __init__(self, sheet, row):
        self.sheet = sheet
        self.row = row
        self.parent = row       # This belongs to a row.

    @property
    def sheetId(self):
        return self.sheet.id

    @property
    def infoForHuman(self):
        return "Sheet '%s', Row # %d" % (self.sheet.name, self.row.rowNumber)



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
            format=False, filters=False, rowIds=None, columnIds=None,
            pageSize=None, page=None):

        '''
        Load the Sheet this SheetInfo object is about.
        The optional parameters are the same as those for
        SmartsheetClient.fetchSheetById().
        Returns the corresponding Sheet.
        '''
        return self.client.fetchSheetById(self.id, format=format,
                filters=filters, rowIds=rowIds, columnIds=columnIds,
                pageSize=pageSize, page=page)

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

class UserProfile(object):
    '''
    Information about a Smartsheet user.
    https://www.smartsheet.com/developers/api-documentation#h.40wgk8q3a4ex
    Handles the fields 'licensedSheetCreator' and 'status', even though
    these are not always available for all UserProfile objects (they are
    empty strings when not initialized).
    '''
    field_list = '''id email firstName lastName timeZone locale
                    licensedSheetCreator status'''.split()

    def __init__(self, fields):
        self.fields = fields
        self._dirty = False

    @property
    def id(self):
        return self.fields['id']

    @property
    def email(self):
        return self.fields['email']

    @property
    def firstName(self):
        return self.fields.get('firstName', '')

    @property
    def lastName(self):
        return self.fields.get('lastName', '')

    @property
    def timeZone(self):
        return self.fields.get('timeZone', '')

    @property
    def locale(self):
        return self.fields.get('locale', '')

    @property
    def licensedSheetCreator(self):
        return self.fields.get('licensedSheetCreator', '')

    @property
    def status(self):
        return self.fields.get('status', '')

    def __str__(self):
        return '<UserProfile: id:%r, email:%r, firstName:%r, lastName:%r>' % (
                self.id, self.email, self.firstName, self.lastName)

    def __repr__(self):
        return str(self)



class SimpleUser(object):
    '''
    Some objects (Discussions and Attachments) use this type of user.
    It's a simplified identifier of a user.
    '''
    field_names = 'email name'.split()

    def __init__(self, fields):
        self.fields = fields

    @property
    def email(self):
        return self.fields['email']

    @property
    def name(self):
        return self.fields.get('name', '')

    def __str__(self):
        return '<SimpleUser email:%r, name:%r>' % (self.email, self.name)

    def __repr__(self):
        return str(self)



class HttpResponse(object):
    '''
    A response from an HTTP request.
    The response contains a header and content object.  The content may be
    empty (None).
    '''
    status_codes = {
        '200': 'OK',
        '400': 'BAD REQUEST',
        '401': 'NOT AUTHORIZED',
        '403': 'FORBIDDEN',
        '404': 'NOT FOUND',
        '405': 'METHOD NOT SUPPORTED',
        '500': 'INTERNAL SERVER ERROR',
        '503': 'SERVICE UNAVAILABLE'
    }
    unknown_status_code = '999'
    unknown_status_message = 'UNKNOWN STATUS CODE'

    def __init__(self, hdr, content=''):
        self.hdr = hdr
        self.content = content or ''

    @property
    def status(self):
        return self.hdr.get('status', self.unknown_status_code)

    @property
    def statusMessage(self):
        return self.status_codes.get(self.status, self.unknown_status_message)

    def isOK(self):
        return self.status == '200'

    def contentAsJSON(self):
        '''
        Assume the content is JSON and return whatever it loads as.
        Raises an exception if the content is not well-formed JSON.
        '''
        return json.loads(self.content)

    def __str__(self):
        return '<HttpResponse status:%s content.len: %d>' % (
                self.status, len(sel.content))

    def __repr__(self):
        return str(self)



class SmartsheetAPIResponseHeader(HttpResponse):
    '''
    Response header from a Smartsheet API request.
    '''
    # If a request results in one of these errors, it might not have the same
    # behavior on a future request.
    transient_errors = dict([(error_code, True) for error_code in
        '''1050 1092 1093 1106 2001 2002 2004 4001 4002 4003'''.split()])

    def __init__(self, hdr, content, client):
        super(SmartsheetAPIResponseHeader, self).__init__(hdr, content)
        self.error_code = None
        self.error_message = None

        if not self.isOK():
            try:
                json_content = self.contentAsJSON()
            except Exception, e:
                if client:
                    client.log.warn("Non-OK header: %r", self.hdr)
                json_content = {}
            self.setError(SmartsheetAPIErrorMessage(json_content))

    def rateLimitExceeded(self):
        '''The rate limit was exceeded.'''
        return (self.status == '503' and self.error_code == '4003')

    def serverTimeout(self):
        '''
        The request timed out.  Retrying it could be useful.
        '''
        return (self.status == '500' and self.error_code == '4002')

    def setError(self, error):
        self.error_code = error.code
        self.error_message = error.message

    def isTransientError(self):
        '''
        Return true if the header indicates a transient error.
        A transient error is one that may not be present in a future request
        of the same path.
        '''
        return (self.error_code in self.transient_errors)

    def __str__(self):
        if self.isOK():
            return '<SmartsheetAPIResponseHeader %r>' % self.hdr
        else:
            return ('<SmartsheetAPIResponseHeader %r error_code:%r, error_message:%r fields:%r>' % (
                        self.status, self.error_code, self.error_message,
                        self.hdr))

    def __repr__(self):
        return str(self)


class SmartsheetAPIErrorMessage(object):
    '''
    Wrap the error message for all non-2xx status code responses from the API.
    '''
    missing_error_code = '9999'
    missing_error_message = 'No Error Message specified.'

    def __init__(self, resp_dict):
        self.code = resp_dict.get('errorCode', self.missing_error_code)
        self.message = resp_dict.get('message', self.missing_error_message)



def string_trim(value, max_len):
    '''
    Return a version of value that fits within max_len characters.
    '''
    if len(str(value)) > max_len:
        return str(value)[:max_len-3] + '...'
    else:
        return value


def maybeAssignFromDict(src_dict, dst_obj, src_name, dst_name=None):
    '''
    If the specified src_name is in the src_dict, assign it in dst_obj.
    If dst_name is given, use that as the attribute name rather than src_name.
    '''
    if src_name in src_dict:
        attr_name = dst_name or src_name
        setattr(dst_obj, attr_name, src_dict[src_name])
    return



class SmartsheetErrorCodes_API_v_1_1(object):
    '''
    Error codes for API version 1.1.
    Taken from: https://www.smartsheet.com/developers/api-documentation
    '''
    # FIXME:  This currently unused.  Does it serve any practical purpose?

    raw_error_code_lines = ('''
1001
An Access Token is required.

1002
Your Access Token is invalid.

1003
Your Access Token has expired.

1004
You are not authorized to perform this action.

1005
Single Sign-On is required for this account.

1006
Not Found.

1007
Version not supported.

1008
Unable to parse request. The following error occurred: {0}

1009
A required parameter is missing from your request: {0}.

1010
HTTP Method not supported.

1011
A required header was missing or invalid: {0}

1012
A required object attribute is missing from your request: {0}.

1013
The operation you are attempting to perform is not supported by your plan.

1014
There are no licenses available on your account.

1015
The user exists in another account. The user must be removed from that account before they can be added to yours.

1016
The user is already a member of your account.

1017
The user already has a paid account. The user must cancel that account before they can be added to yours.

1018
The value {0} was not valid for the parameter {1}.

1019
Cannot transfer to the user specified. User not found.

1020
User not found.

1021
Cannot transfer to the user specified. They are not a member of your account.

1022
Cannot delete the user specified. They are not a member of your account.

1023
The sheet specified is shared at the Workspace level.

1024
The HTTP request body is required for this Method.

1025
The share already exists.

1026
Transferring ownership is not currently supported.

1027
Share not found.

1028
You cannot edit the share of the owner.

1029
The parameter in the URI does not match the object in the request body.

1030
You are unable to assume the user specified.

1031
The value {0} was not valid for the attribute {1}.

1032
The attribute(s) {0} are not allowed for this operation.

1033
The template was not found.

1034
Invalid Row ID.

1035
Attachments and discussions cannot be POSTed with a row.

1036
The columnId {0} is invalid.

1037
The columnId {0} is included more than once in a single row.

1038
Invalid Cell value. Must be numeric or a string.

1039
Cannot edit a locked column {0}

1040
Cannot edit your own share.

1041
The value for {0} must be less than {1} but was {2}.

1042
The value for cell in column {0}, {1}, did not conform to the strict requirements for type {2}.

1043
The row number you requested is blank and cannot be retrieved.        

1044
Assume-User header is required for your Access Token.        

1045
The resource specified is read-only.

1046
Cells containing formulas, links to other cells, system values, or Gantt values cannot be inserted or updated through the API.

1047
You cannot remove yourself from the account through the API.

1048
The user specified has declined the invitation to join your organization. You cannot modify declined invitations.

1049
You cannot remove admin permissions from yourself through the API.

1050
You cannot edit a locked row.

1051
Attachments of type FILE cannot be created using JSON.

1052
Invalid Accept header. Media type not supported.

1053
Unknown Paper size: {0}.

1054
The new sheet requires either a fromId or columns.

1055
One and only one column must be primary.

1056
Column titles must be unique.

1057
Primary columns must be of type TEXT_NUMBER.

1058
Column type of {1} does not support symbol of type {0}.

1059
Column options are not allowed when a symbol is specified.

1060
Column options are not allowed for column type {0}.

1061
Max count exceeded for field {0}.

1062
Invalid row location.

1063
Invalid parentId: {0}.

1064
Invalid siblingId: {0}.

1065
The column specified cannot be deleted.

1066
You can only share to {0} users at a time.

1067
Invalid client_id

1068
Unsupported grant type.

1069
Invalid Request. The authorization_code has expired.

1070
Invalid Request. Required parameter is missing: {0}.

1071
Invalid Grant. The authorization code or refresh token provided was invalid.

1072
Invalid hash value. The hash provided did not match the expected value.

1073
The redirect_uri did not match the expected value.

1074
You are trying to upload a file of {0}, but the API currently only supports {1}

1075
The Content-Size provided did not match the file uploaded. This may be due to network issues or because the wrong Content-Size was specified.

1076
The user has created sheets and must be added as a licensed user.

1077
Duplicate system column type: {0}.

1078
System column type {0} not supported for {1} {2}.

1079
Column type {0} is not supported for system column type {1}

1080
End Dates on dependency-enabled sheets cannot be created/updated. Please update either the Duration or Start Date column.

1081
You cannot delete another user's discussions, comments, or comment attachments.

1082
You cannot add options to the given column {0} because it is not a PICKLIST.

1083
Auto number formatting cannot be added to a column {0}

1084
The auto number format is invalid.

1085
The column specified is either a calendar, Gantt, or dependency column and the type cannot be changed.

1086
Google was not able to verify your access.

1087
The column specified is used in a conditional formatting rule, so the column cannot be deleted and its type cannot be changed.

1088
Invalid length for concatenated auto number format. Concatenated format is {0}, with a length of {1}. Must be less than or equal to 40.

1089
The type specified is only used with System Columns.

1090
Column.type is required when changing symbol, systemColumnType or options.

1091
Invalid Content-Type: {0}

1092
You cannot delete this row. Either it or one or more of its children are locked.

1093
An error occurred verifying this receipt, please try again later.

1094
You cannot set a password on a new user unless they accept the license.

1095
The Excel file is invalid/corrupt. This may be due to an invalid file extension, an outdated Excel format, or an invalid Content-Length.

1096
This Apple payment receipt has already been applied to a user's payment profile.

1097
A user must be a licensed sheet creator to be a resource viewer.

1098
To delete this column you must first disable Dependencies for this sheet.

1099
To delete this column you must first disable Resource Management for this sheet.

1100
Uploading new versions of a discussion comment attachment is not supported.

1101
Uploading new versions of non-FILE type attachments is not supported.

1102
A user must be a licensed sheet creator to be a group administrator.

1103
A group with the same name already exists.

1104
You must be a group administrator to create a group.

1105
The operation failed because one or more group members were not members of your account: {0}

1106
Group not found

1107
User specified in transferGroupsTo must be a group admin.

1108
transferGroupsTo must be provided because user being deleted owns one or more groups.

1109
Only one of cell.hyperlink or cell.linkInFromCell may be non-null.

1110
cell.value must be null if cell.linkInFromCell is non-null.

1111
Only one of cell.hyperlink.sheetId and cell.hyperlink.reportId may be non-null.

1112
cell.hyperlink.url must be null for sheet or report hyperlinks.

1113
cell.value must be a string when the cell is a hyperlink.

1114
Invalid sheetId or reportId: {0}

1115
Row must contain either cell link updates or row/cell value updates; mixing of both update types in one API call is not supported.

1116
You cannot link a cell to its own sheet.

1117
One of the following cell.hyperlink fields must be non-null: url, sheetId, or reportId.

2000
Invalid username and/or password.

2001
Your account is locked out.

2002
Invalid email address

2003
Your account is currently locked out due to a billing issue. Please contact Smartsheet Finance at finance@smartsheet.com.

2004
Your email address must be confirmed for you to log into Smartsheet. Please click on the link from your welcome mail, or you can confirm your email by resetting your password.

2005
The device id you have provided is longer than the maximum of 45 characters.

2006
The client id you have provided is not valid.

2008
Invalid login ticket.

2009
The given launch parameters are not currently supported by the API.

4000
An unexpected error has occurred. Please contact Smartsheet support at support@smartsheet.com for assistance.

4001
Smartsheet.com is currently offline for system maintenance. Please check back again shortly.

4002
Server timeout exceeded. Request has failed.

4003
Rate limit exceeded.
''')
    error_codes = {}
    for line_pair in raw_error_code_lines.strip().split('\n\n'):
        error_code, error_desc = line_pair.split('\n')
        error_codes[error_code] = error_desc

    unkown_error_code = 'Undocumented error code'
   
    def lookup(self, error_code):
        return self.error_codes.get(error_code, self.unkown_error_code)

