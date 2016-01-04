import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestContacts:
    my_contacts = None

    def test_list_contacts(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Contacts.list_contacts()
        assert action.request_response.status_code == 200
        assert action.total_count > 0
        TestContacts.my_contacts = action.result

    def test_get_contact(self, smart_setup):
        smart = smart_setup['smart']
        contact = smart.Contacts.get_contact(
            TestContacts.my_contacts[0].id
        )
        email = contact.email
        name = contact.name
        the_id = contact.id
        contact_dict = contact.to_dict()
        assert contact.request_response.status_code == 200
        assert contact_dict['email'] == email
