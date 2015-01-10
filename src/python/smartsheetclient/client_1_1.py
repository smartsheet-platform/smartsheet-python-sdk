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

# Things that I know need to be fixed.
# TODO:  Create exception classes and use them to pass errors to the caller.
# TODO:  Log when deprecated things (attributes and paths) are used.
# TODO:  Add OAuth support.


class SmartsheetClient(object):
    '''
    Simple client for interacting with Smartsheet sheets using the API v1.1.
    '''
    base_url = 'https://api.smartsheet.com/1.1/'
    version = '1.1'

    def __init__(self, token=None, rate_limit_sleep=10, logger=None):
        self.token = token
        self.rate_limit_sleep = rate_limit_sleep
        self._sheet_list_cache = []
        self.logger = logger or logging.getLogger('SmartsheetClient')
        self.user = None
        self.handle = None
        self.request_count = 0
        self.request_error_count = 0


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
        if path.startswith('/'):
            path = path[1:]

        if path:
            if url.endswith('/'):
                req_url = url + path
            else:
                req_url = url + '/' + path
        else:
            req_url = url

        if not self.handle:
            raise Exception("Must call .connect() before any other calls.")

        self.logger.debug('req_url: %r', req_url)
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
        '''
        headers = self.default_headers()
        if extra_headers:
            headers.update(extra_headers)

        request_try_count = 0
        request_start_time = time.time()

        while True:
            self.request_count += 1
            request_try_count += 1
            request_try_start_time = time.time()
            (resp, content) = self.raw_request(self.base_url, path, method,
                    headers=headers, body=body)
            request_try_end_time = time.time()
            request_try_duration = request_try_end_time - request_try_start_time
            hdr = SmartsheetAPIResponseHeader(resp, content, self)
            body = {}

            if hdr.isOK():
                if content:
                    body = json.loads(content)
                else:
                    self.logger.warn('Request succeeded, with no response body')
                break
            self.request_error_count += 1
            if hdr.rateLimitExceeded():
                self.logger.warn('Hit the rate limit, sleeping for %d',
                        self.rate_limit_sleep)
                time.sleep(self.rate_limit_sleep)
            else:
                self.logger.error("Request error: %r", hdr)
                raise Exception("Request error: %r" % hdr)
        request_end_time = time.time()
        request_duration = request_end_time - request_start_time
        self.logger.info("Request for %r took: %d tries and %f seconds",
                path, request_try_count, request_duration)
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
        raise Exception("Bad request: " + str(hdr))


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
            if hdr.isOK():
                for sheet_info in body:
                    sheet_list.append(SheetInfo(sheet_info, self))
                if use_cache:
                    self._sheet_list_cache = copy.copy(sheet_list)
            else:
                raise Exception("Bad request: " + str(hdr))
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
            raise Exception("Multiple sheets had the same permalink: %r" %
                    [str(si) for si in matches])
        return matches[0]


    def fetchSheetByPermalink(self, permalink, use_cache=False,
            discussions=False, attachments=False, format=False,
            filters=False, row_ids=None, column_ids=None, page_size=None,
            page=None):
        '''
        Fetch the specified sheet.
        May optionally fetch a variety of attributes:
            discussions, attachments, format, filters, rowIds, and columnIds
        NOTE:  Does not support pagination at the moment.
        '''
        si = self.fetchSheetInfoByPermalink(permalink, use_cache=use_cache)
        return self.fetchSheetByID(si.id, discussions=discussions,
                attachments=attachments, format=format, filters=filters,
                row_ids=row_ids, column_ids=column_ids, page_size=page_size,
                page=page)


    def fetchSheetByID(self, sheet_id, discussions=False, attachments=False,
            format=False, filters=False, row_ids=None, column_ids=None,
            page_size=None, page=None):
        '''
        Fetch the specified sheet.
        May optionally fetch a variety of attributes:
            discussions, attachments, format, filters, rowIds, and columnIds
        NOTE:  Does not support pagination at the moment.
        '''
        path = 'sheet/' + str(sheet_id)
        path_params = []

        include = []
        if discussions: include.append('discussions')
        if attachments: include.append('attachments')
        if format: include.append('format')
        if filters: include.append('filters')
        path_params.append("include=" + ','.join(include))

        if row_ids:
            path_params.append('rowIds=' + 
                    ','.join([str(r) for r in row_ids]))
        if column_ids:
            path_params.append('columnIds=' + 
                    ','.join([str(c) for c in column_ids]))

        if path_params:
            path += '?' + ','.join(path_params)

        hdr, body = self.request(path, 'GET')
        if hdr.isOK():
            sheet = Sheet(body, self)
            return sheet
        else:
            raise Exception("Unable to fetch sheet by ID" + str(hdr))


    def __str__(self):
        return '<SmartsheetClient user:%r>' % self.user


    def __repr__(self):
        return str(self)



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

    def __init__(self, fields, client):
        self.fields = fields
        self.client = client
        self._columns = None
        self._rows = None
        self._attachments = None
        self._discussions = None

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
                    Column(c, self) for c in 
                        self.fields.get('columns', [])]
        return self._columns

    @property
    def rows(self):
        if self._rows is None:
            self._rows =  [Row(r, self) for r in self.fields.get('rows', [])]
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

    def refresh(self, client):
        '''
        Refetch the Sheet - using the original fetch options.
        Returns a new instance of the Sheet.
        It unfortunately does not do an in-place refresh.
        '''
        # This means the sheet needs to preserve the original options.
        # Maybe fetching a sheet should be a classmethod that the client
        # calls?
        pass

    def __str__(self):
        return '<Sheet id:%r, name:%r>' % (self.id, self.name)

    def __repr__(self):
        return str(self)



class Row(ContainedThing, object):
    '''
    A row from a sheet.
    '''
    field_names = '''id sheetId rowNumber parentRowNumber cells
                    discussions attachments columns expanded createdAt
                    modifiedAt accessLevel version format filteredOut'''.split()

    def __init__(self, fields, sheet):
        # Does a Row always know its sheet?
        # I think that in the updated API, that the caller MUST know the
        # Sheet.id at least.
        # FIXME: Figure out how to resolve the sheet awareness issue(s).
        self.fields = fields
        self.sheet = sheet
        self.parent = sheet     # The row belongs to the sheet.
        self._cells = None
        self._discussions = None
        self._attachments = None
        self._columns = None

    @property
    def id(self):
        return self.fields['id']

    @property
    def sheetId(self):
        return self.fields['sheetId']

    @property
    def rowNumber(self):
        return self.fields['rowNumber']

    @property
    def parentRowNumber(self):
        return self.fields.get('parentRowNumber', 0)

    @property
    def cells(self):
        if self._cells is None:
            self._cells = [Cell(c, self) for c in self.fields.get('cells', [])]
        return self._cells

    @property
    def discussions(self):
        if self._discussions is None:
            self._discussions = [Discussion(d,
                AncillaryObjectSourceRow(self.sheet, self), self.sheet) for d
                    in self.fields.get('discussions', []) ]
        return self._discussions

    @property
    def attachments(self):
        if self._attachments is None:
            self._attachments = [
                    Attachment(a, AncillaryObjectSourceRow(self.sheet, self),
                        self.sheet) for a in self.fields.get('attachments', [])]
        return self._attachments

    @property
    def columns(self):
        if self._columns is None:
            self._columns = [
                    Column(c, self.sheet) for c in 
                        self.fields.get('columns', [])]
        return self._columns

    @property
    def expanded(self):
        return self.fields.get('expanded')

    @property
    def createdAt(self):
        return self.fields.get('createdAt')

    @property
    def modifiedAt(self):
        return self.fields.get('modifiedAt')

    @property
    def accessLevel(self):
        return self.fields.get('accessLevel')

    @property
    def version(self):
        return self.fields.get('version')

    @property
    def format(self):
        return self.fields.get('format')

    @property
    def filteredOut(self):
        return self.fields.get('filteredOut')

    def getAttachmentByFileName(self, file_name):
        '''
        Return the named Attachment object, or None if not found.
        '''
        for a in self.attachments:
            if a.name == file_name:
                return a
        return None

    def getColumnByIndex(self, column_index):
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

    def getCellByColumnIndex(self, column_index):
        '''
        Get the Cell at the specified column index.
        Columns indexes start at 0.
        Returns None if there is no Cell at the specified index.
        '''
        # This is a bit tricky because we don't really know where to
        # get the columns data from.  It could be on the Row; it
        # could be on the Sheet -- presumably they will agree if it is
        # found on both.
        column = self.getColumnByIndex(column_index)
        if not column:
            column = self.sheet.getColumnByIndex(column_index)
        if not column:
            raise Exception("Unable to find column @ index: %r" % column_index)
        for c in self.cells:
            if c.columnId == column.id:
                return c
        return None

    def __getitem__(self, column_index):
        '''
        Enable indexing a Row object to fetch the cell in the indicated column.
        This allows a Row to be used like a Python list.
        Colum indexes start at 0.
        NOTE:  Negative indexes are not supported.
        Returns the Cell at the specified column
        '''
        if column_index >= 0:
            return self.getCellByColumnIndex(column_index)
        raise Exception("Invalid column index: %r" % column_index)

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

    def __init__(self, fields, sheet):
        # Does a Column always know its sheet?
        # What if a Row is fetched without knowledge of the Row's sheet?
        # TODO:  Deal with the ambiguity surrounding Sheet awareness.
        self.fields = fields
        self.sheet = sheet
        self.parent = sheet     # The column belongs to a sheet

    @property
    def id(self):
        return self.fields['id']

    @property
    def index(self):
        return self.fields['index']

    @property
    def title(self):
        return self.fields.get('title', '')

    @property
    def primary(self):
        return self.fields.get('primary', False)

    @property
    def type(self):
        return self.fields.get('type', '')  # Should this use TEXT_NUMBER

    @property
    def options(self):
        return self.fields.get('options', [])

    @property
    def hidden(self):
        return self.fields.get('hidden', False)

    @property
    def symbol(self):
        return self.fields.get('symbol', '')

    @property
    def systemColumnType(self):
        return self.fields.get('systemColumnType', '')

    @property
    def autoNumberFormat(self):
        return self.fields.get('autoNumberFormat')

    @property
    def tags(self):
        return self.fields.get('tags', [])

    @property
    def width(self):
        return self.fields.get('width')

    @property
    def format(self):
        return self.fields.get('format')

    @property
    def filter(self):
        return self.fields.get('filter')

    def __str__(self):
        return '<Column id:%d index:%r type:%r>' % (
                self.id, self.index, self.type)

    def __repr__(self):
        return str(self)



class Cell(ContainedThing, object):
    '''
    A Cell in a Row of a Sheet.
    Cells don't have a unique ID exposed via the API.  Instead, each Cell is
    uniquely identified by the tuple of Row ID and Column ID.

    A Cell can be either fully (the 
    '''
    field_names = '''type value displayValue columnId link hyperlink
                    linkInFromCell linksOutToCells formula format'''.split()
    max_display_len = 10

    def __init__(self, fields, row):
        self.fields = fields
        self.row = row
        self.parent = row       # The cell belongs to a row.

    @property
    def type(self):
        return self.fields.get('type', '')  # What should the default be?

    @property
    def value(self):
        return self.fields.get('value', '')

    @property
    def displayValue(self):
        return self.fields.get('displayValue', '')

    @property
    def columnId(self):
        return self.fields['columnId']

    @property
    def link(self):
        return self.fields.get('link', '')  # Deprecated

    @property
    def hyperlink(self):
        return self.fields.get('hyperlink')

    @property
    def linkInFromCell(self):
        return self.fields.get('linkInFromCell')

    @property
    def linksOutToCells(self):
        return self.fields.get('linksOutToCells', [])

    @property
    def formula(self):
        return self.fields.get('formula')

    @property
    def format(self):
        return self.fields.get('format')

    @property
    def rowId(self):
        return self.row.id

    def __str__(self):
        return '<Cell rowId:%r, columnId:%r, type:%r value=%r>' % (
                self.rowId, self.columnId, self.type,
                string_trim(self.displayValue, self.max_display_len))

    def __repr__(self):
        return str(self)



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
        Sadly, the Signature in the URL 
        '''
        path = 'sheet/%s/attachment/%s' % (str(self.sheet.id), str(self.id))
        client = client or self.client
        resp, body = client.raw_request(self.url, '', 'HEAD')
        self.logger.debug("HTTP HEAD request for attachment, resp: %r", resp)
        self.logger.debug("HTTP HEAD request for attachment, body: %r", body)

    def download(self, client):
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

    def __str__(self):
        return '<SheetInfo id:%r, name: %r, accessLevel: %r, permalink:%r>' % (
                self.id, self.name, self.accessLevel, self.permalink)

    def __repr__(self):
        return str(self)



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
        self.error_code = error.error_code
        self.error_message = error.error_message

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
    if len(value) > max_len:
        return value[:max_len-3] + '...'
    else:
        return value



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

