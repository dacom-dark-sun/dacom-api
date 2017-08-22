from bitshares.bitshares import BitShares
from bitshares.blockchain import Blockchain

from dacom_gateway.settings import DACOM_NODE_WSS


class Dacom(BitShares):
    def __init__(self, *args, **kwargs):
        super().__init__(DACOM_NODE_WSS, *args, **kwargs)
        self.blockchain = Blockchain(self)
