from django.core.management.base import BaseCommand

from common.dacom import Dacom

from assets.models import Asset


class Command(BaseCommand):
    def handle(self, *args, **options):
        dacom = Dacom()

        for asset in dacom.rpc.list_assets('', 100):
            Asset.objects.update_or_create(name=asset['symbol'])
