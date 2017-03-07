import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
@pytest.mark.usefixtures("tmpdir")
class TestUsers:
    added_user = None
    alt_emails = None

    def test_get_current_user(self, smart_setup):
        smart = smart_setup['smart']
        me = smart.Users.get_current_user()
        assert isinstance(me.id, int)

    def test_get_user(self, smart_setup):
        smart = smart_setup['smart']
        user = smart.Users.get_user(smart_setup['users']['larry'].id)
        assert isinstance(user, smart.models.user_profile.UserProfile)

    def test_update_user(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Users.update_user(
            smart_setup['users']['moe'].id,
            smart.models.User({
                'licensedSheetCreator': True,
                'admin': False
            })
        )
        user = action.result
        assert action.message == 'SUCCESS'

    def test_add_user(self, smart_setup):
        smart = smart_setup['smart']
        shemp = smart.models.User({
            'email': 'shemp@example.com',
            'first_name': 'Shemp',
            'last_name': 'Howard',
            'licensed_sheet_creator': False,
            'admin': False
        })
        action = smart.Users.add_user(shemp)
        user = action.result
        TestUsers.added_user = user
        assert action.message == 'SUCCESS'

    def test_list_users(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Users.list_users()
        users = action.result
        assert action.total_count > 2

    def test_list_users_filtered(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Users.list_users(
            email=smart_setup['users']['moe'].email
                 + ','
                 + smart_setup['users']['curly'].email
        )
        users = action.result
        assert action.total_count < 3

    def test_remove_user(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Users.remove_user(
            TestUsers.added_user.id
        )
        assert action.message == 'SUCCESS'

    def test_list_org_sheets(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Users.list_org_sheets()
        sheets = action.result
        assert isinstance(sheets[0], smart.models.sheet.Sheet)

    def test_add_alternate_email(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Users.add_alternate_email(
            smart_setup['users']['larry'].id,
            [
                smart.models.AlternateEmail({
                    'email': 'foo@somecompany.com'
                }),
                smart.models.AlternateEmail({
                    'email': 'bar@somecompany.com'
                })
            ]
        )
        assert action.message == 'SUCCESS'
        emails = action.result
        TestUsers.alt_emails = emails

    def test_list_alternate_emails(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Users.list_alternate_emails(
            smart_setup['users']['larry'].id
        )
        assert action.total_count > 0
        assert isinstance(action.result[0], smart.models.AlternateEmail)
        TestUsers.alt_emails = action.result

    def test_get_alternate_email(self, smart_setup):
        smart = smart_setup['smart']
        alt_email = smart.Users.get_alternate_email(
            smart_setup['users']['larry'].id,
            TestUsers.alt_emails[0].id
        )
        assert isinstance(alt_email, smart.models.AlternateEmail)

    def test_delete_alternate_email(self, smart_setup):
        smart = smart_setup['smart']
        for email in TestUsers.alt_emails:
            action = smart.Users.delete_alternate_email(
                smart_setup['users']['larry'].id,
                email.id
            )
            assert action.message == 'SUCCESS'


