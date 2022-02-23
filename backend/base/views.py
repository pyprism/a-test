from rest_framework.viewsets import ModelViewSet
from .serializers import AccountSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Account
from .utils import IsAdmin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.order_by('-id')
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdmin]
