'''
Library for working with Smartsheet's version 1.1 API.

This is HORRIBLY incomplete at the moment.

Author:  Scott Wimer <scott.wimer@smartsheet.com>
'''

import json
import os

from smartsheet_exceptions import (SmartsheetClientError,
        OperationOnDiscardedObject)
from base import ContainedThing, slicedict
import client


class Attachment(ContainedThing, object):
    '''
    Information about an attachment.
    There is no reason for an SDK user to create instances of this class.

    Not all instances of Attachment objects are "complete."  In particular,
    if a FILE attachment is not fetched directly then it does not contain the
    url and urlExpiresMillis attributes.  As a result, when fetching a Sheet
    with attachements=True, an additional request to the server is needed to
    get the URL to use to fetch the actual file that was attached to the
    Sheet (or Row or Discussion Comment).

    To handle this, the download() method fetches the latest version of the
    Attachement object prior to downloading the underlying attached file.

    At present, no verification is performed to ensure that the latest version
    of the attachment is materially "the same" (e.g. same name and file type)
    as the version that the caller called .download() on.  In practice, this
    is not expected to be a significant issue.
    '''
    # TODO: Consider renaming this class:  AttachmentInfo or AttachmentMetadata
    # TODO: Check the Example Response secton from Get Row Attachments.
    # I think the use of "parent" instead of "parentType" is an error.
    # TODO: Check the Attachment Object section.
    # I think that url and urlExpiresMillis are actually part of the
    # attachment download info, and not of the attachment information object.
    # Probably, the API docs need to describe this as two different objects,
    # Attachment Information, and the other Attachment Download Information.
    # Otherwise, they're describing an object that does not have a fixed set
    # of fields.
    field_names = '''attachmentType attachmentSubType createdAt createdBy
                    id mimeType name sizeInKb parentType parentId
                    url urlExpiresMillis'''.split()


    def __init__(self, sheet, id, name, attachmentType, attachmentSubType,
            createdAt, createdBy, parentType, parentId, mimeType=None,
            url=None, urlExpiresMillis=None, sizeInKb=None):
        self.sheet = sheet
        self.parent = sheet
        self._id = id
        self._name = name
        self._attachmentType = attachmentType   # TODO: validate this
        self._attachmentSubType = attachmentSubType # TODO: validate this
        self._createdAt = createdAt
        self._createdBy = createdBy
        self._parentType = parentType   # TODO: validate this
        self._parentId = parentId
        self._mimeType = mimeType
        self._url = url                 # I'm not sure this even belongs here.
        self._urlExpiresMillis = urlExpiresMillis   # probably doesn't belong
        self._sizeInKb = sizeInKb
        self._fields = {}       # For consistency with newFromAPI().
        self._data  = None              # The downloaded data goes here.
        self._download_response = None  # The HttpResponse from the download.
        self._discarded = False

    @classmethod
    def newFromAPI(cls, fields, sheet):
        params = slicedict(fields, cls.field_names, include_missing_keys=True)
        att = cls(sheet, **params)
        att._fields = fields
        return att

    @property
    def id(self):
        self.errorIfDiscarded()
        return self._id

    @property
    def name(self):
        self.errorIfDiscarded()
        return self._name

    @property
    def attachmentType(self):
        self.errorIfDiscarded()
        return self._attachmentType

    @property
    def attachmentSubType(self):
        self.errorIfDiscarded()
        return self._attachmentSubType

    @property
    def createdAt(self):
        self.errorIfDiscarded()
        return self._createdAt

    @property
    def createdBy(self):
        self.errorIfDiscarded()
        return client.SimpleUser(self._createdBy)

    @property
    def parentType(self):
        self.errorIfDiscarded()
        return self._parentType

    @property
    def parentId(self):
        self.errorIfDiscarded()
        return self._parentId

    @property
    def mimeType(self):
        self.errorIfDiscarded()
        return self._mimeType

    @property
    def url(self):
        self.errorIfDiscarded()
        return self._url

    @property
    def urlExpiresMillis(self):
        self.errorIfDiscarded()
        return self._urlExpiresMillis

    @property
    def sizeInKb(self):
        self.errorIfDiscarded()
        return self._sizeInKb
 
    @property
    def fields(self):
        self.errorIfDiscarded()
        return self._fields

    @property
    def path(self):
        self.errorIfDiscarded()
        return '/sheet/%s/attachment/%s' % (str(self.sheet.id), str(self.id))

    @property
    def data(self):
        self.errorIfDiscarded()
        return self._data

    @property
    def download_response(self):
        self.errorIfDiscarded()
        return self._download_response

    @property
    def replacePath(self):
        # I'm not sure that this is the right approach.
        # It might be that Sheet.replaceAttachment() would be the way to go.
        # Or, perhaps, we should just let the user of the library do it by
        # uploading a new attachment and deleting the old one.  That seems
        # like the simplest approach.
        raise NotImplementedError("Attachment.replacePath() not implemented")

    @property
    def newVersionPath(self):
        # TODO:  Support limiitiations on where a new version can be uploaded.
        # Attachments on Discussion Comments can not have new versions uploaded
        # for them.  If we don't detect that in the SDK, it will result in an
        # error from the server.
        # A new version is only supported for FILE attachments to Sheets or
        # Rows, at least according to the current API docs (I haven't checked).
        self.errorIfDiscarded()
        return '/sheet/%s/attachment/%s/versions' % (str(self.sheet.id),
                str(self.id))

    @property
    def sourceInfo(self):
        '''
        Human usable information about the source of the attachment.
        '''
        raise NotImplementedError("Attachment.sourceInfo not implemented.")

    def discard(self):
        '''
        Mark this Attachment as discarded, further operations on it will fail.
        '''
        self._discarded = True
        return

    def getVersionList(self, client=None):
        '''
        Get a list of all versions of the Attachment.
        Returns the list of Attachment objects.
        NOTE:  these Attachment objects have additional fields that regular
        Attachment objects don't: 'parentType' and 'parentId'
        '''
        self.errorIfDiscarded()
        path = '/sheet/%s/attachment/%s/versions' % (str(self.sheet.id),
                str(self.id))
        name = "%s.getVersionList()" % self
        client = client or self.client
        body = client.GET(path, name=name)
        return [Attachment(a, self.sheet) for a in body]

    def getFullInfo(self, client=None):
        '''
        Fetch the full Attachment information for this Attachment.
        This call is only necessary for FILE attachments, all other
        attachmentTypes already contain the complete information about the
        attachment.  This call is optional for other attachment types.

        @return Fully populated Attachment object.
        @param client Optional SmartsheetClient instance to use.
        '''
        self.errorIfDiscarded()
        name = "%s.getFullInfo()" % self
        client = client or self.client
        body = client.GET(self.path, name=name)
        return Attachment(body, self.sheet)

    def download(self, client=None):
        '''
        Download the file/data from the Attachment's URL.
        The data fetched from the URL is placed in the .data attribute of
        the returned Attachment object.

        @param client Optional SmartsheetClient instance to use.
        @return Attachment object with a populated .data attribute.
        '''
        self.errorIfDiscarded()
        att = self.getFullInfo()
        client = client or att.client
        if not att.url:
            err = ("%s.download() attempted without a 'url' "
                    "attribute" % att)
            self.logger.error(err)
            raise SmartsheetClientError(err)
        resp, att._data = client.rawRequest(att.url, '', 'GET')
        att._download_response = client.HttpResponse(resp)
        if att.download_resonse.isOK():
            return att
        err = ("%s.download() failed: %s" % (att, resp.hdr))
        self.logger.error(err)
        raise SmartsheetClientError(err)


    def downloadAndStore(self, base_path='', client=None):
        '''
        Download and store an attachment.
        The attachment contents are also available at .data on the returned
        Attachment object.

        @param base_path The path to store the downloaded file at.
        @param client Optional SmartsheetClient instance to use.
        @return Attachment object with a populated .data attribute.
        '''
        self.errorIfDiscarded()
        att = self.download(client=client)
        path = os.path.join(base_path, att.name)
        with file(path, 'w') as fh:
            fh.write(att.data)
        return att

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
        self.errorIfDiscarded()
        if self.attachmentType != 'FILE':
            err = ("Attachment.uploadNewVersion() Can only replace 'FILE' " +
                    "Attachment types")
            self.logger.error(err)
            raise SmartsheetClientError(err)
        path = '/sheet/%s/attachment/%s/versions' % (
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
                 
    def errorIfDiscarded(self):
        if self._discarded:
            raise OperationOnDiscardedObject("Attachment was discarded.")
    def __str__(self):
        self.errorIfDiscarded()
        return '<Attachment id:%r, name:%r, type:%r:%r created:%r>' % (
                self.id, self.name, self.attachmentType, self.mimeType,
                self.createdAt)

    def __repr__(self):
        self.errorIfDiscarded()
        return str(self)


class AttachPoint(object):
    def __init__(self):
        pass

    def get_attach_path(self):
        raise NotImplementedError("Classes using the AttachPoint mixin must "
                                  "define a get_attach_path() call that "
                                  "returns a string URL path")

    def attachFile(self, filename, client=None):
        self.errorIfDiscarded()
        with open(filename, 'rb') as f:
            buf = f.read()
        return self.attachBytes(filename, buf, client=client)

    def attachBytes(self, attachment_name, data, client=None):
        self.errorIfDiscarded()
        headers = {
            'Content-Disposition':
                'attachment; filename="{0}"'.format(attachment_name),
            'Content-Type': 'application/octest-stream',
            'Content-Length': str(len(data)),
        }
        obj = client or self.client
        result = obj.request(self.get_attach_path(),
                             "POST",
                             headers,
                             data)
        return result

    def attachUrl(self, url, link_name=None, link_description=None,
                  client=None):
        self.errorIfDiscarded()
        data = {}
        data['name'] = link_name
        data['description'] = link_description
        data['url'] = url
        data['attachmentType'] = 'LINK'
        data['attachmentSubType'] = None
        body = json.dumps(data)
        obj = client or self.client
        result = obj.request(self.get_attach_path(),
                             "POST",
                             None,
                             body)
        return result
