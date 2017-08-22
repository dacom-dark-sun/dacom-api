import logging

from bitshares.bitshares import BitShares, Account
from bitshares.exceptions import AccountDoesNotExistsException

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view

from dacom_gateway.settings import DACOM_NODE_WSS, REGISTRAR, REFERRER
from faucet.serializers import (
    SignUpWithKeysSerialzer,
    SignUpWithPasswordSerialzer
)


logger = logging.getLogger('dacom')


def validate(slz, request):
    """ Return valid data """
    slz = slz(data=request.data, context={'request': request})
    slz.is_valid(raise_exception=True)
    return slz.validated_data


@api_view(['POST'])
@permission_classes((AllowAny,))
def faucet(request):
    params = {}

    if 'password' in request.data:
        data = validate(SignUpWithPasswordSerialzer, request)
        params['password'] = data['password']
    else:
        # By default with pubKeys
        data = validate(SignUpWithKeysSerialzer, request)
        params['owner_key'] = data['owner_key'],
        params['active_key'] = data['active_key'],
        params['memo_key'] = data['memo_key'],

    params['account'] = data['account']

    bitshares = BitShares(
        DACOM_NODE_WSS,
        keys=[REGISTRAR['wif']]
    )

    try:
        Account(params['account'], bitshares_instance=bitshares)
        return Response('Account already exists', status.HTTP_400_BAD_REQUEST)
    except AccountDoesNotExistsException:
        pass

    registrar = Account(REGISTRAR['name'], bitshares_instance=bitshares)
    referrer = Account(REFERRER['name'], bitshares_instance=bitshares)
    referrer_percent = REFERRER['present']

    try:
        result = bitshares.create_account(
            params.pop('account'),
            registrar=registrar['id'],
            referrer=referrer['id'],
            referrer_percent=referrer_percent,
            storekeys=False,
            **params,
        )['operations'][0][1]
    except Exception as e:
        logger.exception('Ошибка создания пользователя')
        return Response(e, status.HTTP_500_INTERNAL_SERVER_ERROR)

    logger.info('New account created: %s' % result['name'])

    return Response({
        'account': {
            'name': result['name'],
            'owner_key': result['owner']['key_auths'][0][0],
            'active_key': result['active']['key_auths'][0][0],
            'memo_key': result['options']['memo_key'],
            'referrer': referrer['name'],
            'btc': 'какой btc отдавать?',
        }
    })
