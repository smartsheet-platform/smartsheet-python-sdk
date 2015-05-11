'''
Library for working with Smartsheet's version 1.1 API.

This is HORRIBLY incomplete at the moment.

Author:  Scott Wimer <scott.wimer@smartsheet.com>
'''

import httplib2
import json
import copy
import time
import logging
import collections


from smartsheet_exceptions import (SmartsheetClientError)


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
        path = '/user/' + str(user)
        name = "%s.fetchUserProfile(%s)" % (self, user)
        body = self.GET(path, name=name)
        return UserProfile(body)


    def fetchSheetList(self, use_cache=False):
        '''
        Fetch a list of sheets.
        The list returned may be cached to avoid repeated redundant requests.
        The sheets are returned as SheetInfo objects.
        '''
        path = '/sheets'
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
        path = '/sheet/' + str(sheet_id)
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
            return ('<SmartsheetAPIResponseHeader %r error_code:%r, '
                    'error_message:%r fields:%r>' % (
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


