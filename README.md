# APTC: APTOS Client for Python

![Version](https://img.shields.io/badge/aptc-v0.1.0-green)
![GitHub Org's stars](https://img.shields.io/github/stars/ackness/aptc?style=social)
![GitHub forks](https://img.shields.io/github/forks/ackness/aptc?style=social)
![Pypi](https://img.shields.io/pypi/dm/aptc)

---

An easier RESTful client for the APTOS chain than the
[official python SDK](https://github.com/aptos-labs/aptos-python-sdk).

Targets the current Aptos Node API (`/v1`) on **mainnet**, **testnet** and
**devnet**, via the `api.{network}.aptoslabs.com` endpoints.

Requires **Python 3.14+**.

## Installation

```bash
# pip
pip install aptc

# uv (recommended)
uv add aptc
```

### Development setup (uv)

```bash
uv sync          # create .venv and install all deps (incl. dev: pytest, ruff, loguru)
uv run pytest    # run offline unit tests
uv run pytest -m network   # run the live-network tests too (devnet + mainnet)
uv run ruff check .        # lint
uv run ruff format .       # format
```

## Quick start

### Create a client

```python
from aptc import new_client, APTClient, HttpxProvider

# mainnet (default)
client = new_client()

# pick a network explicitly: "mainnet" | "testnet" | "devnet"
client = new_client(network="devnet")

# custom node URL
client = new_client(node_url="https://api.mainnet.aptoslabs.com/v1")

# with an Aptos Labs API key (higher rate limits, https://geomi.dev)
client = new_client(network="mainnet", api_key="aptoslabs_...")

# or construct manually
client = APTClient(HttpxProvider("https://api.mainnet.aptoslabs.com/v1"))
```

Default endpoints (`aptc/configs.py`):

| Network | Node API (`/v1`) | Faucet |
| --- | --- | --- |
| mainnet | `https://api.mainnet.aptoslabs.com/v1` | — |
| testnet | `https://api.testnet.aptoslabs.com/v1` | requires Google sign-in (JWT) |
| devnet | `https://api.devnet.aptoslabs.com/v1` | `https://faucet.devnet.aptoslabs.com` |

### Faucet client (devnet)

```python
from aptc import new_client, Account

account = Account.generate()
print("account address:", account.address())

faucet_client = new_client(faucet=True)  # devnet faucet
txn_hash = faucet_client.deposit(account.address())
print(txn_hash)
```

> The **testnet** faucet (`faucet.testnet.aptoslabs.com`) requires Google
> sign-in and can no longer be used programmatically. Use devnet, or the
> [Aptos mint page](https://aptos.dev/network/faucet) for testnet.

### Read from the blockchain

See [examples/example1.py](examples/example1.py).

```python
from aptc import new_client

client = new_client()

client.get_ledger_info()  # chain id, epoch, ledger version, ...
client.check_health()  # {"message": "aptos-node:ok"}
client.get_node_info()  # node identity / sync info
client.estimate_gas_price()  # {"gas_estimate": ..., ...}

address = "0x1"
client.get_account(address)
client.get_account_balance(address)  # uses /accounts/{addr}/balance/{asset_type}
client.get_account_resources(address)
client.get_account_resource(address, "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>")
client.get_account_modules(address)
client.get_account_module(address, "coin")  # GET /accounts/{addr}/module/{name}
client.get_account_transactions(address)
client.get_account_transaction_summaries(address)

# blocks / transactions
client.get_block_by_height(1234)
client.get_transaction_by_hash("0x...")
client.get_transaction_by_version(123456)
client.wait_transaction_by_hash("0x...")  # long-poll variant

# view functions (on-chain read-only calls)
client.view_function(
    "0x1::coin::balance",
    type_arguments=["0x1::aptos_coin::AptosCoin"],
    arguments=["0x1"],
)  # -> [11120868786]

# table items
client.get_table_item(handle, key, key_type="0x1::string::String", value_type="u64")
client.get_table_item_raw(handle, key="0x...")
```

### Send a transaction

See [examples/example2.py](examples/example2.py) for details.

```python
import os
import time
from aptc import Account, APT, new_client

client = new_client()

# load your private key from an environment variable
account = Account.load_key(os.environ["private_key"])
account_address = account.address()

payload = {
    "function": "0x1::aptos_account::transfer",
    "type_arguments": [],
    "arguments": [
        "0x8d763223180a2b92f97755a3ea581f1c68d342275ca6118badff663f57aca7a5",  # receiver
        str(1 * APT),  # amount in octas (1 APT = 10^8 octas)
    ],
    "type": "entry_function_payload",
}

txn_dict = {
    "sender": f"{account_address}",
    "sequence_number": str(client.get_account_sequence_number(account_address)),
    "max_gas_amount": str(100_000),
    "gas_unit_price": str(100),
    "expiration_timestamp_secs": str(int(time.time()) + 600),
    "payload": payload,
}

# encode (BCS) -> sign -> attach signature -> submit
encoded = client.encode_submission(txn_dict)  # or client.encode(...)
signature = account.sign(encoded)

txn_dict["signature"] = {
    "type": "ed25519_signature",
    "public_key": f"{account.public_key()}",
    "signature": f"{signature}",
}

tx = client.submit_transaction(txn_dict)
client.wait_for_transaction(tx["hash"])
```

## Testing

```bash
uv run pytest               # offline unit tests
uv run pytest -m network    # + live devnet/mainnet tests, incl. faucet->transfer e2e
```

## Ref

1. [Aptos Fullnode REST API](https://aptos.dev/build/apis/fullnode-rest-api)
2. [Node API spec (OpenAPI)](https://github.com/aptos-labs/aptos-core/blob/main/api/doc/spec.yaml)
3. [Aptos Python SDK](https://github.com/aptos-labs/aptos-python-sdk)
