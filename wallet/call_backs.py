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

    tr, _ = Transaction.objects.get_or_create(
        hash=data['additional_data']['hash'],
        defaults={
            'wallet': wallet,
            'amount': data['additional_data']['amount']['amount']
        }
    )

    # TODO Implement for another currency
    # Bitcoin
    if tr.amount < 0.0001:
        logger.warning(
            f'Amount less then minimum! {tr.amount}({tr.wallet.currency})'
        )

        return None

    # Transfer money to common address
    try:
        coin_base.send_money(
            data['account']['id'],  # Account from. (current)
            to=DACOM_COMMON_BCT_ADDRESS,
            amount=data['additional_data']['amount']['amount'],
            currency=data['additional_data']['amount']['currency'])

        tr.transferred = True
        tr.save()
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



