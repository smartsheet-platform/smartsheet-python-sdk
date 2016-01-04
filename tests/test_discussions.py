import pytest
import smartsheet
import os.path

_dir = os.path.dirname(os.path.abspath(__file__))

@pytest.mark.usefixtures("smart_setup")
class TestDiscussions:
    sheet_discussion = None
    row_discussion = None
    added_comment = None

    def test_create_discussion_on_sheet(self, smart_setup):
        smart = smart_setup['smart']
        action = smart_setup['sheet_b'].create_discussion('Nyuk!', 'Poifect!')
        assert action.message == 'SUCCESS'
        TestDiscussions.sheet_discussion = action.result

    def test_create_discussion_on_row(self, smart_setup):
        smart = smart_setup['smart']
        row = smart_setup['sheet_b'].rows[0]
        dis = smart.models.Discussion({
            'title': 'Nyuk! Nyuk!',
            'comment': smart.models.Comment({'text': 'Poifect!'})
        })

        action = smart.Discussions.create_discussion_on_row(
            smart_setup['sheet_b'].id,
            row.id,
            dis
        )
        assert action.message == 'SUCCESS'
        TestDiscussions.row_discussion = action.result

    def test_get_all_discussions(self, smart_setup):
        smart = smart_setup['smart']
        action = smart_setup['sheet_b'].get_all_discussions()
        assert action.request_response.status_code == 200
        assert action.total_count > 0
        discussions = action.result
        assert isinstance(discussions[0], smart.models.discussion.Discussion)

    def test_add_comment_to_discussion(self, smart_setup):
        smart = smart_setup['smart']
        comment = smart.models.Comment({
            'text': 'Hey, fellas!'
        })
        action = smart.Discussions.add_comment_to_discussion(
            smart_setup['sheet_b'].id,
            TestDiscussions.sheet_discussion.id,
            comment
        )
        assert action.message == 'SUCCESS'
        TestDiscussions.added_comment = action.result

    def test_get_discussion_comment(self, smart_setup):
        smart = smart_setup['smart']
        comment = smart.Discussions.get_discussion_comment(
            smart_setup['sheet_b'].id,
            TestDiscussions.added_comment.id
        )
        assert comment.request_response.status_code == 200
        assert comment.text == 'Hey, fellas!'

    def test_get_row_discussions(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Discussions.get_row_discussions(
            smart_setup['sheet_b'].id,
            smart_setup['sheet_b'].rows[0].id
        )
        assert action.request_response.status_code == 200
        assert action.total_count > 0
        discussions = action.result

    def test_get_discussion(self, smart_setup):
        smart = smart_setup['smart']
        sheet = smart.Sheets.get_sheet(
            smart_setup['sheet_b'].id,
            include='discussions'
        )
        assert sheet.request_response.status_code == 200
        discussion = smart.Discussions.get_discussion(
            sheet.id,
            sheet.discussions[0].id
        )
        assert discussion.request_response.status_code == 200
        assert len(discussion.comments) > 0

    def test_add_url_to_comment(self, smart_setup):
        smart = smart_setup['smart']
        url = smart.models.Attachment({
            'name': 'Cool site',
            'description': 'You have to see this.',
            'url': 'http://www.smartsheet.com/',
            'attachment_type': 'LINK'
        })
        action = smart.Attachments.attach_url_to_comment(
            smart_setup['sheet_b'].id,
            TestDiscussions.added_comment.id,
            url
        )
        assert action.message == 'SUCCESS'

    def test_attach_file_to_comment(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Attachments.attach_file_to_comment(
            smart_setup['sheet_b'].id,
            TestDiscussions.added_comment.id,
            ('curly.jpg', open(_dir + '/fixtures/curly.jpg', 'rb'), 'image/jpeg')
        )
        assert action.message == 'SUCCESS'

    def test_attach_file_to_row(self, smart_setup):
        smart = smart_setup['smart']
        row = smart_setup['sheet_b'].rows[2]
        action = smart.Attachments.attach_file_to_row(
            smart_setup['sheet_b'].id,
            row.id,
            ('quote.txt', open(_dir + '/fixtures/quote.txt', 'rb'), 'text/plain')
        )
        assert action.message == 'SUCCESS'

    def test_add_comment_to_discussion_with_attachment(self, smart_setup):
        smart = smart_setup['smart']
        comment = smart.models.Comment({'text': "What're you lookin' at?"})
        action = smart.Discussions.add_comment_to_discussion_with_attachment(
            smart_setup['sheet_b'].id,
            TestDiscussions.sheet_discussion.id,
            comment,
            ('stooges.jpg', open(_dir + '/fixtures/stooges_v1.jpg', 'rb'), 'image/jpeg')
        )
        assert action.message == 'SUCCESS'

    def test_create_discussion_on_row_with_attachment(self, smart_setup):
        smart = smart_setup['smart']
        discussion = smart.models.Discussion({
            'title': 'What a row!',
            'comment': smart.models.Comment({'text': "This row's lookin' better already!"})
        })
        row = smart_setup['sheet_b'].rows[1]
        action = smart.Discussions.create_discussion_on_row_with_attachment(
            smart_setup['sheet_b'].id,
            row.id,
            discussion,
            ('curly.jpg', open(_dir + '/fixtures/curly.jpg', 'rb'), 'image/jpeg')
        )
        assert action.message == 'SUCCESS'

    def test_list_row_attachments(self, smart_setup):
        smart = smart_setup['smart']
        row = smart_setup['sheet_b'].rows[1]
        action = smart.Attachments.list_row_attachments(
            smart_setup['sheet_b'].id,
            row.id
        )
        assert action.request_response.status_code == 200
        assert action.total_count > 0

    def test_list_discussion_attachments(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Attachments.list_discussion_attachments(
            smart_setup['sheet_b'].id,
            TestDiscussions.sheet_discussion.id
        )
        assert action.request_response.status_code == 200
        assert action.total_count > 0

    def test_create_discussion_on_sheet_with_attachment(self, smart_setup):
        smart = smart_setup['smart']
        discussion = smart.models.Discussion({
            'title': "Now that's what I call a Sheet",
            'comment': smart.models.Comment({'text': "Get back to woik!"})
        })
        action = smart.Discussions.create_discussion_on_sheet_with_attachment(
            smart_setup['sheet_b'].id,
            discussion,
            ('moe-curly.jpg', open(_dir + '/fixtures/moe-curly.jpg', 'rb'), 'image/jpeg')
        )
        assert action.message == 'SUCCESS'

    def test_delete_discussion_comment(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Discussions.delete_discussion_comment(
            smart_setup['sheet_b'].id,
            TestDiscussions.added_comment.id
        )
        assert action.message == 'SUCCESS'

    def test_delete_discussion(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Discussions.delete_discussion(
            smart_setup['sheet_b'].id,
            TestDiscussions.sheet_discussion.id
        )
        assert action.message == 'SUCCESS'

