from django.db import models

from wallet.coin_base import coin_base

from account.models import Account


WALLET_TYPES = (
    ('direct', 'Direct'),  # Для прямого входа
    ('ico', 'ICO'),  # Для ico
)

CURRENCY_TYPES = (
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum'),
)


class Wallet(models.Model):
    owner = models.ForeignKey(Account, null=True, related_name='wallets')
    type = models.CharField(max_length=50, choices=WALLET_TYPES, null=True)
    address = models.CharField(
        max_length=300,
        null=True,
        unique=True,
        blank=True
    )
    currency = models.CharField(
        max_length=300,
        choices=CURRENCY_TYPES,
        default=CURRENCY_TYPES[0][0],
        null=True
    )

    def __str__(self):
        return '{} | {}: {}'.format(self.owner, self.currency, self.type)

    def save(self, *args, **kwargs):
        if not self.pk and not self.address:
            # Для каждого нового кошелька генерируем адрес
            self.address = coin_base.new_address(self.currency)

        super().save(*args, **kwargs)

    @classmethod
    def create_by_account_name(cls, account, currency):
        return cls.objects.create(
            owner=Account.objects.get(name=account),
            currency=currency
        )


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, null=True, related_name='transactions')
    processed_at = models.DateTimeField(null=True, auto_now_add=True)
    hash = models.CharField(max_length=200, null=True)
    success = models.BooleanField(default=False)
    amount = models.DecimalField(
        default=0,
        null=True,
        max_digits=19,
        decimal_places=10
    )

    def __str__(self):
        return '{}: {}'.format(
            self.wallet.currency,
            self.amount
        )
