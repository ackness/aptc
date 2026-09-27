"""Live tests against real Aptos endpoints (devnet/mainnet).

Skipped by default; run with:

    uv run pytest -m network
"""

import time

import pytest

from aptc import Account, new_client

pytestmark = pytest.mark.network


@pytest.fixture(scope="module")
def devnet_client():
    return new_client(network="devnet")


@pytest.fixture(scope="module")
def mainnet_client():
    return new_client(network="mainnet")


def test_ledger_info(devnet_client):
    info = devnet_client.get_ledger_info()
    assert info["node_role"] == "full_node"
    assert int(info["chain_id"]) > 0


def test_health_and_node_info(devnet_client):
    assert devnet_client.check_health()["message"].startswith("aptos-node")
    assert devnet_client.get_node_info()


def test_account_reads_on_mainnet(mainnet_client):
    # 0x1 is the framework address, always present.
    account = mainnet_client.get_account("0x1")
    assert "sequence_number" in account
    assert mainnet_client.get_account_balance("0x1") > 0
    assert mainnet_client.get_account_module("0x1", "coin")["abi"]
    assert mainnet_client.estimate_gas_price()["gas_estimate"] > 0


def test_view_function(mainnet_client):
    result = mainnet_client.view_function(
        "0x1::coin::balance", ["0x1::aptos_coin::AptosCoin"], ["0x1"]
    )
    assert int(result[0]) > 0


def test_encode_submission(devnet_client):
    txn_dict = {
        "sender": "0x1",
        "sequence_number": "0",
        "max_gas_amount": "1000",
        "gas_unit_price": "100",
        "expiration_timestamp_secs": str(int(time.time()) + 600),
        "payload": {
            "type": "entry_function_payload",
            "function": "0x1::aptos_account::transfer",
            "type_arguments": [],
            "arguments": ["0x1", "1"],
        },
    }
    encoded = devnet_client.encode_submission(txn_dict)
    assert isinstance(encoded, bytes) and len(encoded) > 0


def test_devnet_faucet_and_transfer(devnet_client):
    """Full e2e: faucet mint -> sign -> submit -> wait -> balance updated."""
    sender = Account.generate()
    receiver = Account.generate()

    faucet = new_client(faucet=True, network="devnet")
    mint_hash = faucet.deposit(sender.address())
    devnet_client.wait_for_transaction(mint_hash, timeout=30)
    assert devnet_client.get_account_balance(sender.address()) > 0

    amount = 1000
    txn_dict = {
        "sender": sender.address().hex(),
        "sequence_number": str(
            devnet_client.get_account_sequence_number(sender.address())
        ),
        "max_gas_amount": "100000",
        "gas_unit_price": "100",
        "expiration_timestamp_secs": str(int(time.time()) + 600),
        "payload": {
            "type": "entry_function_payload",
            "function": "0x1::aptos_account::transfer",
            "type_arguments": [],
            "arguments": [receiver.address().hex(), str(amount)],
        },
    }
    encoded = devnet_client.encode_submission(txn_dict)
    signature = sender.sign(encoded)
    txn_dict["signature"] = {
        "type": "ed25519_signature",
        "public_key": f"{sender.public_key()}",
        "signature": f"{signature}",
    }
    submitted = devnet_client.submit_transaction(txn_dict)
    committed = devnet_client.wait_for_transaction(submitted["hash"], timeout=30)
    assert committed["success"]
    assert devnet_client.get_account_balance(receiver.address()) == amount
