from django.test import TestCase
from django.urls import reverse
from .models import Account
from rest_framework.test import APIClient


class AccountAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = Account.objects.create_superuser("admin", "admin")
        self.user = Account.objects.create_user("scrapper", "scrapper")

    def test_only_admin_can_access_endpoint(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.get(reverse('account-list'))
        self.assertEqual(res.status_code, 200)

        self.client.logout()

        self.client.force_authenticate(user=self.user)
        res = self.client.get(reverse('account-list'))
        self.assertEqual(res.status_code, 403)

    def test_account_list(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.get(reverse('account-list'))
        response = res.json()
        self.assertEqual(response['count'], 2)

    def test_scrapper_account_creation(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "username": "scrapper1",
            "password": "scrapper1",
            "is_scrapper": True,
        }
        res = self.client.post(reverse('account-list'), format='json', data=data)
        self.assertEqual(res.json()['username'], "scrapper1")
        self.assertEqual(res.status_code, 201)
