# APTC: APTOS Client for Python

![Version](https://img.shields.io/badge/aptc-v0.0.2-green)
![GitHub Org's stars](https://img.shields.io/github/stars/ackness/aptc?style=social)
![GitHub forks](https://img.shields.io/github/forks/ackness/aptc?style=social)
![Pypi](https://img.shields.io/pypi/dm/aptc)

---

[WIP] An easier RESTful client for APTOS chain than [official python client](https://github.com/aptos-labs/aptos-core/blob/main/ecosystem/python/sdk/README.md).

---

## Installation

```bash
pip install aptc

# update
pip install -U aptc
```

## Usage

### Create a client

```python
from aptc import new_client, APTOS_NODE_URL_LIST, APTClient, HttpxProvider

APT_NODE_URL = APTOS_NODE_URL_LIST[0]

# mainnet
client = new_client(node_url=APT_NODE_URL)
# or
client = APTClient(HttpxProvider(APT_NODE_URL))

# faucet client
client = new_client(faucet=True)
# claim apt from faucet
client.deposit('your address')

```

### Faucet client

The devnet faucet may sometimes not work. Some APIs are not supported by faucet.

```python
from aptc import new_client, Account

account = Account.generate()

print('account address:', account.address())
print('account private key:', account.private_key)

faucet_client = new_client(faucet=True)
txn_hash = faucet_client.deposit(account.address())
print(txn_hash)
```


### Get information from blockchain

more: [examples/example1.py](https://github.com/ackness/aptc/blob/main/examples/example1.py)


```python
from aptc import new_client, APTClient, HttpxProvider, APTOS_NODE_URL_LIST

client = new_client()

client.get_ledger_info()
client.check_health()

example_address = "0xc739507214d0e1bf9795485299d709e00024e92f7c0d055a4c2c39717882bdfd"
client.get_account(example_address)
client.get_account_balance(example_address)
client.get_account_resources(example_address)
client.get_account_transactions(example_address)

# for some nft mint, get resources is useful to get nft info
# here are one of bluemove nft mint info
some_address = "your address"
# some nft mint factory
some_resource_type = "0xf9bf19f5077c196e5468510e140d1e3cbfa0681f67fe245566ceab2399a6388d::factory::MintedByUser"
client.get_account_resource(some_address, some_resource_type)
```

### Send Transaction

Detail information about transaction, please refer to [examples/example2.py](https://github.com/ackness/aptc/blob/main/examples/example2.py)

```python
import os
import time
from aptc import Account, APT, new_client


client = new_client()

# submit transaction
# load your private key, environment variable
account = Account.load_key(os.environ['private_key'])
account_address = account.address()

# build a transaction payload
payload = {
    'function': '0x1::aptos_account::transfer',
    'type_arguments': [],
    'arguments': [
        "0x8d763223180a2b92f97755a3ea581f1c68d342275ca6118badff663f57aca7a5",  # receiver
        str(1 * APT)  # amount
    ],
    'type': 'entry_function_payload'
}

txn_dict = {
    "sender": f"{account_address}",
    "sequence_number": str(client.get_account_sequence_number(account_address)),
    "max_gas_amount": str(100_000),
    "gas_unit_price": str(100),
    "expiration_timestamp_secs": str(int(time.time()) + 100),
    "payload": payload,
}

# encode this transaction
encoded = client.encode(txn_dict)
# sign this transaction
signature = account.sign(encoded)

txn_dict["signature"] = {
    "type": "ed25519_signature",
    "public_key": f"{account.public_key()}",
    "signature": f"{signature}",
}

# submit transaction
tx = client.submit_transaction(txn_dict)
```


## Ref

1. [Aptos Node API](https://fullnode.devnet.aptoslabs.com/v1/spec#/)
2. [Aptos Python SDK](https://github.com/aptos-labs/aptos-core/blob/main/ecosystem/python/sdk/README.md)
