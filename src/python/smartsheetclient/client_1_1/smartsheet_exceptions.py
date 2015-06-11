'''
Library for working with Smartsheet's version 1.1 API.

This is HORRIBLY incomplete at the moment.

Author:  Scott Wimer <scott.wimer@smartsheet.com>
'''

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

class OperationOnDiscardedObject(SmartsheetClientError):
    '''
    An operation on a discarded object was attempted.
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


