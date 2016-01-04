# Smartsheet Python SDK.
#
# Copyright 2016 Smartsheet.com, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# pylint: disable=C0302,C0111


class SmartsheetException(Exception):
    """Root for SmartsheetErrors, never raised directly."""

    pass


class ApiError(SmartsheetException):
    """Errors produced by the Smartsheet API."""

    def __init__(self, error, message=None):
        """
        An error produced by the API.

        Args:
            error: An instance of the Error data type.
            message (str): A human-readable message that can be
                displayed to the end user. Is None, if unavailable.
        """
        super(ApiError, self).__init__(error)
        self.error = error
        self.message = message

    def __repr__(self):
        return 'ApiError({})'.format(self.error)


class HttpError(SmartsheetException):
    """Errors produced at the HTTP layer."""

    def __init__(self, status_code, body):
        super(HttpError, self).__init__(status_code, body)
        self.status_code = status_code
        self.body = body

    def __repr__(self):
        return 'HttpError({}, {!r})'.format(self.status_code, self.body)


class InternalServerError(HttpError):
    """Errors due to a problem on Smartsheet."""

    def __init__(self, status_code, message):
        super(InternalServerError, self).__init__(
            status_code, status_code, message)
        self.status_code = status_code
        self.message = message

    def __repr__(self):
        return 'InternalServerError({}, {!r})'.format(
            self.status_code, self.message)


class UnexpectedRequestError(SmartsheetException):
    """Error originating from Requests API."""

    def __init__(self, request, response):
        super(UnexpectedRequestError, self).__init__(request, response)
        self.request = request
        self.response = response

    def __repr__(self):
        return 'UnexpectedRequestError({!r}, {!r})'.format(
            self.request, self.response)


class AccessTokenRequiredError(ApiError):
    """An Access Token is required."""

    def __init__(self, error, message):
        super(AccessTokenRequiredError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'AccessTokenRequiredError({!r})'.format(self.message)


class AccessTokenInvalidError(ApiError):
    """Your Access Token is invalid."""

    def __init__(self, error, message):
        super(AccessTokenInvalidError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'AccessTokenInvalidError({!r})'.format(self.message)


class AccessTokenExpiredError(ApiError):
    """Your Access Token has expired."""

    def __init__(self, error, message):
        super(AccessTokenExpiredError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'AccessTokenExpiredError({!r})'.format(self.message)


class UnauthorizedError(ApiError):
    """You are not authorized to perform this action."""

    def __init__(self, error, message):
        super(UnauthorizedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UnauthorizedError({!r})'.format(self.message)


class SSORequiredError(ApiError):
    """Single Sign-On is required for this account."""

    def __init__(self, error, message):
        super(SSORequiredError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'SSORequiredError({!r})'.format(self.message)


class NotFoundError(ApiError):
    """Not Found."""

    def __init__(self, error, message):
        super(NotFoundError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'NotFoundError({!r})'.format(self.message)


class VersionNotSupportedError(ApiError):
    """Version not supported."""

    def __init__(self, error, message):
        super(VersionNotSupportedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'VersionNotSupportedError({!r})'.format(self.message)


class UnparseableRequestError(ApiError):
    """Unable to parse request. The following error occurred: {0}."""

    def __init__(self, error, message):
        super(UnparseableRequestError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UnparseableRequestError({!r})'.format(self.message)


class RequiredParameterMissingError(ApiError):
    """Invalid Request. Required parameter is missing: {0}."""

    def __init__(self, error, message):
        super(RequiredParameterMissingError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'RequiredParameterMissingError({!r})'.format(self.message)


class HttpMethodNotSupportedError(ApiError):
    """HTTP Method not supported."""

    def __init__(self, error, message):
        super(HttpMethodNotSupportedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'HttpMethodNotSupportedError({!r})'.format(self.message)


class RequiredHeaderMissingInvalidError(ApiError):
    """A required header was missing or invalid: {0}."""

    def __init__(self, error, message):
        super(RequiredHeaderMissingInvalidError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'RequiredHeaderMissingInvalidError({!r})'.format(self.message)


class RequiredObjectAttributeMissingError(ApiError):
    """A required object attribute is missing from your request: {0}."""

    def __init__(self, error, message):
        super(RequiredObjectAttributeMissingError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'RequiredObjectAttributeMissingError({!r})'.format(self.message)


class UnsupportedByPlanError(ApiError):
    """The operation you are attempting to perform is not supported by ..."""

    def __init__(self, error, message):
        super(UnsupportedByPlanError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UnsupportedByPlanError({!r})'.format(self.message)


class NoLicensesAvailableError(ApiError):
    """There are no licenses available on your account."""

    def __init__(self, error, message):
        super(NoLicensesAvailableError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'NoLicensesAvailableError({!r})'.format(self.message)


class UserExistsInAnotherAccountError(ApiError):
    """The user exists in another account. The user must be removed ..."""

    def __init__(self, error, message):
        super(UserExistsInAnotherAccountError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UserExistsInAnotherAccountError({!r})'.format(self.message)


class UserAlreadyExistsError(ApiError):
    """The user is already a member of your account."""

    def __init__(self, error, message):
        super(UserAlreadyExistsError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UserAlreadyExistsError({!r})'.format(self.message)


class PaidUserAccountExistsError(ApiError):
    """The user already has a paid account. The user must cancel that ..."""

    def __init__(self, error, message):
        super(PaidUserAccountExistsError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'PaidUserAccountExistsError({!r})'.format(self.message)


class InvalidParameterValueError(ApiError):
    """The value {0} was not valid for the parameter {1}."""

    def __init__(self, error, message):
        super(InvalidParameterValueError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidParameterValueError({!r})'.format(self.message)


class TransferNonexistentUserError(ApiError):
    """Cannot transfer to the user specified. User not found."""

    def __init__(self, error, message):
        super(TransferNonexistentUserError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'TransferNonexistentUserError({!r})'.format(self.message)


class UserNotFoundError(ApiError):
    """User not found."""

    def __init__(self, error, message):
        super(UserNotFoundError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UserNotFoundError({!r})'.format(self.message)


class TransferNonmemberUserError(ApiError):
    """Cannot transfer to the user specified. They are not a member of ..."""

    def __init__(self, error, message):
        super(TransferNonmemberUserError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'TransferNonmemberUserError({!r})'.format(self.message)


class DeleteNonmemberUserError(ApiError):
    """Cannot delete the user specified. They are not a member of your ..."""

    def __init__(self, error, message):
        super(DeleteNonmemberUserError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'DeleteNonmemberUserError({!r})'.format(self.message)


class SheetSharedAtWorkspaceLevelError(ApiError):
    """The sheet specified is shared at the Workspace level."""

    def __init__(self, error, message):
        super(SheetSharedAtWorkspaceLevelError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'SheetSharedAtWorkspaceLevelError({!r})'.format(self.message)


class HttpBodyRequiredError(ApiError):
    """The HTTP request body is required for this Method."""

    def __init__(self, error, message):
        super(HttpBodyRequiredError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'HttpBodyRequiredError({!r})'.format(self.message)


class ShareAlreadyExistsError(ApiError):
    """The share already exists."""

    def __init__(self, error, message):
        super(ShareAlreadyExistsError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ShareAlreadyExistsError({!r})'.format(self.message)


class TransferringOwnershipNotSupportedError(ApiError):
    """Transferring ownership is not currently supported."""

    def __init__(self, error, message):
        super(TransferringOwnershipNotSupportedError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'TransferringOwnershipNotSupportedError({!r})'.format(
            self.message)


class ShareNotFoundError(ApiError):
    """Share not found."""

    def __init__(self, error, message):
        super(ShareNotFoundError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ShareNotFoundError({!r})'.format(self.message)


class EditShareOfOwnerError(ApiError):
    """You cannot edit the share of the owner."""

    def __init__(self, error, message):
        super(EditShareOfOwnerError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'EditShareOfOwnerError({!r})'.format(self.message)


class URIParameterDoesNotMatchBodyError(ApiError):
    """The parameter in the URI does not match the object in the ..."""

    def __init__(self, error, message):
        super(URIParameterDoesNotMatchBodyError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'URIParameterDoesNotMatchBodyError({!r})'.format(self.message)


class UnableToAssumeUserError(ApiError):
    """You are unable to assume the user specified."""

    def __init__(self, error, message):
        super(UnableToAssumeUserError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UnableToAssumeUserError({!r})'.format(self.message)


class InvalidAttributeError(ApiError):
    """The value {0} was not valid for the attribute {1}."""

    def __init__(self, error, message):
        super(InvalidAttributeError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidAttributeError({!r})'.format(self.message)


class AttributeNotAllowedError(ApiError):
    """The attribute(s) {0} are not allowed for this operation."""

    def __init__(self, error, message):
        super(AttributeNotAllowedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'AttributeNotAllowedError({!r})'.format(self.message)


class TemplateNotFoundError(ApiError):
    """The template was not found."""

    def __init__(self, error, message):
        super(TemplateNotFoundError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'TemplateNotFoundError({!r})'.format(self.message)


class InvalidRowIdError(ApiError):
    """Invalid Row ID."""

    def __init__(self, error, message):
        super(InvalidRowIdError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidRowIdError({!r})'.format(self.message)


class RowPostError(ApiError):
    """Attachments and discussions cannot be POSTed with a row."""

    def __init__(self, error, message):
        super(RowPostError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'RowPostError({!r})'.format(self.message)


class InvalidColumnIdError(ApiError):
    """The columnId {0} is invalid."""

    def __init__(self, error, message):
        super(InvalidColumnIdError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidColumnIdError({!r})'.format(self.message)


class DuplicateColumnIdError(ApiError):
    """The columnId {0} is included more than once in a single row."""

    def __init__(self, error, message):
        super(DuplicateColumnIdError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'DuplicateColumnIdError({!r})'.format(self.message)


class InvalidCellValueError(ApiError):
    """Invalid Cell value. Must be numeric or a string."""

    def __init__(self, error, message):
        super(InvalidCellValueError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidCellValueError({!r})'.format(self.message)


class EditLockedColumnError(ApiError):
    """Cannot edit a locked column {0}."""

    def __init__(self, error, message):
        super(EditLockedColumnError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'EditLockedColumnError({!r})'.format(self.message)


class CannotEditOwnShareError(ApiError):
    """Cannot edit your own share."""

    def __init__(self, error, message):
        super(CannotEditOwnShareError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'CannotEditOwnShareError({!r})'.format(self.message)


class InvalidCharacterLengthError(ApiError):
    """The value for {0} must be {1} characters in length or less, but ..."""

    def __init__(self, error, message):
        super(InvalidCharacterLengthError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidCharacterLengthError({!r})'.format(self.message)


class StrictRequirementsFailureError(ApiError):
    """The value for cell in column {0}, {1}, did not conform to the ..."""

    def __init__(self, error, message):
        super(StrictRequirementsFailureError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'StrictRequirementsFailureError({!r})'.format(self.message)


class BlankRowRetrievalError(ApiError):
    """The row number you requested is blank and cannot be retrieved."""

    def __init__(self, error, message):
        super(BlankRowRetrievalError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'BlankRowRetrievalError({!r})'.format(self.message)


class AssumeUserHeaderRequiredError(ApiError):
    """Assume-User header is required for your Access Token."""

    def __init__(self, error, message):
        super(AssumeUserHeaderRequiredError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'AssumeUserHeaderRequiredError({!r})'.format(self.message)


class ReadOnlyResourceError(ApiError):
    """The resource specified is read-only."""

    def __init__(self, error, message):
        super(ReadOnlyResourceError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ReadOnlyResourceError({!r})'.format(self.message)


class NotEditableViaApiError(ApiError):
    """Cells containing formulas, links to other cells, system values, ..."""

    def __init__(self, error, message):
        super(NotEditableViaApiError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'NotEditableViaApiError({!r})'.format(self.message)


class CannotRemoveSelfViaApiError(ApiError):
    """You cannot remove yourself from the account through the API."""

    def __init__(self, error, message):
        super(CannotRemoveSelfViaApiError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'CannotRemoveSelfViaApiError({!r})'.format(self.message)


class ModifyDeclinedInvitationError(ApiError):
    """The user specified has declined the invitation to join your ..."""

    def __init__(self, error, message):
        super(ModifyDeclinedInvitationError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ModifyDeclinedInvitationError({!r})'.format(self.message)


class CannotRemoveAdminForSelfViaApiError(ApiError):
    """You cannot remove admin permissions from yourself through the ..."""

    def __init__(self, error, message):
        super(CannotRemoveAdminForSelfViaApiError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'CannotRemoveAdminForSelfViaApiError({!r})'.format(self.message)


class EditLockedRowError(ApiError):
    """You cannot edit a locked row."""

    def __init__(self, error, message):
        super(EditLockedRowError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'EditLockedRowError({!r})'.format(self.message)


class FileAttachmentUsingJsonError(ApiError):
    """Attachments of type FILE cannot be created using JSON."""

    def __init__(self, error, message):
        super(FileAttachmentUsingJsonError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'FileAttachmentUsingJsonError({!r})'.format(self.message)


class InvalidAcceptHeaderError(ApiError):
    """Invalid Accept header. Media type not supported."""

    def __init__(self, error, message):
        super(InvalidAcceptHeaderError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidAcceptHeaderError({!r})'.format(self.message)


class UnknownPaperSizeError(ApiError):
    """Unknown Paper size: {0}."""

    def __init__(self, error, message):
        super(UnknownPaperSizeError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UnknownPaperSizeError({!r})'.format(self.message)


class NewSheetMissingRequirementsError(ApiError):
    """The new sheet requires either a fromId or columns."""

    def __init__(self, error, message):
        super(NewSheetMissingRequirementsError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'NewSheetMissingRequirementsError({!r})'.format(self.message)


class OnlyOnePrimaryError(ApiError):
    """One and only one column must be primary."""

    def __init__(self, error, message):
        super(OnlyOnePrimaryError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'OnlyOnePrimaryError({!r})'.format(self.message)


class UniqueColumnTitlesError(ApiError):
    """Column titles must be unique."""

    def __init__(self, error, message):
        super(UniqueColumnTitlesError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UniqueColumnTitlesError({!r})'.format(self.message)


class PrimaryColumnTypeError(ApiError):
    """Primary columns must be of type TEXT_NUMBER."""

    def __init__(self, error, message):
        super(PrimaryColumnTypeError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'PrimaryColumnTypeError({!r})'.format(self.message)


class ColumnTypeSymbolTypeUnsupportedError(ApiError):
    """Column type of {1} does not support symbol of type {0}."""

    def __init__(self, error, message):
        super(ColumnTypeSymbolTypeUnsupportedError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ColumnTypeSymbolTypeUnsupportedError({!r})'.format(
            self.message)


class ColumnOptionsNotAllowedWhenSymbolError(ApiError):
    """Column options are not allowed when a symbol is specified."""

    def __init__(self, error, message):
        super(ColumnOptionsNotAllowedWhenSymbolError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ColumnOptionsNotAllowedWhenSymbolError({!r})'.format(
            self.message)


class ColumnOptionsNotAllowedForColumnTypeError(ApiError):
    """Column options are not allowed for column type {0}."""

    def __init__(self, error, message):
        super(ColumnOptionsNotAllowedForColumnTypeError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ColumnOptionsNotAllowedForColumnTypeError({!r})'.format(
            self.message)


class MaxCountExceededError(ApiError):
    """Max count exceeded for field {0}."""

    def __init__(self, error, message):
        super(MaxCountExceededError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'MaxCountExceededError({!r})'.format(self.message)


class InvalidRowLocationError(ApiError):
    """Invalid row location."""

    def __init__(self, error, message):
        super(InvalidRowLocationError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidRowLocationError({!r})'.format(self.message)


class InvalidParentIdError(ApiError):
    """Invalid parentId: {0}."""

    def __init__(self, error, message):
        super(InvalidParentIdError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidParentIdError({!r})'.format(self.message)


class InvalidSiblingIdError(ApiError):
    """Invalid siblingId: {0}."""

    def __init__(self, error, message):
        super(InvalidSiblingIdError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidSiblingIdError({!r})'.format(self.message)


class ColumnCannotBeDeletedError(ApiError):
    """The column specified cannot be deleted."""

    def __init__(self, error, message):
        super(ColumnCannotBeDeletedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ColumnCannotBeDeletedError({!r})'.format(self.message)


class UserShareLimitError(ApiError):
    """You can only share to {0} users at a time."""

    def __init__(self, error, message):
        super(UserShareLimitError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UserShareLimitError({!r})'.format(self.message)


class InvalidClientIdError(ApiError):
    """Invalid client_id."""

    def __init__(self, error, message):
        super(InvalidClientIdError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidClientIdError({!r})'.format(self.message)


class UnsupportedGrantTypeError(ApiError):
    """Unsupported grant type."""

    def __init__(self, error, message):
        super(UnsupportedGrantTypeError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UnsupportedGrantTypeError({!r})'.format(self.message)


class AuthorizationCodeExpiredError(ApiError):
    """Invalid Request. The authorization_code has expired."""

    def __init__(self, error, message):
        super(AuthorizationCodeExpiredError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'AuthorizationCodeExpiredError({!r})'.format(self.message)


class InvalidTokenProvidedError(ApiError):
    """Invalid Grant. The authorization code or refresh token provided ..."""

    def __init__(self, error, message):
        super(InvalidTokenProvidedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidTokenProvidedError({!r})'.format(self.message)


class InvalidHashValueError(ApiError):
    """Invalid hash value. The hash provided did not match the ..."""

    def __init__(self, error, message):
        super(InvalidHashValueError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidHashValueError({!r})'.format(self.message)


class RedirectUrlDidNotMatchError(ApiError):
    """The redirect_uri did not match the expected value."""

    def __init__(self, error, message):
        super(RedirectUrlDidNotMatchError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'RedirectUrlDidNotMatchError({!r})'.format(self.message)


class UploadUnsupportedFileError(ApiError):
    """You are trying to upload a file of {0}, but the API currently ..."""

    def __init__(self, error, message):
        super(UploadUnsupportedFileError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UploadUnsupportedFileError({!r})'.format(self.message)


class ContentSizeDidNotMatchError(ApiError):
    """The Content-Size provided did not match the file uploaded. This ..."""

    def __init__(self, error, message):
        super(ContentSizeDidNotMatchError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ContentSizeDidNotMatchError({!r})'.format(self.message)


class UserMustBeLicensedError(ApiError):
    """The user has created sheets and must be added as a licensed user."""

    def __init__(self, error, message):
        super(UserMustBeLicensedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UserMustBeLicensedError({!r})'.format(self.message)


class DuplicateSystemColumnTypeError(ApiError):
    """Duplicate system column type: {0}."""

    def __init__(self, error, message):
        super(DuplicateSystemColumnTypeError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'DuplicateSystemColumnTypeError({!r})'.format(self.message)


class SystemColumnTypeNotSupportedError(ApiError):
    """System column type {0} not supported for {1} {2}."""

    def __init__(self, error, message):
        super(SystemColumnTypeNotSupportedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'SystemColumnTypeNotSupportedError({!r})'.format(self.message)


class ColumnTypeNotSupportedForSystemTypeError(ApiError):
    """Column type {0} is not supported for system column type {1}."""

    def __init__(self, error, message):
        super(ColumnTypeNotSupportedForSystemTypeError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ColumnTypeNotSupportedForSystemTypeError({!r})'.format(
            self.message)


class DependencyEnabledEndDatesError(ApiError):
    """End Dates on dependency-enabled sheets cannot be ..."""

    def __init__(self, error, message):
        super(DependencyEnabledEndDatesError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'DependencyEnabledEndDatesError({!r})'.format(self.message)


class DeleteAnotherUserDiscussionElementsError(ApiError):
    """You cannot delete another user's discussions, comments, or ..."""

    def __init__(self, error, message):
        super(DeleteAnotherUserDiscussionElementsError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'DeleteAnotherUserDiscussionElementsError({!r})'.format(
            self.message)


class NonPicklistError(ApiError):
    """You cannot add options to the given column {0} because it is ..."""

    def __init__(self, error, message):
        super(NonPicklistError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'NonPicklistError({!r})'.format(self.message)


class AutoNumberFormattingCannotBeAddedError(ApiError):
    """Auto number formatting cannot be added to a column {0}."""

    def __init__(self, error, message):
        super(AutoNumberFormattingCannotBeAddedError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'AutoNumberFormattingCannotBeAddedError({!r})'.format(
            self.message)


class AutoNumberFormatInvalidError(ApiError):
    """The auto number format is invalid."""

    def __init__(self, error, message):
        super(AutoNumberFormatInvalidError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'AutoNumberFormatInvalidError({!r})'.format(self.message)


class ChangeColumnDisableDependenciesFirstError(ApiError):
    """To change this column's type you must first disable ..."""

    def __init__(self, error, message):
        super(ChangeColumnDisableDependenciesFirstError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ChangeColumnDisableDependenciesFirstError({!r})'.format(
            self.message)


class GoogleAccessVerificationError(ApiError):
    """Google was not able to verify your access."""

    def __init__(self, error, message):
        super(GoogleAccessVerificationError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'GoogleAccessVerificationError({!r})'.format(self.message)


class ColumnRequiredByConditionalFormattingError(ApiError):
    """The column specified is used in a conditional formatting rule, ..."""

    def __init__(self, error, message):
        super(ColumnRequiredByConditionalFormattingError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ColumnRequiredByConditionalFormattingError({!r})'.format(
            self.message)


class InvalidLengthAutoNumberFormatError(ApiError):
    """Invalid length for concatenated auto number format. ..."""

    def __init__(self, error, message):
        super(InvalidLengthAutoNumberFormatError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidLengthAutoNumberFormatError({!r})'.format(self.message)


class TypeForSystemColumnsOnlyError(ApiError):
    """The type specified is only used with System Columns."""

    def __init__(self, error, message):
        super(TypeForSystemColumnsOnlyError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'TypeForSystemColumnsOnlyError({!r})'.format(self.message)


class ColumnTypeRequiredError(ApiError):
    """Column.type is required when changing symbol, systemColumnType ..."""

    def __init__(self, error, message):
        super(ColumnTypeRequiredError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ColumnTypeRequiredError({!r})'.format(self.message)


class InvalidContentTypeError(ApiError):
    """Invalid Content-Type: {0}."""

    def __init__(self, error, message):
        super(InvalidContentTypeError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidContentTypeError({!r})'.format(self.message)


class LockedChildrenError(ApiError):
    """You cannot delete this row. Either it or one or more of its ..."""

    def __init__(self, error, message):
        super(LockedChildrenError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'LockedChildrenError({!r})'.format(self.message)


class ExcelFileCorruptError(ApiError):
    """The Excel file is invalid/corrupt. This may be due to an ..."""

    def __init__(self, error, message):
        super(ExcelFileCorruptError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ExcelFileCorruptError({!r})'.format(self.message)


class ApplePaymentReceiptAlreadyAppliedError(ApiError):
    """This Apple payment receipt has already been applied to a user's ..."""

    def __init__(self, error, message):
        super(ApplePaymentReceiptAlreadyAppliedError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ApplePaymentReceiptAlreadyAppliedError({!r})'.format(
            self.message)


class LicensedSheetCreatorRequiredError(ApiError):
    """A user must be a licensed sheet creator to be a resource viewer."""

    def __init__(self, error, message):
        super(LicensedSheetCreatorRequiredError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'LicensedSheetCreatorRequiredError({!r})'.format(self.message)


class DeleteColumnDisableDependenciesFirstError(ApiError):
    """To delete this column you must first disable Dependencies for ..."""

    def __init__(self, error, message):
        super(DeleteColumnDisableDependenciesFirstError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'DeleteColumnDisableDependenciesFirstError({!r})'.format(
            self.message)


class DeleteColumnDisableResourceManagementFirstError(ApiError):
    """To delete this column you must first disable Resource ..."""

    def __init__(self, error, message):
        super(DeleteColumnDisableResourceManagementFirstError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'DeleteColumnDisableResourceManagementFirstError({!r})'.format(
            self.message)


class DiscussionCommentAttachmentVersionsNotSupportedError(ApiError):
    """Uploading new versions of a discussion comment attachment is ..."""

    def __init__(self, error, message):
        super(DiscussionCommentAttachmentVersionsNotSupportedError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        retval = 'DiscussionCommentAttachmentVersionsNotSu'
        retval += 'portedError'
        return retval.format(self.message)


class NewVersionsNonFileNotSupportedError(ApiError):
    """Uploading new versions of non-FILE type attachments is not ..."""

    def __init__(self, error, message):
        super(NewVersionsNonFileNotSupportedError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'NewVersionsNonFileNotSupportedError({!r})'.format(self.message)


class AdminRequiresLicensedSheetCreatorError(ApiError):
    """A user must be a licensed sheet creator to be a group ..."""

    def __init__(self, error, message):
        super(AdminRequiresLicensedSheetCreatorError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'AdminRequiresLicensedSheetCreatorError({!r})'.format(
            self.message)


class GroupNameExistsError(ApiError):
    """A group with the same name already exists."""

    def __init__(self, error, message):
        super(GroupNameExistsError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'GroupNameExistsError({!r})'.format(self.message)


class GroupAdminMustCreateGroupError(ApiError):
    """You must be a group administrator to create a group."""

    def __init__(self, error, message):
        super(GroupAdminMustCreateGroupError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'GroupAdminMustCreateGroupError({!r})'.format(self.message)


class GroupMembersNotMembersOfAccountError(ApiError):
    """The operation failed because one or more group members were not ..."""

    def __init__(self, error, message):
        super(GroupMembersNotMembersOfAccountError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'GroupMembersNotMembersOfAccountError({!r})'.format(
            self.message)


class GroupNotFoundError(ApiError):
    """Group not found."""

    def __init__(self, error, message):
        super(GroupNotFoundError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'GroupNotFoundError({!r})'.format(self.message)


class TransferGroupsToUserMustBeGroupAdminError(ApiError):
    """User specified in transferGroupsTo must be a group admin."""

    def __init__(self, error, message):
        super(TransferGroupsToUserMustBeGroupAdminError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'TransferGroupsToUserMustBeGroupAdminError({!r})'.format(
            self.message)


class TransferGroupsToValueRequiredError(ApiError):
    """transferGroupsTo must be provided because user being deleted ..."""

    def __init__(self, error, message):
        super(TransferGroupsToValueRequiredError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'TransferGroupsToValueRequiredError({!r})'.format(self.message)


class OnlyOneLinkMayBeNonNullError(ApiError):
    """Only one of cell.hyperlink or cell.linkInFromCell may be ..."""

    def __init__(self, error, message):
        super(OnlyOneLinkMayBeNonNullError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'OnlyOneLinkMayBeNonNullError({!r})'.format(self.message)


class CellValueMustBeNullError(ApiError):
    """cell.value must be null if cell.linkInFromCell is non-null."""

    def __init__(self, error, message):
        super(CellValueMustBeNullError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'CellValueMustBeNullError({!r})'.format(self.message)


class OnlyOneNullCellHyperlinkSheetIdReportIdError(ApiError):
    """Only one of cell.hyperlink.sheetId and cell.hyperlink.reportId ..."""

    def __init__(self, error, message):
        super(OnlyOneNullCellHyperlinkSheetIdReportIdError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'OnlyOneNullCellHyperlinkSheetIdReportIdError({!r})'.format(
            self.message)


class CellHyperlinkUrlMustBeNullError(ApiError):
    """cell.hyperlink.url must be null for sheet or report hyperlinks."""

    def __init__(self, error, message):
        super(CellHyperlinkUrlMustBeNullError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'CellHyperlinkUrlMustBeNullError({!r})'.format(self.message)


class CellHyperlinkValueMustBeStringError(ApiError):
    """cell.value must be a string when the cell is a hyperlink."""

    def __init__(self, error, message):
        super(CellHyperlinkValueMustBeStringError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'CellHyperlinkValueMustBeStringError({!r})'.format(self.message)


class InvalidSheetIdOrReportIdError(ApiError):
    """Invalid sheetId or reportId: {0}."""

    def __init__(self, error, message):
        super(InvalidSheetIdOrReportIdError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidSheetIdOrReportIdError({!r})'.format(self.message)


class UpdateTypeMixingNotSupportedError(ApiError):
    """Row must contain either cell link updates or row/cell value ..."""

    def __init__(self, error, message):
        super(UpdateTypeMixingNotSupportedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UpdateTypeMixingNotSupportedError({!r})'.format(self.message)


class CellLinkToSelfSheetError(ApiError):
    """You cannot link a cell to its own sheet."""

    def __init__(self, error, message):
        super(CellLinkToSelfSheetError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'CellLinkToSelfSheetError({!r})'.format(self.message)


class CellHyperlinkNeedsUrlSheetIdOrReportIdError(ApiError):
    """One of the following cell.hyperlink fields must be non-null: ..."""

    def __init__(self, error, message):
        super(CellHyperlinkNeedsUrlSheetIdOrReportIdError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'CellHyperlinkNeedsUrlSheetIdOrReportIdError({!r})'.format(
            self.message)


class GanttAllocationColumnIdError(ApiError):
    """You cannot set the value of a Gantt allocation column (id {0}) ..."""

    def __init__(self, error, message):
        super(GanttAllocationColumnIdError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'GanttAllocationColumnIdError({!r})'.format(self.message)


class CopyFailedError(ApiError):
    """Failed to complete copy. **NOTE**: may include a "detail" ..."""

    def __init__(self, error, message):
        super(CopyFailedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'CopyFailedError({!r})'.format(self.message)


class TooManySheetsToCopyError(ApiError):
    """Too many sheets to copy. **NOTE**: includes a "detail" object ..."""

    def __init__(self, error, message):
        super(TooManySheetsToCopyError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'TooManySheetsToCopyError({!r})'.format(self.message)


class TransferToRequiredError(ApiError):
    """transferTo must be provided because user being deleted owns one ..."""

    def __init__(self, error, message):
        super(TransferToRequiredError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'TransferToRequiredError({!r})'.format(self.message)


class UnsupportedMethodError(ApiError):
    """Requested URL does not support this method: {0}."""

    def __init__(self, error, message):
        super(UnsupportedMethodError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UnsupportedMethodError({!r})'.format(self.message)


class MultipleRowLocationSpecificationError(ApiError):
    """Specifying multiple row locations is not yet supported. Each ..."""

    def __init__(self, error, message):
        super(MultipleRowLocationSpecificationError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'MultipleRowLocationSpecificationError({!r})'.format(
            self.message)


class InvalidContentTypeMediaUnsupportedError(ApiError):
    """Invalid Content-Type header. Media type not supported."""

    def __init__(self, error, message):
        super(InvalidContentTypeMediaUnsupportedError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidContentTypeMediaUnsupportedError({!r})'.format(
            self.message)


class AllPartsRequireNamesMultipartPayloadError(ApiError):
    """Each part in a multipart payload must have a name."""

    def __init__(self, error, message):
        super(AllPartsRequireNamesMultipartPayloadError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'AllPartsRequireNamesMultipartPayloadError({!r})'.format(
            self.message)


class DuplicatePartNamesMultipartPayloadError(ApiError):
    """Multipart payload contained duplicate part names: {0}."""

    def __init__(self, error, message):
        super(DuplicatePartNamesMultipartPayloadError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'DuplicatePartNamesMultipartPayloadError({!r})'.format(
            self.message)


class RequiredMultiPartPartMissingError(ApiError):
    """Required multipart part was missing: '{0}'."""

    def __init__(self, error, message):
        super(RequiredMultiPartPartMissingError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'RequiredMultiPartPartMissingError({!r})'.format(self.message)


class MultipartUploadSizeLimitExceededError(ApiError):
    """Multipart upload size limit exceeded."""

    def __init__(self, error, message):
        super(MultipartUploadSizeLimitExceededError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'MultipartUploadSizeLimitExceededError({!r})'.format(
            self.message)


class ResourceAlreadyExistsError(ApiError):
    """The resource you tried to create already exists."""

    def __init__(self, error, message):
        super(ResourceAlreadyExistsError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ResourceAlreadyExistsError({!r})'.format(self.message)


class CellValueOrObjectValueError(ApiError):
    """One of cell.value or objectValue may be set, but not both."""

    def __init__(self, error, message):
        super(CellValueOrObjectValueError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'CellValueOrObjectValueError({!r})'.format(self.message)


class CellWrongObjectTypeError(ApiError):
    """cell.{0} for column {1} was of the wrong object type. Allowed ..."""

    def __init__(self, error, message):
        super(CellWrongObjectTypeError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'CellWrongObjectTypeError({!r})'.format(self.message)


class TokenRevokedError(ApiError):
    """The token provided has previously been revoked."""

    def __init__(self, error, message):
        super(TokenRevokedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'TokenRevokedError({!r})'.format(self.message)


class ColumnTitlesNotUniqueInInputError(ApiError):
    """Column titles are not unique among input columns."""

    def __init__(self, error, message):
        super(ColumnTitlesNotUniqueInInputError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ColumnTitlesNotUniqueInInputError({!r})'.format(self.message)


class DuplicateSystemColumnTypesInInputError(ApiError):
    """Duplicate system column type among input columns."""

    def __init__(self, error, message):
        super(DuplicateSystemColumnTypesInInputError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'DuplicateSystemColumnTypesInInputError({!r})'.format(
            self.message)


class InputColumnIndexDiffersFromFirstInputColumnIndexError(ApiError):
    """Input column index {0} is different from the first input column ..."""

    def __init__(self, error, message):
        super(InputColumnIndexDiffersFromFirstInputColumnIndexError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        retval = 'InputColumnIndexDiffersFromFirstInputCol'
        retval += 'mnIndexError'
        return retval.format(self.message)


class CopyMoveInSameSheetError(ApiError):
    """Cannot copy or move row(s) within the same sheet."""

    def __init__(self, error, message):
        super(CopyMoveInSameSheetError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'CopyMoveInSameSheetError({!r})'.format(self.message)


class MultipleInstancesSameElementError(ApiError):
    """Input collection contains multiple instances of the same element."""

    def __init__(self, error, message):
        super(MultipleInstancesSameElementError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'MultipleInstancesSameElementError({!r})'.format(self.message)


class UserIneligibleForTrialOrgError(ApiError):
    """The user is not eligible for a trial organization."""

    def __init__(self, error, message):
        super(UserIneligibleForTrialOrgError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UserIneligibleForTrialOrgError({!r})'.format(self.message)


class UserAdminAnotherOrgError(ApiError):
    """The user is an admin in another organization. Add ..."""

    def __init__(self, error, message):
        super(UserAdminAnotherOrgError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UserAdminAnotherOrgError({!r})'.format(self.message)


class UserMustBeAddedAsLicensedError(ApiError):
    """The user must be added as a licensed user."""

    def __init__(self, error, message):
        super(UserMustBeAddedAsLicensedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UserMustBeAddedAsLicensedError({!r})'.format(self.message)


class InvitingEnterpriseUsersError(ApiError):
    """Inviting users from an enterprise organization is not supported."""

    def __init__(self, error, message):
        super(InvitingEnterpriseUsersError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvitingEnterpriseUsersError({!r})'.format(self.message)


class ColumnTypeReservedForProjectSheetsError(ApiError):
    """Column type {0} is reserved for project sheets and may not be ..."""

    def __init__(self, error, message):
        super(ColumnTypeReservedForProjectSheetsError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'ColumnTypeReservedForProjectSheetsError({!r})'.format(
            self.message)


class EnableSheetDependenciesFirstError(ApiError):
    """To set {0}, you must first enable dependencies on the sheet."""

    def __init__(self, error, message):
        super(EnableSheetDependenciesFirstError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'EnableSheetDependenciesFirstError({!r})'.format(self.message)


class UserOwnsOnePlusGroupsError(ApiError):
    """The user owns one or more groups and must be added as a Group ..."""

    def __init__(self, error, message):
        super(UserOwnsOnePlusGroupsError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UserOwnsOnePlusGroupsError({!r})'.format(self.message)


class InvalidMultipartUploadRequestError(ApiError):
    """Multipart upload request was invalid. Please check your request ..."""

    def __init__(self, error, message):
        super(InvalidMultipartUploadRequestError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidMultipartUploadRequestError({!r})'.format(self.message)


class UnsupportedOperationError(ApiError):
    """Unsupported operation: {0}."""

    def __init__(self, error, message):
        super(UnsupportedOperationError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UnsupportedOperationError({!r})'.format(self.message)


class InvalidPartNameMultipartPayloadError(ApiError):
    """Multipart request contained an invalid part name: '{0}'."""

    def __init__(self, error, message):
        super(InvalidPartNameMultipartPayloadError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidPartNameMultipartPayloadError({!r})'.format(
            self.message)


class CellValuesOutOfRangeError(ApiError):
    """Numeric cell values must be between {0} and {1}."""

    def __init__(self, error, message):
        super(CellValuesOutOfRangeError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'CellValuesOutOfRangeError({!r})'.format(self.message)


class InvalidUsernameOrPasswordError(ApiError):
    """Invalid username and/or password."""

    def __init__(self, error, message):
        super(InvalidUsernameOrPasswordError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidUsernameOrPasswordError({!r})'.format(self.message)


class AccountLockedError(ApiError):
    """Your account is locked out."""

    def __init__(self, error, message):
        super(AccountLockedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'AccountLockedError({!r})'.format(self.message)


class InvalidEmailAddressError(ApiError):
    """Invalid email address."""

    def __init__(self, error, message):
        super(InvalidEmailAddressError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidEmailAddressError({!r})'.format(self.message)


class AccountBillingLockError(ApiError):
    """Your account is currently locked out due to a billing issue. ..."""

    def __init__(self, error, message):
        super(AccountBillingLockError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'AccountBillingLockError({!r})'.format(self.message)


class EmailConfirmationRequiredError(ApiError):
    """Your email address must be confirmed for you to log into ..."""

    def __init__(self, error, message):
        super(EmailConfirmationRequiredError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'EmailConfirmationRequiredError({!r})'.format(self.message)


class DeviceIdExceedsMaxLengthError(ApiError):
    """The device id you have provided is longer than the maximum of ..."""

    def __init__(self, error, message):
        super(DeviceIdExceedsMaxLengthError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'DeviceIdExceedsMaxLengthError({!r})'.format(self.message)


class InvalidClientIdProvidedError(ApiError):
    """The client id you have provided is not valid."""

    def __init__(self, error, message):
        super(InvalidClientIdProvidedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidClientIdProvidedError({!r})'.format(self.message)


class InvalidLoginTicketError(ApiError):
    """Invalid login ticket."""

    def __init__(self, error, message):
        super(InvalidLoginTicketError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'InvalidLoginTicketError({!r})'.format(self.message)


class LaunchParametersProvidedUnsupportedError(ApiError):
    """The given launch parameters are not currently supported by the ..."""

    def __init__(self, error, message):
        super(LaunchParametersProvidedUnsupportedError,
              self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'LaunchParametersProvidedUnsupportedError({!r})'.format(
            self.message)


class UnexpectedError(ApiError):
    """An unexpected error has occurred. Please contact ..."""

    def __init__(self, error, message):
        super(UnexpectedError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = False

    def __repr__(self):
        return 'UnexpectedError({!r})'.format(self.message)


class SystemMaintenanceError(ApiError):
    """Smartsheet.com is currently offline for system maintenance. ..."""

    def __init__(self, error, message):
        super(SystemMaintenanceError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = True

    def __repr__(self):
        return 'SystemMaintenanceError({!r})'.format(self.message)


class ServerTimeoutExceededError(ApiError):
    """Server timeout exceeded. Request has failed."""

    def __init__(self, error, message):
        super(ServerTimeoutExceededError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = True

    def __repr__(self):
        return 'ServerTimeoutExceededError({!r})'.format(self.message)


class RateLimitExceededError(ApiError):
    """Rate limit exceeded."""

    def __init__(self, error, message):
        super(RateLimitExceededError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = True

    def __repr__(self):
        return 'RateLimitExceededError({!r})'.format(self.message)


class UnexpectedErrorShouldRetryError(ApiError):
    """An unexpected error has occurred. Please retry your request. If ..."""

    def __init__(self, error, message):
        super(UnexpectedErrorShouldRetryError, self).__init__(error, message)
        self.error = error
        self.message = message
        self.should_retry = True

    def __repr__(self):
        return 'UnexpectedErrorShouldRetryError({!r})'.format(self.message)
