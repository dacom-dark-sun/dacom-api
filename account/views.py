from rest_framework import viewsets

from account.models import Account
from account.serializers import DacomUserSerializer


class DacomUserViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'name'
    queryset = Account.objects.all()
    serializer_class = DacomUserSerializer
