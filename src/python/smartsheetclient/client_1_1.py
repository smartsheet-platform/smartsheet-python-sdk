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
import operator
import datetime
import traceback

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


    def defaultHeaders(self):
        return {'Authorization': 'Bearer %s' % self.token}


    def rawRequest(self, url, path, method='GET', headers=None, body=None):
        '''
        Make a request with no API headers added.
        Returns the response header and body.
        '''
        req_headers = headers or {}
        req_url = join_url_path(url, path)

        if not self.handle:
            self.handle = httplib2.Http()

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
        headers = self.defaultHeaders()
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
            (resp, content) = self.rawRequest(self.base_url, path, method,
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


    def wrappedRequest(self, path, method='GET', extra_headers=None,
            body=None, name=''):
        '''
        Make the specified request, and do standard error handling work.
        @return The response body (typically a string, list, or dict).
        @raises SmartsheetClientError
        @raises other exceptions -- Needs to only raise SmartsheetClientError
        '''
        # FIXME: Should only raise SmartsheetClientError instances.
        # That will involve rewrapping APIRequestError, as well as any of
        # the socket and/or httplib2 exceptions.
        self.logger.debug("Issuing request: %s", str(name))
        try:
            hdr, body = self.request(path, method=method,
                    extra_headers=extra_headers, body=body)
        except Exception, e:
            err = "%s failed: %s" % (str(name), str(e))
            self.logger.exception(err)
            raise
        if not hdr.isOK():
            err = "%s failed: %s" % (str(name), str(hdr))
            self.logger.error(err)
            raise SmartsheetClientError
        self.logger.debug("%s succeeded", str(name))
        return body


    def GET(self, path, extra_headers=None, name=''):
        return self.wrappedRequest(path, method='GET',
                extra_headers=extra_headers, body=None, name=name)


    def POST(self, path, extra_headers=None, body=None, name=''):
        return self.wrappedRequest(path, method='POST',
                extra_headers=extra_headers, body=body, name=name)


    def PUT(self, path, extra_headers=None, body=None, name=''):
        return self.wrappedRequest(path, method='PUT',
                extra_headers=extra_headers, body=body, name=name)


    def DELETE(self, path, extra_headers=None, name=''):
        return self.wrappedRequest(path, method='DELETE',
                extra_headers=extra_headers, body=None, name=name)


    def fetchUserProfile(self, user='me'):
        '''
        Fetch information about a user.
        By default, the user is determined by the token -- the 'me' user.
        '''
        path = 'user/' + user
        name = "%s.fetchUserProfile(%s)" % (self, user)
        body = self.GET(path, name=name)
        return UserProfile(body)


    def fetchSheetList(self, use_cache=False):
        '''
        Fetch a list of sheets.
        The list returned may be cached to avoid repeated redundant requests.
        The sheets are returned as SheetInfo objects.
        '''
        path = 'sheets'
        name = "%s.fetchSheetList()"
        sheet_list = []
        if not (use_cache and len(self._sheet_list_cache) != 0):
            body = self.GET(path, name=name)
            for sheet_info in body:
                sheet_list.append(SheetInfo(sheet_info, self))
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
        if len(matches) == 1:
            return matches[0]
        else:
            return None


    def fetchSheetById(self, sheet_id, discussions=False, attachments=False,
            format=False, filters=False, source=None, rowNumbers=None,
            rowIds=None, columnIds=None, pageSize=None, page=None):
        '''
        Fetch the specified Sheet.

        May optionally fetch a variety of Sheet attributes:
            Discussions, Attachments, Format, Filters
        In order to get Attachments to Discussion Comments, both 'discussions'
        and 'attachments' must be True.

        Optionally, a subset of the Rows and Columns of the Sheet can be
        fetched by specifying the desired values as lists:
            rowNumbers = List of Row numbers (Row numbers start at 1)
            rowIds = List of Row identifiers (typically big numbers)
            columnIds = List of Column identfiers (typically big numbers)

        @param sheetId The ID of the Sheet to fetch
        @param discussions True to fetch Discussions on the Sheet (and its Rows)
        @param attachments True to fetch Attachments on the Sheet (and its Rows)
        @param format 
        @return The specified Sheet
        @raises SmartsheetClientError
        '''
        path = 'sheet/' + str(sheet_id)
        name = (("%s.fetchSheetById(%r, discussions=%r, attachments=%r, " +
                "format=%r, filters=%r, source=%r, rowNumbers=%r, " +
                "rowIds=%r, columnIds=%r, pageSize=%r, page=%r") % 
                (self, sheet_id, discussions, attachments, format, filters,
                    source, rowNumbers, rowIds, columnIds, pageSize, page))
        path_params = []
        include = []
        if discussions: include.append('discussions')
        if attachments: include.append('attachments')
        if format:
            include.append('format')
            self.logger.warn('SDK support for formats is incomplete.')
        if filters:
            include.append('filters')
            self.logger.warn('SDK support for filters is incomplete.') 
        if include:
            path_params.append("include=" + ','.join(include))
        if rowIds:
            path_params.append('rowIds=' + 
                    ','.join([str(r) for r in rowIds]))
        if rowNumbers:
            path_params.append('rowNumbers='+
                    ','.join([str(r) for r in rowNumbers]))
        if columnIds:
            path_params.append('columnIds=' + 
                    ','.join([str(c) for c in columnIds]))
        if pageSize is not None:
            path_params.append('pageSize=%s' % str(pageSize))
        if page is not None:
            path_params.append('page=%s' % str(page))

        if path_params:
            path += '?' + '&'.join(path_params)

        body = self.GET(path, name=name)
        request_parameters = {
                'discussions': discussions, 'attachments': attachments,
                'format': format, 'filters': filters, 'rowIds': rowIds,
                'columnIds': columnIds, 'pageSize': pageSize, 'page': page}
        sheet = Sheet.newFromAPI(body, self, request_parameters)
        return sheet


    def fetchSheetByPermalink(self, permalink, use_cache=False,
            discussions=False, attachments=False, format=False,
            filters=False, source=None, rowNumbers=None, rowIds=None,
            columnIds=None, pageSize=None, page=None):
        '''
        Fetch the specified Sheet.
        See `.fetchSheetById()` for an explanation of the optional parameters
        that control how the Sheet is fetched and what additional attributes
        are fetched along with it.

        @param permalink The permalink of the Sheet to fetch.
        @param use_cache True to avoid refetching the SheetList.
        @returns the Sheet with the specified permalink
        '''
        si = self.fetchSheetInfoByPermalink(permalink, use_cache=use_cache)
        return self.fetchSheetById(si.id, discussions=discussions,
                attachments=attachments, format=format, filters=filters,
                source=source, rowNumbers=rowNumbers, rowIds=rowIds,
                columnIds=columnIds, pageSize=pageSize, page=page)


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
        if self.client is not None and self.client.logger is not None:
            return self.client.logger
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

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
            self.column_id_map = {}
            self.column_index_map = {}

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
            for column in columns:
                self.column_id_map[column.id] = column
                self.column_index_map[column.index] = column
            return self

        @property
        def columns(self):
            if self._columns is None:
                self._columns = sorted(self.column_id_map.values(),
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
            raise IndexError

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
        self._attachments = []
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
        self.fields = fields
        maybeAssignFromDict(fields, self, 'id')
        maybeAssignFromDict(fields, self, 'name')
        maybeAssignFromDict(fields, self, 'version')
        self.columnsInfo = self.ColumnsInfo.newFromDict(self, fields)

        for row_fields in fields.get('rows', []):
            row = Row.newFromAPI(row_fields, self, self.columnsInfo)
            self._addRowToCache(row)

        self._attachments = [Attachment(a, self) for a in
                fields.get('attachments', [])]
        self._discussions = [Discussion(d,self) for d in 
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
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def columns(self):
        return self.columnsInfo.columns

    @property
    def rows(self):
        return sorted(self._row_id_map.values(),
                key=operator.attrgetter('rowNumber'))

    @property
    def accessLevel(self):
        return self._accessLevel

    @property
    def discussions(self):
        return self._discussions

    @property
    def attachments(self):
        return self._attachments

    @property
    def effectiveAttachmentOptions(self):
        return self._effectiveAttachmentOptions

    @property
    def readOnly(self):
        return self._readOnly

    @property
    def createdAt(self):
        return self._createdAt

    @property
    def modifiedAt(self):
        return self._modifiedAt

    @property
    def permalink(self):
        return self._permalink
 
    @property
    def ganttEnabled(self):
        return self._ganttEnabled

    @property
    def dependenciesEnabled(self):
        return self._dependenciesEnabled

    @property
    def favorite(self):
        return self._favorite

    @property
    def showParentRowsForFilters(self):
        return self._showParentRowsForFilters

    @property
    def version(self):
        return self._version

    @property
    def workspace(self):
        # NOTE: This doesn't seem to be a documented Sheet attribute.
        return self._workspace

    @property
    def totalRowCount(self):
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
        self._use_cache = False
        return self

    def forceCache(self):
        '''
        Enable the cache and return the prior cache state.
        @return prior cache state, suitible for passing to restoreCache().
        '''
        prior_cache_state = self._use_cache
        self.enableCache()
        return prior_cache_state

    def forceNoCache(self):
        '''
        Disable the cache and return the prior cache state.
        @return prior cache state, suitable for passing to restoreCache().
        '''
        prior_cache_state = self._use_cache
        self.disableCache()
        return prior_cache_state

    def restoreCache(self, cache_state):
        '''
        Set the cache state to the passed in value (from forceCache())
        '''
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

    def fetchColumnsInfo(self):
        '''
        Fetch the list of Columns' information for this Sheet.
        Raises SmartsheetClientError on error.

        @return A list of Column objects.
        @raises SmartsheetClientError
        '''
        path = '/sheet/%s?pageSize=1&page=1' % str(self.id)
        name = "%s.fetchColumnsInfo()" % str(self)
        body = self.client.GET(path, name=name)

        ci = self.ColumnsInfo.newFromDict(self, body)
        return ci

    def refreshColumnsInfo(self):
        '''
        Refresh the cached Columns information.
        '''
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
        if row_number == 0:
            err = "%s.getRowByRowNumber(%d) 0 is not a valid Row number" % self
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
        path = '/sheet/%s?pageSize=1&page=1' % str(self.id)
        name = "%s.fetchTotalRowCount()" % self
        body = self.client.GET(path, name=name)
        return body['totalRowCount']

    def _addRowToCache(self, row):
        '''
        Add this Row to the Row cache.
        '''
        self._row_number_map[row.rowNumber] = row
        self._row_id_map[row.id] = row
        return self

    def clearRowCache(self):
        '''
        Clear the Row cache.
        '''
        self._row_id_map = {}
        self._row_number_map = {}
        return self

    def __getitem__(self, row_number):
        '''
        Add a list-style interface to fetching a Row.
        The index is the row_number (1-based) and not a classic (0-based) index.
        This forces the use of caching.
        '''


        prior_cache = self.forceCache()
        row = self.getRowByRowNumber(row_number)
        self.restoreCache(prior_cache)
        return row

    def __iter__(self):
        # TODO:  Make sure this still works now that Rows are stored in a dict.
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
        if use_cache:
            acc = [a for a in self._attachments if a.id == attachment_id]
            if acc:
                return acc[0]
            return None
        else:
            # We could either fetch the info for just this Attachment, or
            # for all Attachments.  since we're caching the info, we'll get
            # the info for all of them.
            attachments = self.fetchAllAttachments(client=client)
            self._attachments = attachments

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
        if use_cache:
            return copy.copy(self._attachments)
        else:
            attachments = self.fetchAllAttachments(client=client)
            self._attachments = attachments
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
        return RowWrapper(self, position=position, parentId=parentId,
                siblingId=siblingId)

    def makeRow(self):
        '''
        Create a new Row.

        The Row is given a copy of the current ColumnsInfo for the Sheet,
        but is not "attached" to the Sheet (it isn't found in Sheet.rows).
        In order to attach the Row to the Sheet, it must be passed to
        sheet.addRow() or placed in a RowWrapper and passed to sheet.addRows().
        @returns The new Row
        '''
        return Row(self, self.columnsInfo.copy())

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
        if self._discarded:
            raise OperationOnDiscardedSheetError()
        row_wrapper = RowWrapper(self, position=position, parentId=parentId,
                siblingId=siblingId)
        row_wrapper.addRow(row)
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
        if self._discarded:
            raise OperationOnDiscardedSheetError()
        path = '/sheet/%s/rows' % str(self.id)
        name = "%s.addRows(%s,strict=%r)" % (self, str(row_wrapper), strict)

        body = self.client.POST(path, extra_headers=self.client.json_headers,
                body=json.dumps(row_wrapper.flattenForInsert()))
        self.clearRowCache()
        row_wrapper.discard()
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
        path = '/sheet/%s/row/%s' % (str(self.id), str(row_id))
        name = "%s.deleteRowById(%s)" % (self, str(row_id))
        body = self.client.DELETE(path, name=name)
        self.clearRowCache()
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
        path = '/sheet/%s/columns' % str(self.id)
        name = "%s.insertColumn(%s, %s)" % (self, column, str(index))
        col_fields = column.flattenToCreationFields()
        ins_index = index
        if index < 0:
            tmp_col = self.getColumnByIndex(index)
            ins_index = tmp_col.index + 1
        col_fields['index'] = ins_index
        
        body = self.client.POST(path, extra_headers=self.client.json_headers,
                body=json.dumps[col_fields])

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
        return self.deleteColumnById(column.id)

    def deleteColumnById(self, column_id):
        '''
        Delete the specified Column from the Sheet.
        @param column_id The ID of the Column to delete.
        @returns The Sheet
        @raises SmartsheetClientError
        '''
        path = '/sheet/%s/column/%s' % (str(self.id), str(column_id))
        name = "%s.deleteColumnById(%s)" % str(column_id)
        body = self.DELETE(path, name=name)
        self.logger.debug("%s.deleteColumnById() refreshing columns_info", self)
        self.refreshColumnsInfo()
        return self

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

        TODO: Make this actually occur.
        '''
        self._discarded = True
        self.client = None      # Not very nice, but it'll work for now.
        for row in self.rows:
            row.discard()

    def delete(self):
        '''
        Delete the Sheet.
        Returns True on success, raise SmartsheetClientError otherwise.
        '''
        if self._discarded:
            raise OperationOnDiscardedSheetError()
        path = '/sheet/%s' % str(self.id)
        name = "%s.delete()" % self
        body = self.client.DELETE(path, name=name)
        self.discard()
        return True

    def __str__(self):
        return '<Sheet id:%r, name:%r>' % (self.id, self.name)

    def __repr__(self):
        return str(self)



class RowWrapper(object):
    '''
    Specifies the expansion state and/or position of one or more Rows.
    The Rows are contiguous.
    '''
    # By default, Add rows to the bottom of a Sheet.
    default_position = 'toBottom'
    def __init__(self, sheet, position=None, expanded=True, parentId=None,
            siblingId=None, *rows):
        '''
        If the Rows are to be children of a parent Row, then the position is
        relative to the parent Row (either the first children
        (position=='toTop'), or the last children (position=='toBottom')).
        `parentId` and `siblingId` are mutually exclusive.

        NOTE:  Rows added to a RowWrapper use cached Colum info.
        This reduces, but does not prevent, the risk of the Rows having
        a different set of Column info.  It also improves performance.

        @param sheet The sheet this RowWrapper is for.
        @param position 'toBottom' (default) or 'toTop'
        @param expanded Whether or not the Rows should be expanded.
        @param parentId Put the Rows as children of this Row.id.
        @param siblingId Put the Rows as the next sibling of this Row.id.
        @param rows A list of Rows these position+expansion applies to.
        '''
        # TODO: Should we let the caller pass us a Row for parent or sibling?
        # This might be less annoying for them than passing us a_row.id.

        if position not in ('toBottom', 'toTop', None):
            err = ("position, if specified,  must be 'toBottom' or 'toTop', " +
                    "got %r")  % position
            sheet.logger.error(err)
            raise SmartsheetClientError(err)
        if parentId is not None and siblingId is not None:
            err = "parentId and siblingId are mutually exclusive"
            sheet.logger.error(err)
            raise SmartsheetClientError(err)

        self.sheet = sheet
        self.parentId = None
        self.siblingId = None
        self.position = None
        self.expanded = None
        self.rows = []
        self.rows.extend(rows)

        if parentId is not None:
            if position == 'toTop':
                # This is redundant when specifying a parent Row.
                # TODO: Determine if sending 'toTop' and parentId is an error.
                position = None
            if position == 'toBottom':
                self.position == position
            self.parentId = parentId

        if siblingId is not None:
            if position is not None:
                err = "position not used when specifying a siblingId."
                sheet.logger.error(err)
                raise SmartsheetClientError(err)
            self.siblingId = siblingId

        if parentId is None and siblingId is None and position is not None:
            self.position = position

        if not (self.position or self.parentId or self.siblingId):
            self.position = self.default_position

        # Get the current Columns information.
        self.sheet.logger.debug("%s.__init__() calling refresh columns_info", self)
        self._columns_info = self.sheet.fetchColumnsInfo()

    def makeRow(self):
        '''
        Make an empty Row object that is suitable for use with this RowWrapper.
        '''
        row = Row(self.sheet, self._columns_info)
        return row

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
        elif self.position == 'toBottom':
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

    def __str__(self):
        return "<RowWrapper position: %s rows=%r>" % (self.position, self.rows)



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

    def __init__(self, sheet, columns_info=None):
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
        self._columns_info = columns_info
        self._rowNumber = -1    # Invalid row number
        self._parentRowNumber = 0   # Initially, no parent Row.
        self._cells = []
        self._discussions = []
        self._attachments = []
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
    def newFromAPI(cls, fields, sheet, columns_info=None):
        row = Row(sheet)
        row.fields = fields
        row.sheet = sheet
        row.parent = sheet     # The Row belongs to the Sheet.
        row._columns_info = columns_info

        row.sheet.logger.debug("Row.newFromAPI(# %d)", fields['rowNumber']) 
        row._id = fields['id']
        row._rowNumber = fields['rowNumber']
        row._parentRowNumber = fields.get('parentRowNumber', 0)
        row._cells = [Cell.newFromAPI(c, row) for c in fields.get('cells', [])]

        # When a Row is fetched directly, the caller can choose to get
        # the Columns with the Row.  Use them if they show up.
        # TODO: This needs to be tested.
        # It should be used to replace the columns_info.
        # row._columns = [
                # Column.newFromAPI(c, row) for c in fields.get('columns', [])
        # ]
        # row._column_id_map = dict([(c.id, c) for c in row._columns])

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
        if self._columns_info:
            return self._columns_info.columns
        return self.sheet.columns

    def getColumnById(self, column_id):
        '''Return the Column that has the specified ID.'''
        # Use the local columns info if it exists, otherwise use the Sheet.
        if self._columns_info:
            self.logger.debug("%s.getColumnById() Using Row.local columns_info", self)
            return self._columns_info.getColumnById(column_id)
        self.logger.debug("%s.getColumnById() Using Sheet columns_info", self)
        return self.sheet.getColumnById(column_id)

    def getColumnByIndex(self, idx):
        '''Return the Column that has the specified index.'''
        if self._columns_info:
            self.logger.debug("%s.getColumnByIndex(%r) using Row.local columns_info", self, idx)
            return self._columns_info.getColumnByIndex(idx)
        self.logger.debug("%s.getColumnByIndex(%r) using sheet columns_info", self, idx)
        return self.sheet.getColumnByIndex(idx)

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

    def delete(self):
        '''
        Delete this Row.
        This method executes immediately against the API server (like all
        actions that affect the structure of a Sheet).
        The Row should not be used after deleting it.
        The Rows remaining after the deletion are renumbered accordingly.
        '''
        return self.sheet.deleteRow(self)

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
        if isinstance(idx, slice):
            err = "Slices of Cell indexes are not supported."
            self.logger.error(err)
            raise NotImplementedError(err)
        try:
            column = self.getColumnByIndex(idx)
            return self.getCellByColumnId(column.id)
        except UnknownColumnId:
            raise IndexError
        except IndexError:
            raise
        except Exception, e:
            err = "Error getting Cell %r[%s]: %s" % (self, str(idx), e)
            self.logger.error(err)
            raise IndexError(err)

    def getCellByColumnId(self, column_id):
        '''
        Get the Cell on this row at the specified Column ID.
        Returns the Cell at the Column ID, or an empty Cell in that position.
        Raises InvalidColumnId if column_id is unknown.
        
        @param column_id The ID of the Column
        @param use_cache True to use the Columns cache; False to refetch it
        @return The Cell on the Row at the specified Column
        @raises InvalidColumnId if the specified column_id is unknown
        '''
        for c in self.cells:
            if c.columnId == column_id:
                return c
        self.logger.debug("%s.getCellByColumnId(%r) calling row.getColumnById()", self, column_id)
        column = self.getColumnById(column_id)
        return Cell(self, column, None, type=CellTypes.EmptyCell, isDirty=False)

    def addSaveData(self, rowchange):
        '''
        If this Row has changed, add its change data to the RowChangeSaveData.
        '''
        if not self.isDirty():
            return
        rowchange.addRowChange(self.change)
        return self

    def save(self):
        '''
        Save this Row to the server.

        Any changes (new Cells, format, position, or expansion) on the Row
        are saved to the API server.

        If this Row has been discarded, it will not be saved and None will
        be returned.

        Once saved, this Row is replaced by the Row constructed from the
        data returned by the server.  The caller should not hold a reference
        to it past calling `save()`.

        @param client The optional Client to use (instead the Sheet's).
        @return The Row returned by the server or None.
        '''
        if self._discarded:
            self.logger.error("Attempted to save a discarded Row: %r", self)
            return None

        # client = client or self.client
        # path = '/sheet/%s/row/%s' % (str(self.sheet.id), str(self.id))
        rc = RowChangeSaveData(self)
        self.addSaveData(rc)
        for cell in self.cells:
            cell.addSaveData(rc)
        return self.saveRowChange(rc)

    def saveRowChange(self, row_change):
        '''
        Save a Row that has been changed (as opposed to a newly created Row).

        If this Row has been discarded, it will not be saved and None will
        be returned.

        @param row_change The RowChangeSaveData for the changed Row.
        @return The Sheet
        @raises SmartsheetClientError
        '''
        if self._discarded:
            self.logger.error("Attempted to save a discarded Row: %r", self)
            return None

        path = '/sheet/%s/row/%s' % (str(self.sheet.id), str(self.id))
        name = "%s.saveRowChange(%s)" % (self, str(row_change))
        body = self.client.PUT(path, extra_headers=self.client.json_headers,
                body=row_change.toJSON())
        self.sheet.clearRowCache()
        return self.sheet

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
        Column indexes start at 0; negative indexes work as normal for Python.
        Returns the value of the Cell at the specified column
        '''
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
        cell = self.getCellByIndex(idx)
        cell.assign(value)
        self.markDirty()
        return value

    def __len__(self):
        '''
        Calling len(a_row) will return the # of columns.
        '''
        return len(self.columns)

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
        self._hidden = False
        self._tags = []
        self._format = None
        self._filter = None
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
        acc = {'title': self.title, 'type': self.type }
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
        return acc

    def delete(self, client=None):
        '''
        Delete this Column.
        '''
        self.discard()
        return self.sheet.deleteColumnById(self, self.id, client=client)

    def __str__(self):
        return '<Column id:%d index:%r title:%r type:%r>' % (
                self.id, self.index, self.title, self.type)

    def __repr__(self):
        return str(self)



class CellHyperlink(object):
    def __init__(self, url=None, sheetId=None, reportId=None):
        if 1 != len([x for x in (url, sheetId, reportId) if x is not None]):
            raise SmartsheetClientError("Must specify one of url, sheetId, " +
                    "or reportId")
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



class CellLinkStatus(object):
    OK = 'OK'
    BROKEN = 'BROKEN'
    INACCESSIBLE = 'INACCESSIBLE'
    NOT_SHARED = 'NOT_SHARED'
    BLOCKED = 'BLOCKED'
    CIRCULAR = 'CIRCULAR'
    INVALID = 'INVALID'
    DISABLED = 'DISABLED'



class CellLinkIn(object):

    def __init__(self, sheetId, rowId, columnId, status):
        self.sheetId = sheetId
        self.rowId = rowId
        self.columnId = columnId
        self.status = status
        self.fields = {}

    @classmethod
    def newFromAPI(cls, fields):
        link = CellLinkIn(fields['sheetId'], fields['rowId'],
                fields['columnId'], fields['status'])
        link.fields = fields
        return link

    def flatten(self):
        acc = { 'sheetId': self.sheetId,
                'rowId': self.rowId,
                'columnId': self.columnId }
        return acc

    def toJSON(self):
        return json.dumps(self.flatten())

    def __str__(self):
        return ('<CellLinkIn: sheetId: %r  rowId: %r  columnId: %r status: %r' %
                (self.sheetId, self.rowId, self.columnId, self.status))

    def __repr__(self):
        return str(self)



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
        self.parent = row
        if link:
            self.logger.warn("Got a 'link' attribute for a Cell")

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
        self.columnId = column.id
        self._value = value
        self._displayValue = displayValue
        self.type = type
        self.hyperlink = hyperlink
        self.linkInFromCell = linkInFromCell
        self.linksOutToCells = None # Not settable by library user.
        self.format = format
        self.formula = None        # Not settable by library user.
        self.link = link            # Deprecated, but can be set by API server.
        self.modifiedAt = None      # Not settable by library user.
        self.modifiedBy = None      # Not settable by library user.
        self._dirty = isDirty
        self.change = None
        self.fields = {}            # Only set by newFromAPI()
        self.isDeleted = False

        if immediate:
            # FIXME: Save this Cell right now.
            raise NotImplementedError("immediate save of Cell not implemented")

    @classmethod
    def newFromAPI(cls, fields, row):
        '''
        Create a new instance from the dict of values from the API.
        '''
        row.logger.debug("Cell.newFromAPI(row:%s) calling row.getColumnById(%r", row, fields['columnId'])
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
                link=fields.get('link', None), isDirty=False,
                immediate=False)
        # Not all attributes are setable with __init__().
        cell.fields = fields
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
        self.hyperlink = hyperlink
        self.linkInFromCell = linkInFromCell
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
        self.logger.debug("%s.column calling self.row.getColumnById()", repr(self))
        return self.row.getColumnById(self.columnId)

    def addSaveData(self, rowchange):
        '''
        If this Cell has changed, add its change data to the RowChangeSaveData.
        '''
        if not self.isDirty():
            return
        rowchange.addCellChange(self.change)
        return self

    def save(self, propagate=True):
        '''
        Save the Cell if it has been changed.
        Successfully saving any Cell on a Row results in the full
        replacement of the Row the Cell was on.  If you are saving each
        Cell as you change it, (either by directly calling save or with the
        `immediate` flag in `assign`), that most likely won't result in
        unexpected behavior.  If, on the other hand, you are "batching up"
        Cell changes, the changes will be lost if this Cell is saved without
        `propagate` set to True.

        @param propagate (optional) False to not save any other changes on Row.
        @return The newly updated Row, or raises SmartsheetClientError.
        '''
        # FIXME:  Clean up this method.
        #path = ('/sheet/%s/row/%s' % (str(self.row.sheet.id), str(self.rowId)))
        rc = RowChangeSaveData(self.row)
        if propagate:       # Get all changes on this Row.
            self.row.save()
        else:               # Only worry about this Cell.
            self.addSaveData(rc)
        return self.row.saveRowChange(rc)

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
        
    def fetchHistory(self):
        '''
        Fetch the history of the Cell.
        '''
        # TODO: Consider making Cell.__getitem__ operate over Cell history.
        # That would let a Sheet be treated as a cube rows x columns x history
        # That operational model might give rise to some interesting uses.
        path = '/sheet/%s/row/%s/column/%s/history' % (
                str(self.row.sheet.id), str(self.rowId), str(self.columnId))
        name = "%r.fetchHistory()" % self
        body = self.client.GET(path, name=name)
        return [Cell.newFromAPI(c, self.row) for c in body]

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
            self._attachments = [Attachment(a, self.sheet) for a 
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

    def __init__(self, fields, sheet):
        self.fields = fields
        self.parent = sheet
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
        return 'sheet/%s/attachment/%s' % (str(self.sheet.id), str(self.id))

    @property
    def replacePath(self):
        raise NotImplementedError("Attachment.replacePath() not implemented")

    @property
    def newVersionPath(self):
        return 'sheet/%s/attachment/%s/versions' % (str(self.sheet.id),
                str(self.id))

    @property
    def sourceInfo(self):
        '''
        Human usable information about the source of the attachment.
        '''
        raise NotImplementedError("Attachment.sourceInfo not implemented.")

    def getVersionList(self):
        '''
        Get a list of all versions of the attachment.
        Returns the list of Attachment objects.
        NOTE:  these Attachment objects have additional fields that regular
        Attachment objects don't: 'parentType' and 'parentId'
        '''
        path = 'sheet/%s/attachment/%s/versions' % (str(self.sheet.id),
                str(self.id))
        name = "%s.getVersionList()" % self
        body = self.client.GET(path, name=name)
        return [Attachment(a, self.sheet) for a in body]

    def getDownloadInfo(self):
        '''
        Fetch the AttachmentDownloadInfo for this Attachment.
        Return the URL used to fetch the attachment.
        '''
        path = 'sheet/%s/attachment/%s' % (str(self.sheet.id), str(self.id))
        name = "%s.getDownloadInfo()" % self
        body = self.client.GET(path, name=name)
        return AttachmentDownloadInfo(body, self.sheet)

    def download(self):
        '''
        Download the attachment, into a populated AttachmentDownloadInfo object.
        The attachment contents are available at .data on the returned object.
        '''
        di = self.getDownloadInfo()
        di.download()
        return di

    def downloadAndStore(self, base_path=''):
        '''
        Download and store an attachment.
        The attachment contents are also available at .data on the returned
        AttachmentDownloadInfo object.
        '''
        di = self.download()
        di.save(base_path)
        return di

    def uploadNewVersion(self, content, content_type=None):
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
            err = ("Attachment.uploadNewVersion() Can only replace 'FILE' " +
                    "Attachment types")
            self.logger.error(err)
            raise SmartsheetClientError(err)
        path = 'sheet/%s/attachment/%s/versions' % (
                str(self.sheet.id), str(self.id))
        headers = {'Content-Type': self.mimeType,
                    'Content-Length': str(len(content)),
                    'Content-Disposition': 
                            'attachment; filename="%s"' % (self.name),
                  }
        name = "%s.uploadNewVersion()" % self
        body = self.client.POST(path, extra_headers=headers, body=content,
                name=name)
        return Attachment(body['result'], sheet=self.sheet)
                 
    def __str__(self):
        return '<Attachment id:%r, name:%r, type:%r:%r created:%r>' % (
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
        resp, body = client.rawRequest(self.url, '', 'HEAD')
        self.logger.debug("HTTP HEAD request for attachment, resp: %r", resp)
        self.logger.debug("HTTP HEAD request for attachment, body: %r", body)

    def download(self, client=None):
        '''
        Download the attachment, and store it in self._data
        '''
        path = 'sheet/%s/attachment/%s' % (str(self.sheet.id), str(self.id))
        client = client or self.client
        resp, self._data = client.rawRequest(self.url, '', 'GET')
        self._download_resp = resp
        resp = HttpResponse(resp)
        if resp.isOK():
            return True
        err = ("AttachmentDownloadInfo.download(%s) failed: %s" %
                (self, resp.hdr))
        self.logger.error(err)
        raise SmartsheetClientError(err)

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
    The attribute name is the ('_' + src_name) unless dst_name is given.
    '''
    if src_name in src_dict:
        attr_name = dst_name or '_' + src_name
        setattr(dst_obj, attr_name, src_dict[src_name])
    return


