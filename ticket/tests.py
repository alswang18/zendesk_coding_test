from django.shortcuts import reverse
from django.test import TestCase


class ListingPageTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse("ticket_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ticket_list.html")
