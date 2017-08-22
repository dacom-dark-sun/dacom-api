import logging

from rest_framework import viewsets, decorators, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from wallet.models import Wallet
from wallet.serializers import WalletSerializer
from wallet.coin_base import NotificationError, coin_base

from wallet import call_backs


logger = logging.getLogger('transactions')


handlers = {
    'wallet:addresses:new-payment': call_backs.new_payment
}


class IcoWalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


@decorators.api_view(['POST'])
@decorators.permission_classes([AllowAny])
def coinbase_callback(request):
    from pprint import pformat
    logger.info('new hook meta: \n %s' % pformat(request.META))
    signature = request.META.get(['CB-SIGNATURE'], '')

    if not coin_base.verify_callback(request.body, signature):
        logger.warning('Hook not validated! \n %s' % request.body)
        return Response('You are not coinbase!!', status.HTTP_403_FORBIDDEN)

    logger.info('New Hook\n %s' % request.body)
    data = request.data

    handler = handlers.get(data['type'])

    if not handler:
        logger.warning('Unsupported notification type %s' % data['type'])
        return Response('OK')

    try:
        handler(data)
    except NotificationError:
        return Response('ERR')
    except:
        logger.exception('Err in notification handler')

    return Response('OK')
