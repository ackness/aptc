"""Offline tests for request path building and client plumbing."""

import pytest
from httpx import ReadTimeout

from aptc import APTClient, HttpxProvider, new_client
from aptc.libs.utils import build_transfer_payload


class RecordingProvider:
    """Minimal provider double that records calls instead of doing HTTP."""

    DEFAULT_HEADERS = {"Content-Type": "application/json"}
    base_url = "https://example.test/v1"

    def __init__(self):
        self.calls = []
        self.call_kwargs = []
        self.client = None
        # api substring -> queue of scripted responses or exceptions
        self.results = {}

    def get(self, api="", params_dict=None, **kwargs):
        self.calls.append(("GET", api, params_dict))
        self.call_kwargs.append(kwargs)
        for key, results in self.results.items():
            if key in api and results:
                result = results.pop(0)
                if isinstance(result, Exception):
                    raise result
                return result
        if "/balance/" in api:
            return "0"
        return {}

    def post(self, api="", params_dict=None, **kwargs):
        self.calls.append(("POST", api, params_dict))
        return {}

    def patch_url(self, extra):
        return f"{self.base_url}/{extra}"


@pytest.fixture()
def client():
    return APTClient(RecordingProvider())


def test_get_account_path(client):
    client.get_account("0x1")
    assert client.provider.calls[-1] == ("GET", "accounts/0x1", None)


def test_get_account_module_uses_singular_path(client):
    # Node API exposes /accounts/{address}/module/{module_name} (singular).
    client.get_account_module("0x1", "coin")
    assert client.provider.calls[-1] == ("GET", "accounts/0x1/module/coin", None)


def test_get_account_balance_uses_balance_endpoint(client):
    client.get_account_balance("0x1")
    assert client.provider.calls[-1] == (
        "GET",
        "accounts/0x1/balance/0x1::aptos_coin::AptosCoin",
        None,
    )


def test_get_account_balance_custom_asset_type(client):
    client.get_account_balance("0x1", "0x1::foo::Bar")
    assert client.provider.calls[-1] == (
        "GET",
        "accounts/0x1/balance/0x1::foo::Bar",
        None,
    )


def test_get_event_by_event_handle_includes_field_name(client):
    client.get_event_by_event_handle("0x1", "handle", "withdraw_events")
    assert client.provider.calls[-1] == (
        "GET",
        "accounts/0x1/events/handle/withdraw_events",
        None,
    )


def test_get_table_item_posts_request_body(client):
    client.get_table_item("0xhandle", "0xkey", "0x1::string::String", "0x1::u64")
    method, api, body = client.provider.calls[-1]
    assert method == "POST"
    assert api == "tables/0xhandle/item"
    assert body == {
        "key": "0xkey",
        "key_type": "0x1::string::String",
        "value_type": "0x1::u64",
    }


def test_get_transactions_pagination_params(client):
    client.get_transactions(start=100, limit=25)
    assert client.provider.calls[-1] == (
        "GET",
        "transactions",
        {"start": "100", "limit": 25},
    )


def test_estimate_gas_price_path(client):
    client.estimate_gas_price()
    assert client.provider.calls[-1] == ("GET", "estimate_gas_price", None)


def test_view_function_body(client):
    client.view_function("0x1::coin::balance", ["0x1::aptos_coin::AptosCoin"], ["0x1"])
    method, api, body = client.provider.calls[-1]
    assert (method, api) == ("POST", "view")
    assert body == {
        "function": "0x1::coin::balance",
        "type_arguments": ["0x1::aptos_coin::AptosCoin"],
        "arguments": ["0x1"],
    }


def test_new_client_network_selection():
    client = new_client(network="devnet")
    assert client.base_url == "https://api.devnet.aptoslabs.com/v1"
    client = new_client(network="testnet")
    assert client.base_url == "https://api.testnet.aptoslabs.com/v1"
    with pytest.raises(ValueError):
        new_client(network="localnet")


def test_new_client_faucet_defaults_to_devnet():
    client = new_client(faucet=True)
    assert client.base_url == "https://faucet.devnet.aptoslabs.com"


def test_api_key_sets_bearer_header():
    provider = HttpxProvider("https://api.mainnet.aptoslabs.com/v1", api_key="secret")
    assert provider.client.headers["Authorization"] == "Bearer secret"


def test_wait_for_transaction_bounds_poll_read_timeout(client):
    # wait_by_hash is a server-held long poll: each poll gets a read timeout
    # bounded by the deadline instead of the HTTP client's shorter default.
    client.provider.results["wait_by_hash"] = [
        {"type": "user_transaction", "success": True}
    ]
    txn = client.wait_for_transaction("0xabc", timeout=30, poll_interval=0)
    assert txn["type"] == "user_transaction"
    assert client.provider.calls[-1] == (
        "GET",
        "transactions/wait_by_hash/0xabc",
        None,
    )
    assert client.provider.call_kwargs[-1]["timeout"] > 5.0


def test_wait_for_transaction_poll_timeout_is_still_pending(client):
    client.provider.results["wait_by_hash"] = [
        ReadTimeout("read timed out"),
        ReadTimeout("read timed out"),
        {"type": "user_transaction", "success": True},
    ]
    txn = client.wait_for_transaction("0xabc", timeout=30, poll_interval=0)
    assert txn["success"] is True


def test_wait_for_transaction_times_out(client):
    # provider returns {} (not found) forever -> TimeoutError, not a hang
    with pytest.raises(TimeoutError):
        client.wait_for_transaction("0xabc", timeout=0.01, poll_interval=0)


def test_build_transfer_payload():
    payload = build_transfer_payload("0xabc", 1000)
    assert payload["type"] == "entry_function_payload"
    assert payload["function"] == "0x1::aptos_account::transfer"
    assert payload["arguments"] == ["0xabc", "1000"]
