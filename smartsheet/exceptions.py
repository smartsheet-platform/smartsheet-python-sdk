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

    def __init__(self, error, message=None, should_retry=False):
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
        self.should_retry = should_retry

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


class SystemMaintenanceError(ApiError):
    """Smartsheet.com is currently offline for system maintenance. ..."""

    def __init__(self, error, message):
        super(SystemMaintenanceError, self).__init__(error, message, True)
        self.error = error
        self.message = message
        self.should_retry = True

    def __repr__(self):
        return 'SystemMaintenanceError({!r})'.format(self.message)


class ServerTimeoutExceededError(ApiError):
    """Server timeout exceeded. Request has failed."""

    def __init__(self, error, message):
        super(ServerTimeoutExceededError, self).__init__(error, message, True)
        self.error = error
        self.message = message
        self.should_retry = True

    def __repr__(self):
        return 'ServerTimeoutExceededError({!r})'.format(self.message)


class RateLimitExceededError(ApiError):
    """Rate limit exceeded."""

    def __init__(self, error, message):
        super(RateLimitExceededError, self).__init__(error, message, True)
        self.error = error
        self.message = message
        self.should_retry = True

    def __repr__(self):
        return 'RateLimitExceededError({!r})'.format(self.message)


class UnexpectedErrorShouldRetryError(ApiError):
    """An unexpected error has occurred. Please retry your request. If ..."""

    def __init__(self, error, message):
        super(UnexpectedErrorShouldRetryError, self).__init__(error, message, True)
        self.error = error
        self.message = message
        self.should_retry = True

    def __repr__(self):
        return 'UnexpectedErrorShouldRetryError({!r})'.format(self.message)
