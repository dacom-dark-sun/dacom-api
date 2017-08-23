from django.contrib import admin

from wallet.models import Wallet, Transaction


admin.site.register([
    Wallet,
    Transaction,
])
