from coinbase.wallet.client import Client
from dacom_gateway.settings import (
    COIN_BASE_API_KEY,
    COIN_BASE_API_SECRET,
    COIN_BASE_ACCOUNTS
)


class NotificationError(Exception):
    pass


class CoinBase(Client):
    def new_address(self, currency):
        account = self.get_account(COIN_BASE_ACCOUNTS[currency])

        return account.create_address()['address']


coin_base = CoinBase(COIN_BASE_API_KEY, COIN_BASE_API_SECRET)
