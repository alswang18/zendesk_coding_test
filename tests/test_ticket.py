import os
from django.shortcuts import reverse
from django.test import TestCase
from ticket.views import create_ticket_list_context

class ListingPageTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse("ticket_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ticket_list.html")
    
def test_bad_auth(client, monkeypatch):
    envs = {
        'ZENDESK_USER': 'fake_user',
        'ZENDESK_PASSWORD': 'fake_password',
        'ZENDESK_URL': 'https://zccdotslashdev.zendesk.com'
    }
    monkeypatch.setattr(os, 'environ', envs)
    context = create_ticket_list_context(1)
    assert context["error"] == True