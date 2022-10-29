from typing import Optional, Union

from . import APTClient, HttpxProvider
from ._types import Address
from .client import APTDevClient


def build_transfer_payload(receiver: Address, balance: int):
    return {
        'function': '0x1::aptos_account::transfer',
        'type_arguments': [],
        'arguments': [
            str(receiver),
            str(balance)
        ],
        'type': 'entry_function_payload'
    }


def new_client(node_url: Optional[str] = None, faucet: bool = False) -> Union[APTClient, APTDevClient]:
    if faucet:
        if node_url is None:
            # node_url = "https://faucet.devnet.aptoslabs.com"
            node_url = "https://tap.devnet.prod.gcp.aptosdev.com"
            # node_url = "https://faucet.testnet.aptoslabs.com"
        return APTDevClient(HttpxProvider(node_url))
    else:
        if node_url is None:
            node_url = "https://fullnode.mainnet.aptoslabs.com/v1"
        return APTClient(HttpxProvider(node_url))
