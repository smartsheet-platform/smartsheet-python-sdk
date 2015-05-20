'''
Library for working with Smartsheet's version 1.1 API.

This is HORRIBLY incomplete at the moment.

Author:  Scott Wimer <scott.wimer@smartsheet.com>
'''

import client
from base import (ContainedThing, slicedict)
from attachment import Attachment, AttachPoint
from smartsheet_exceptions import OperationOnDiscardedObject
import json

class Discussion(ContainedThing):
    '''
    Information about a Discussion.
    Depending on how the fields were obtained, the Discussion may or may not
    contain the Comments and Attachments from the Discussion.
    '''
    field_names = '''id title comments createdBy lastCommentedAt
                lastCommentedUser commentAttachments parentType'''.split()
    # The same sort of incompletely specified situation that exists for
    # Attachments is present for Discussions.  If the Discussion's parent,
    # or the Discussion itself was not fetched with an include option that
    # specified 'comments' and 'attachments', then these won't be in the
    # data from the server used to populate the Discussion object.
    # We can force the request of a fully populated Discussion object, but
    # we are left with the uncertainty of what should be done with the
    # original.  For now, we leave the original untouched (and don't bother
    # updating any pointers to it) and return the complete one to the caller
    # that requested it.
    #
    # A Discussion can be associated with either a Sheet or a Row.
    # However, all Discussions are associated with the Sheet, whether they
    # are also directly associated with a Row or not.  Depending on the
    # way the Discussion was fetched, it may or may not indicate its direct
    # parent.

    def __init__(self, sheet, title, id=-1, comments=None,
            commentAttachments=None, parentId=None, parentType=None,
            lastCommentedAt=None, lastCommentedUser=None, createdBy=None):
        self.sheet = sheet
        self.parent = sheet
        self._title = title
        self._id = id
        self._comments = comments or []
        self._commentAttachments = commentAttachments or []
        self._parentId = parentId
        self._parentType = parentType
        self._lastCommentedAt = lastCommentedAt
        self._lastCommentedUser = lastCommentedUser
        self._createdBy = createdBy
        self._fields = {}
        self._discarded = False

    @classmethod
    def newFromAPI(cls, fields, sheet):
        params = slicedict(fields, cls.field_names, include_missing_keys=True)
        params['commentAttachments'] = [Attachment.newFromAPI(a, sheet) for a in
                fields.get('commentAttachments', [])]
        params['comments'] = [Comment.newFromAPI(c, sheet) for c in
                fields.get('comments', [])]
        params['createdBy'] = client.SimpleUser(fields['createdBy'])
        disc = cls(sheet, **params)
        disc._fields = fields
        return disc

    @property
    def id(self):
        self.errorIfDiscarded()
        return self._id

    @property
    def title(self):
        self.errorIfDiscarded()
        return self._title

    @property
    def comments(self):
        self.errorIfDiscarded()
        return self._comments

    @property
    def commentAttachments(self):
        self.errorIfDiscarded()
        return self._commentAttachments

    @property
    def lastCommentedAt(self):
        self.errorIfDiscarded()
        return self._lastCommentedAt

    @property
    def lastCommentedUser(self):
        self.errorIfDiscarded()
        return self._lastCommentedUser

    @property
    def createdBy(self):
        self.errorIfDiscarded()
        return self._createdBy

    @property
    def parentType(self):
        self.errorIfDiscarded()
        return self._parentType

    def getAttachmentsByName(self, name):
        '''
        Return a list of Attachments that match the specified name.

        @param name The name of the attachment(s) to find.
        @return List of matching attachments; an empty list when none found.
        '''
        self.errorIfDiscarded()
        return [a for a in self.commentAttachments if a.name == name]

    def discard(self):
        for comment in self.comments:
            comment.discard()
        for attachment in self.commentAttachments:
            attachment.discard()
        self._discarded = False

    def errorIfDiscarded(self):
        if self._discarded:
            raise OperationOnDiscardedObject("Comment was discarded.")

    def __str__(self):
        self.errorIfDiscarded()
        return '<Discussion id:%r title:%r>' % (self.id, self.title)

    def __repr__(self):
        self.errorIfDiscarded()
        return str(self)

    def addComment(self, text, client=None):
        self.errorIfDiscarded()
        client = client or self.client
        # headers = {
        #     'Content-Type': 'application/json',
        # }
        body = json.dumps({'text': text})
        path = 'sheet/{0}/discussion/{1}/comments'.format(
                self.sheet.id,
                self.id)
        response = client.POST(
                path,
                extra_headers=client.json_headers,
                body=body)
        return Comment.newFromAPI(response['result'], self.sheet)

    def refreshComments(self, client=None):
        self.errorIfDiscarded()
        client = client or self.client
        path = 'sheet/{0}/discussion/{1}'.format(self.sheet.id, self.id)
        response = client.GET(path)
        self._comments = [Comment.newFromAPI(i, self.sheet) for i in
                response['comments']]


class Comment(AttachPoint, ContainedThing):
    '''
    A Comment on a Discussion.
    '''
    # Just like Attachments and Discussions, the Comment might not be
    # fully complete when it is fetched.  The attachements array on the
    # Comment will only be included from the server if it is specifically
    # included in the request for the Sheet, Row, or Discussion.
    # The API docs do not indicated that you can get the attachments when
    # fetching a specific Comment.
    # TODO:  Determine if you can get attachments when fetching a Comment by ID.
    field_names = '''id text createdBy createdAt modifiedAt
                    attachments discussionId'''.split()

    def __init__(self, sheet, id=None, text='', createdBy=None, createdAt=None,
            modifiedAt=None, attachments=None, discussionId=None):
        self.sheet = sheet
        # TODO:  Should the parent be a Discussion object?
        # We might not have the Discussion object if somebody tried to fetch
        # a Comment directly.  But, we don't really give them a way to do
        # that.
        self.parent = sheet
        self._id = id
        self._text = text
        self._createdBy = createdBy
        self._createdAt = createdAt
        self._modifiedAt = modifiedAt
        self._attachments = attachments or []
        self._discussionId = discussionId
        self._fields = {}
        self._discarded = False

    @classmethod
    def newFromAPI(cls, fields, sheet):
        params = slicedict(fields, cls.field_names, include_missing_keys=True)
        params['attachments'] = [Attachment.newFromAPI(a, sheet) for a in 
                fields.get('attachments', [])]
        comment = Comment(sheet, **params)
        comment._fields = fields
        return comment

    @property
    def id(self):
        self.errorIfDiscarded()
        return self._id

    @property
    def text(self):
        self.errorIfDiscarded()
        return self._text

    @property
    def createdBy(self):
        self.errorIfDiscarded()
        return self._createdBy

    @property
    def createdAt(self):
        self.errorIfDiscarded()
        return self._createdAt

    @property
    def modifiedAt(self):
        self.errorIfDiscarded()
        return self._modifiedAt

    @property
    def attachments(self):
        self.errorIfDiscarded()
        return self._attachments

    @property
    def discussionId(self):
        self.errorIfDiscarded()
        return self._discussionId

    @property
    def fields(self):
        self.errorIfDiscarded()
        return self._fields

    def discard(self):
        for att in self.attachments:
            att.discard()
        self._discarded = True

    def getFullInfo(self, client=None):
        '''
        Fetch the complete version of this Comment.
        The complete version will include any Attachments and should include
        the discussionId for the Discussion this comment is part of.

        @param client Optional SmartsheetClient instance to use.
        @return Fully-populated Comment object.
        '''
        self.errorIfDiscarded()
        path = '/sheet/%s/comment/%s/' % (str(self.sheet.id), str(self.id))
        client = client or self.client
        body = client.get(path, name='Comment.getFullInfo(%s)' % str(self.id))
        return self.__class__.newFromAPI(body, self.sheet)

    def addAttachment(self, attachment):
        raise NotImplementedError("Support for adding attachments to "
                "comments is not implemented.")

    def errorIfDiscarded(self):
        if self._discarded:
            raise OperationOnDiscardedObject("Comment was discarded.")

    def get_attach_path(self):
        self.errorIfDiscarded()
        sheet_id = self.sheet.id
        comment_id = self.id
        path = 'sheet/{0}/comment/{1}/attachments'.format(sheet_id, comment_id)
        return path
