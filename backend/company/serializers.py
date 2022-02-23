from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Company, Employee


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class EmployeeSerializer(ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_name = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'name', 'company', 'employee_type', 'company_name')
