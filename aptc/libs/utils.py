from ..configs import FAUCET_URLS, NODE_URLS
from . import APTClient, HttpxProvider
from ._types import Address
from .client import APTDevClient


def build_transfer_payload(receiver: Address, balance: int):
    return {
        "function": "0x1::aptos_account::transfer",
        "type_arguments": [],
        "arguments": [str(receiver), str(balance)],
        "type": "entry_function_payload",
    }


def new_client(
    node_url: str | None = None,
    faucet: bool = False,
    network: str = "mainnet",
    api_key: str | None = None,
) -> APTClient | APTDevClient:
    """Create a client for the given Aptos network.

    `network` is one of "mainnet", "testnet", "devnet" and picks the matching
    default node/faucet URL. `api_key` is sent as `Authorization: Bearer <key>`
    for Aptos Labs hosted endpoints (optional, raises the rate limit).

    With `faucet=True` a devnet/testnet faucet client is returned. Note that the
    testnet faucet requires Google sign-in (JWT) and cannot be used
    programmatically; use `network="devnet"` or the web mint page instead.
    """
    if faucet:
        if node_url is None:
            faucet_network = network if network in FAUCET_URLS else "devnet"
            node_url = FAUCET_URLS[faucet_network]
        return APTDevClient(HttpxProvider(node_url, api_key=api_key))
    if node_url is None:
        if network not in NODE_URLS:
            raise ValueError(
                f"unknown network: {network!r}, expected one of {sorted(NODE_URLS)}"
            )
        node_url = NODE_URLS[network]
    return APTClient(HttpxProvider(node_url, api_key=api_key))
