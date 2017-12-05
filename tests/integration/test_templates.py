import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestTemplates:
    test_templates = None

    def test_list_public_templates(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Templates.list_public_templates()
        templates = action.result
        assert action.request_response.status_code == 200
        assert action.total_count > 0
        assert isinstance(templates[0], smart.models.template.Template)

    def test_list_user_created_templates(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Templates.list_user_created_templates()
        templates = action.result
        # can't test more because we can't create a template with the API
        assert action.request_response.status_code == 200