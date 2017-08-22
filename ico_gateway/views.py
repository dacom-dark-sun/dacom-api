from rest_framework import viewsets, status
from rest_framework.response import Response

from account.models import Account
from wallet.coin_base import coin_base
from wallet.models import Wallet
from ico_gateway.models import IcoWallet, IcoProject
from ico_gateway.serializers import (
    IcoProjectSerializer,
    IcoWalletSerializer,
    CreateIcoWalletSerializer
)


class IcoWalletViewSet(viewsets.ModelViewSet):
    queryset = IcoWallet.objects.all()
    serializer_class = IcoWalletSerializer

    def create(self, request):
        slz = CreateIcoWalletSerializer(data=request.data)
        slz.is_valid(raise_exception=True)

        community = request.community

        if IcoWallet.objects.filter(
            # Если кошелек для ico уже у юзера есть
            wallet__currency=slz.validated_data['currency'],
            wallet__owner__name=slz.validated_data['account'],
            ico_project__community=community
        ).exists():
            return Response('IcoWallet for %s already exists'
                            % slz.validated_data['account'],
                            status.HTTP_400_BAD_REQUEST)

        # Предполагается что аккаунт существует
        # все новые акки сразу синхронизируются
        wallet = Wallet.objects.create(
            owner=Account.objects.get(name=slz.validated_data['account']),
            currency=slz.validated_data['currency']
        )

        new_ico_wallet = IcoWallet.objects.create(
            wallet=wallet,
            ico_project=IcoProject.objects.get(community=request.community),
        )

        return Response(self.serializer_class(new_ico_wallet).data)


class IcoProjectViewSet(viewsets.ModelViewSet):
    queryset = IcoProject.objects.all()
    serializer_class = IcoProjectSerializer
