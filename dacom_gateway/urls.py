from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from account import views as account_views
from ico_gateway import views as ico_gateway_views
from wallet import views as wallet_views
from faucet.views import faucet
from assets import views as assets_views


router = DefaultRouter()
router.register('accounts', account_views.DacomUserViewSet)
router.register('assets', assets_views.AssetViewSet)
router.register('ico_projects', ico_gateway_views.IcoProjectViewSet)
router.register('ico_wallets', ico_gateway_views.IcoWalletViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^faucet/', faucet),

    url(r'^api/', include(router.urls)),
    url(r'^api/asset-wallet/', assets_views.AssetWalletView.as_view()),

    url(r'^coinbase_callback/$', wallet_views.coinbase_callback),
]
