# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os import path

# from django.conf import settings

from .jsonrpc import EthJsonRpc

contract_path = path.join(path.dirname(path.abspath(__file__)), 'server.se')
contract_code = open(contract_path).read()
eth_client = EthJsonRpc(settings.ETHEREUM_HOST,
                        settings.ETHEREUM_RPC_PORT,
                        contract_code,
                        settings.ETHEREUM_DEFAULT_CREATOR_ADDRESS)


def set_winning_outcome_on_blockchain(event_hash, outcome):
    eth_client.eth_call(
        settings.ETHEREUM_DEFAULT_CREATOR_ADDRESS,
        'set_winning_outcome',
        [event_hash, outcome]
    )
