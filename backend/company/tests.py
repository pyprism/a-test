from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from base.models import Account
from company.models import Company, Employee


class TestCompanyApi(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = Account.objects.create_superuser("admin", "admin")
        self.client.force_authenticate(user=self.admin)

    def test_company_create(self):
        url = reverse("company-list")
        data = {"name": "Test Company"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], data["name"])


class TestEmployeeApi(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = Account.objects.create_superuser("admin", "admin")
        self.client.force_authenticate(user=self.admin)
        self.com = Company.objects.create(name="Test Company")
        self.cto = Employee.objects.create(name="CTO", employee_type="cto", company=self.com)

    def test_employee_create(self):
        url = reverse("employee-list")
        data = {"name": "CTO", "employee_type": "cto", "company_name": "Test Company"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], data["name"])

    def test_get_all_employee_by_cto_id(self):
        Employee.objects.create(name="sr", employee_type="sr", company=self.com)
        url = reverse("employee-get-all-employee") + f"?cto_id={self.cto.id}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_all_employee_by_cto_id_without_auth(self):
        Employee.objects.create(name="sr", employee_type="sr", company=self.com)
        self.client.logout()
        url = reverse("employee-get-all-employee") + f"?cto_id={self.cto.id}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
