from django.contrib import admin

from assets.models import Asset, AssetWallet


admin.site.register([
    Asset,
    AssetWallet
])
