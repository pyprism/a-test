from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer
from rest_framework import permissions


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.get_all_company()
    serializer_class = CompanySerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.get_all_employee()
    serializer_class = EmployeeSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]

    def get_permissions(self):
        """Returns the permission based on the type of action"""
        if self.action == "get_all_employee":
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            Employee.objects.create_employee(serializer.validated_data['name'],
                                             serializer.validated_data['company_name'],
                                             serializer.validated_data['employee_type'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_all_employee(self, request):
        query = request.query_params.get('cto_id', None)
        if query:
            queryset = Employee.objects.get_all_employee_by_cto_id(request.query_params.get('cto_id', None))
            serializer = EmployeeSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
