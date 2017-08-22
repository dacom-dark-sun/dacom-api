from django.core.management.base import BaseCommand

from bitshares.bitshares import BitShares
from bitshares.blockchain import Blockchain

from dacom_gateway.settings import DACOM_NODE_WSS
from account.models import Account


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('bc', nargs='?', type=str)
        parser.add_argument('block_num', nargs='?', type=int)

    def handle(self, *args, **options):
        bitshares = BitShares(DACOM_NODE_WSS)

        blockchain = Blockchain(bitshares)

        for a in blockchain.get_all_accounts():
            account, _ = Account.objects.update_or_create(name=a)
