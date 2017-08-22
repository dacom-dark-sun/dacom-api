from django.core.management.base import BaseCommand

from wallet.coin_base import client


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('bc', nargs='?', type=str)
        parser.add_argument('block_num', nargs='?', type=int)

    def handle(self, *args, **options):
        account = client.get_account('fc3ee97c-5121-597a-b076-eac36927add3')
        new_addres = account.create_address()

        #print(account.get_addresses())
        print(new_addres)
