import logging

from django.core.exceptions import ObjectDoesNotExist

from dacom_gateway.settings import DACOM_COMMON_BCT_ADDRESS
from wallet.models import Transaction, Wallet
from wallet.coin_base import NotificationError, coin_base


logger = logging.getLogger('transactions')


def new_payment(data):
    try:
        wallet = Wallet.objects.get(address=data['data']['address'])
    except ObjectDoesNotExist:
        logger.critical('Not found wallet for payment! {}: {}'.format(
                        data['additional_data']['amount']['currency'],
                        data['additional_data']['hash']))
        raise NotificationError

    tr = Transaction.objects.create(
        wallet=wallet,
        hash=data['additional_data']['hash'],
        amount=data['additional_data']['amount']['amount']
    )

    # Transfer money to common address
    try:
        coin_base.send_money(
            data['account']['id'],  # Account from. (current)
            to=DACOM_COMMON_BCT_ADDRESS,
            amount=data['additional_data']['amount']['amount'],
            currency=data['additional_data']['amount']['currency'],  # Currency
        )
    except Exception as e:
        logger.critical('TO COMMON -> {} hash: {}'.format(e.message, tr.hash))
        return None

    logger.info('Transaction completed: {}({}): {}'.format(
        data['additional_data']['amount']['amount'],
        data['additional_data']['amount']['currency'],
        data['additional_data']['hash'])
    )

    handle_transaction(tr)


def handle_transaction(tr):
    # Определяем тип транзакции

    print(tr.wallet.type)



