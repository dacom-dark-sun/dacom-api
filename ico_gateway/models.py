from django.db import models


from wallet.models import Wallet
from community.models import Community


PERIOD_CHOICES = (
    ('week', 'Неделя'),
    ('month', 'Месяц'),
)


class IcoProject(models.Model):
    """ То для чего проводится ICO """
    name = models.CharField(max_length=300, null=True, unique=True)
    community = models.OneToOneField(Community, null=True)
    asset_name = models.CharField(max_length=3, null=True, unique=True)
    distribution_period = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES,
        default=PERIOD_CHOICES[0][0],
        null=True
    )

    distribution_count = models.IntegerField(
        'Количество токенов на период',
        default=0
    )

    def __str__(self):
        return self.name


class IcoWallet(models.Model):
    ico_project = models.ForeignKey(IcoProject, null=True)
    wallet = models.ForeignKey(Wallet, null=True, related_name='ico_wallet')

    class Meta:
        unique_together = ('ico_project', 'wallet'),

    def __str__(self):
        return '{}: {}'.format(self.ico_project, self.wallet)


class IcoInvest(models.Model):
    ico_wallet = models.ForeignKey(IcoWallet, null=True)
    amount = models.DecimalField(
        decimal_places=10,
        default=0,
        max_digits=19,
        null=True
    )

    def __str__(self):
        return '{}: {}'.format(self.ico_project, self.wallet)
