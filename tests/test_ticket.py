import os

from django.test import TestCase

from ticket.utils import (
    create_ticket_detail_context,
    create_ticket_list_context,
    get_group_name,
    get_user_name,
)


class ListingPageTest(TestCase):
    def test_get_list_view(self):
        response = self.client.get("/?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ticket_list.html")

    def test_get_detail_view(self):
        response = self.client.get("/ticket/1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ticket.html")


def test_utils():
    # specific to applicant's context
    assert get_group_name(4411238137236) is not None
    assert get_user_name(421994449552) is not None
    assert not create_ticket_list_context()["error"]
    assert not create_ticket_detail_context()["error"]


def test_bad_auth(monkeypatch):
    envs = {
        "ZENDESK_USER": "fake_user",
        "ZENDESK_PASSWORD": "fake_password",
        "ZENDESK_URL": "https://zccdotslashdev.zendesk.com",
    }
    monkeypatch.setattr(os, "environ", envs)
    list_context = create_ticket_list_context()
    assert list_context["error"]
    detail_context = create_ticket_detail_context()
    assert detail_context["error"]
