from django.db import models
from django.core.exceptions import ValidationError

from wallet.models import Wallet


class Asset(models.Model):
    name = models.CharField(max_length=50, null=True, unique=True)

    def __str__(self):
        return self.name


class AssetWallet(models.Model):
    asset = models.ForeignKey(Asset, null=True)
    wallet = models.OneToOneField(
        Wallet,
        primary_key=True,
        related_name='asset_wallet',
    )

    def __str__(self):
        return '{} | {} -> {}'.format(
            self.wallet.owner,
            self.asset,
            self.wallet.address
        )

    @property
    def btc(self):
        return self.wallet.address

    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)

        if AssetWallet.objects.filter(
                wallet__owner=self.wallet.owner,
                asset=self.asset).exists():
            raise ValidationError(
                '{} AssetWallet for user "{}" does exists'.format(
                    self.asset, self.wallet.owner)
            )
