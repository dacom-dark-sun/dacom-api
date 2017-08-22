from rest_framework import serializers

from wallet.serializers import WalletSerializer
from account.models import Account


class DacomUserSerializer(serializers.ModelSerializer):
    wallets = WalletSerializer(read_only=True, many=True)

    class Meta:
        model = Account
        exclude = 'id',
