from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from wallet.models import Wallet
from assets.models import Asset, AssetWallet
from assets.serializers import (
    AssetSerializer,
    AssetWalletSerializer,
    AssetWalletReadSerializer,
)


class AssetViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'name'
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class AssetWalletView(APIView):
    """
    Отдает и при необходимости создает кошелек для прямого вхождения
    для пользователя:

    account: Аккаунт
    asset: Ассет
    currency: Криптовалюта BTC/ETH
    """
    def post(self, request):
        slz = AssetWalletSerializer(data=request.data)
        slz.is_valid(raise_exception=True)

        try:
            asset_wallet = AssetWallet.objects.get(
                asset__name=slz.validated_data['asset'],
                wallet__owner__name=slz.validated_data['account'],
                wallet__currency=slz.validated_data['currency'],
            )
        except AssetWallet.DoesNotExist:
            # Тогда создаем
            wallet = Wallet.objects.create(
                owner=slz.validated_data['account'],
                currency=slz.validated_data['currency'],
                type='direct',
            )

            asset_wallet = AssetWallet.objects.create(
                wallet=wallet,
                asset=slz.validated_data['asset']
            )

        return Response(AssetWalletReadSerializer(asset_wallet).data)
