import logging

from django.db import models


log = logging.getLogger(__name__)


class CompanyManager(models.Manager):
    def get_all_company(self):
        return self.all()

    def create_company(self, name):
        try:
            company = self.create(name=name)
            return company
        except Exception as e:
            log.info("Company already exists", extra={"company_name": name, "exception": str(e)})
            raise Exception("Company already exists")

    def get_company_by_name(self, name):
        company = self.filter(name=name).first()
        return company


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CompanyManager()


class EmployeeManager(models.Manager):

    def get_all_employee(self):
        return self.select_related('company').all()

    def get_all_employee_by_cto_id(self, cto_id):
        company = self.filter(id=cto_id).first()
        if company.employee_type == 'cto':
            return self.filter(company__id=company.company.id).select_related('company').exclude(id=cto_id)
        return []

    def create_employee(self, name, company_name, employee_type):
        company = Company.objects.get_company_by_name(company_name)
        employee = self.create(name=name, company=company, employee_type=employee_type)
        return employee


class Employee(models.Model):
    EMPLOYEE_TYPE = (
        ('cto', 'Chief Technology Officer'),
        ('srs', 'Senior Software Engineer'),
        ('sr', 'Software Engineer'),
    )
    name = models.CharField(max_length=100)
    employee_type = models.CharField(max_length=3, choices=EMPLOYEE_TYPE)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EmployeeManager()
