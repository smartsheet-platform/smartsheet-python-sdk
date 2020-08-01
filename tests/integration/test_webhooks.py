import pytest


@pytest.mark.usefixtures("smart_setup")
class TestWebhooks:
    webhook = None

    def test_create_webhook(self, smart_setup):
        smart = smart_setup['smart']

        webhook = smart.models.Webhook()
        webhook.name = 'My Webhook'
        webhook.callback_url = 'https://www.smartsheet.com'
        webhook.scope = 'sheet'
        webhook.scope_object_id = smart_setup['sheet'].id
        webhook.events.append('*.*')
        webhook.version = 1
        webhook.subscope = smart.models.WebhookSubscope({'column_ids': [smart_setup['sheet'].columns[0].id]})

        action = smart.Webhooks.create_webhook(webhook)
        assert action.message == 'SUCCESS'
        assert isinstance(action.result, smart.models.Webhook)
        TestWebhooks.webhook = action.result

    def test_list_webhooks(self, smart_setup):
        smart = smart_setup['smart']
        webhooks = smart.Webhooks.list_webhooks()
        assert isinstance(webhooks, smart.models.IndexResult)

    def test_reset_share_secret(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Webhooks.reset_shared_secret(TestWebhooks.webhook.id)
        assert action.message == 'SUCCESS'

    def test_get_webhook(self, smart_setup):
        smart = smart_setup['smart']
        webhook = smart.Webhooks.get_webhook(TestWebhooks.webhook.id)
        assert isinstance(webhook, smart.models.Webhook)

    def test_update_webhook(self, smart_setup):
        smart = smart_setup['smart']
        webhook = smart.models.Webhook()
        webhook.name = 'My New Webhook'
        action = smart.Webhooks.update_webhook(TestWebhooks.webhook.id, webhook)
        assert action.message == 'SUCCESS'

    def test_delete_webhook(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Webhooks.delete_webhook(TestWebhooks.webhook.id)
        assert action.message == 'SUCCESS'
