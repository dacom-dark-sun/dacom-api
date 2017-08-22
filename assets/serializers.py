from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from account.models import Account
from wallet.serializers import WalletSerializer
from wallet.models import CURRENCY_TYPES
from assets.models import Asset, AssetWallet


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        exclude = 'id',


class AssetWalletReadSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = AssetWallet
        fields = 'wallet',


class AssetWalletSerializer(serializers.Serializer):
    currency = serializers.ChoiceField(CURRENCY_TYPES)
    account = serializers.CharField()
    asset = serializers.CharField()

    def validate_account(self, data):
        try:
            account = Account.objects.get(name=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Account does not exists')

        return account

    def validate_asset(self, data):
        try:
            asset = Asset.objects.get(name=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('asset does not exists')

        return asset
