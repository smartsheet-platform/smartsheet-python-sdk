import pytest
import smartsheet
import os.path
import time
import datetime

_dir = os.path.dirname(os.path.abspath(__file__))

@pytest.mark.usefixtures("smart_setup")
class TestProofs:
    # values go here | VERIFY VALUES
    row_url_proof = None
    proof_file_attachment = None
    sheet_discussion = None
    row_discussion = None
    added_comment = None

#################################################################### Attach & Add Tests
    def test_attach_proof_to_sheet(self, smart_setup): # Maybe not needed because of create_proof test
        smart = smart_setup['smart']
        action = smart.Proofs.attach_proof_to_sheet(
            smart_setup['sheet_b'].id,
            ('stooges.jpg', open(_dir + '/fixtures/stooges_v1.jpg', 'rb'), 'image/jpeg')
        )
        assert action.message == 'SUCCESS'
        TestProofs.sheet_file_attachment = action.result

    def test_attach_file_to_comment(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Attachments.attach_file_to_comment(
            smart_setup['sheet_b'].id,
            TestProofs.added_comment.id,
            ('curly.jpg', open(_dir + '/fixtures/curly.jpg', 'rb'), 'image/jpeg')
        )
        assert action.message == 'SUCCESS'

    def test_attach_file_to_row(self, smart_setup): # TO VERIFY
        smart = smart_setup['smart']
        row = smart_setup['sheet_b'].rows[2]
        action = smart.Attachments.attach_file_to_row(
            smart_setup['sheet_b'].id,
            row.id,
            ('quote.txt', open(_dir + '/fixtures/quote.txt', 'rb'), 'text/plain')
        )
        assert action.message == 'SUCCESS'

    def test_add_comment_to_proof(self, smart_setup):
        smart = smart_setup['smart']
        comment = smart.models.Comment({
            'text': 'Hey, fellas!'
        })
        action = smart.Proofs.add_comment_to_proof(
            smart_setup['sheet_b'].id,
            TestProofs.sheet_proof.id,
            comment
        )
        assert action.message == 'SUCCESS'
        TestProofs.added_comment = action.result

    def test_add_url_to_comment(self, smart_setup): # TO VERIFY
        smart = smart_setup['smart']
        url = smart.models.Attachment({
            'name': 'Cool site',
            'url': 'http://www.smartsheet.com/',
            'attachment_type': 'LINK'
        })
        action = smart.Attachments.attach_url_to_comment(
            smart_setup['sheet_b'].id,
            TestProofs.added_comment.id,
            url
        )
        assert action.message == 'SUCCESS'

    def test_add_comment_to_proof_with_attachment(self, smart_setup):
        smart = smart_setup['smart']
        comment = smart.models.Comment({'text': "What're you lookin' at?"})
        action = smart.Proofs.add_comment_to_proof_with_attachment(
            smart_setup['sheet_b'].id,
            TestProofs.sheet_proof.id,
            comment,
            ('stooges.jpg', open(_dir + '/fixtures/stooges_v1.jpg', 'rb'), 'image/jpeg')
        )
        assert action.message == 'SUCCESS'

#################################################################### Get & List Tests
    def test_get_proof(self, smart_setup): # Verify which get_proof test is correct
        smart = smart_setup['smart']
        file = smart.Proofs.get_proof(
            smart_setup['sheet_b'].id,
            TestProofs.sheet_file_proof.id
        )
        assert file.name == 'stooges.jpg'

    def test_get_proof(self, smart_setup): # Verify which get_proof test is correct
        smart = smart_setup['smart']
        sheet = smart.Sheets.get_sheet(
            smart_setup['sheet_b'].id,
            include='proofs'
        )
        assert sheet.request_response.status_code == 200
        proof = smart.Proofs.get_proof(
            sheet.id,
            sheet.proofs[0].id
        )
        assert proof.request_response.status_code == 200
        assert len(proof.comments) > 0

    def test_get_all_proofs(self, smart_setup):
        smart = smart_setup['smart']
        action = smart_setup['sheet_b'].get_all_proofs()
        assert action.request_response.status_code == 200
        assert action.total_count > 0
        proofs = action.result
        assert isinstance(proofs[0], smart.models.proof.Proof)

    def test_get_proof_comment(self, smart_setup):
        smart = smart_setup['smart']
        comment = smart.Proofs.get_proof_comment(
            smart_setup['sheet_b'].id,
            TestProofs.added_comment.id
        )
        assert comment.request_response.status_code == 200
        assert comment.text == 'Hey, fellas!'

    def test_get_row_proofs(self, smart_setup): # Maybe not needed
        smart = smart_setup['smart']
        action = smart.Proofs.get_row_proofs(
            smart_setup['sheet_b'].id,
            smart_setup['sheet_b'].rows[0].id
        )
        assert action.request_response.status_code == 200
        assert action.total_count > 0
        proofs = action.result

    def test_list_all_proofs(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Proofs.list_all_proofs(
            smart_setup['sheet_b'].id
        )
        assert action.total_count > 0

    def test_list_proof_versions(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Proofs.list_proof_versions(
            smart_setup['sheet_b'].id,
            TestProofs.sheet_file_proof.id
        )
        assert action.total_count > 0
        vlist = action.result
        assert isinstance(action.result[0], smart.models.proof.Proof)

#     def test_list_row_attachments(self, smart_setup):      ### Verify not needed ###
#         smart = smart_setup['smart']
#         row = smart_setup['sheet_b'].rows[1]
#         action = smart.Attachments.list_row_attachments(
#             smart_setup['sheet_b'].id,
#             row.id
#         )
#         assert action.request_response.status_code == 200
#         assert action.total_count > 0

    def test_list_proof_attachments(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Attachments.list_proof_attachments(
            smart_setup['sheet_b'].id,
            TestProofs.sheet_proof.id
        )
        assert action.request_response.status_code == 200
        assert action.total_count > 0

#################################################################### Create Tests
    def test_create_proof_on_sheet(self, smart_setup):
        smart = smart_setup['smart']
        action = smart_setup['sheet_b'].create_proof('Nyuk!', 'Poifect!')
        assert action.message == 'SUCCESS'
        TestProofs.sheet_proof = action.result

    def test_create_proof_on_row(self, smart_setup):
        smart = smart_setup['smart']
        row = smart_setup['sheet_b'].rows[0]
        dis = smart.models.Proof({
            'title': 'Nyuk! Nyuk!',
            'comment': smart.models.Comment({'text': 'Poifect!'})
        })

        action = smart.Proofs.create_proof_on_row(
            smart_setup['sheet_b'].id,
            row.id,
            dis
        )
        assert action.message == 'SUCCESS'
        TestProofs.row_proof = action.result

    def test_create_proof_on_row_with_attachment(self, smart_setup):
        smart = smart_setup['smart']
        proof = smart.models.Proof({
            'title': 'What a row!',
            'comment': smart.models.Comment({'text': "This row's lookin' better already!"})
        })
        row = smart_setup['sheet_b'].rows[1]
        action = smart.Proofs.create_proof_on_row_with_attachment(
            smart_setup['sheet_b'].id,
            row.id,
            proof,
            ('curly.jpg', open(_dir + '/fixtures/curly.jpg', 'rb'), 'image/jpeg')
        )
        assert action.message == 'SUCCESS'

    def test_create_proof_on_sheet_with_attachment(self, smart_setup):
        smart = smart_setup['smart']
        proof = smart.models.Proof({
            'title': "Now that's what I call a Sheet",
            'comment': smart.models.Comment({'text': "Get back to woik!"})
        })
        action = smart.Proofs.create_proof_on_sheet_with_attachment(
            smart_setup['sheet_b'].id,
            proof,
            ('moe-curly.jpg', open(_dir + '/fixtures/moe-curly.jpg', 'rb'), 'image/jpeg')
        )
        assert action.message == 'SUCCESS'

#################################################################### Delete Tests
    def test_delete_proof_versions(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Proofs.delete_proof_versions(
            smart_setup['sheet_b'].id,
            TestProofs.sheet_file_proof.id
        )
        assert action.message == 'SUCCESS'

    def test_delete_proof_comment(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Proofs.delete_proof_comment(
            smart_setup['sheet_b'].id,
            TestProofs.added_comment.id
        )
        assert action.message == 'SUCCESS'

    def test_delete_proof(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Proofs.delete_proof(
            smart_setup['sheet_b'].id,
            TestProofs.sheet_proof.id
        )
        assert action.message == 'SUCCESS'

#################################################################### Version Tests
    def test_proof_new_version(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Proofs.proof_new_version(
            smart_setup['sheet_b'].id,
            TestProofs.sheet_file_proof.id,
            ('stooges.jpg', open(_dir + '/fixtures/stooges_v2.jpg', 'rb'), 'image/jpeg')
        )
        assert action.message == 'SUCCESS'

    def test_proof_version(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Proofs.proof_version(
            smart_setup['sheet_b'].id,
            TestProofs.sheet_file_proof.id,
            () ### Find out what goes here
        )