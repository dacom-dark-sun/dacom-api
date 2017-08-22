from rest_framework import serializers

from wallet.models import CURRENCY_TYPES
from wallet.serializers import WalletSerializer
from ico_gateway.models import IcoWallet, IcoProject


class IcoWalletSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = IcoWallet
        fields = '__all__'


class IcoProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = IcoProject
        fields = '__all__'


class CreateIcoWalletSerializer(serializers.Serializer):
    account = serializers.CharField()
    currency = serializers.ChoiceField(CURRENCY_TYPES)
