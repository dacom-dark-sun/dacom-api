from coinbase.wallet.client import Client
from dacom_gateway.settings import (
    COIN_BASE_API_KEY,
    COIN_BASE_API_SECRET,
)


class NotificationError(Exception):
    pass


class CoinBase(Client):
    accounts = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for account in self.get_accounts()['data']:
            self.accounts[account['balance']['currency']] = account['id']

    def new_address(self, currency):
        account = self.get_account(self.accounts[currency])

        return account.create_address()['address']


coin_base = CoinBase(COIN_BASE_API_KEY, COIN_BASE_API_SECRET)
